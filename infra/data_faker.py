#!/usr/bin/env python3
import os, sys, random, importlib.util, pprint
from typing import Dict, Any, List, Set, Tuple, Optional
from faker import Faker

# -------------------- CLI / paths --------------------
faker = Faker()
if len(sys.argv) < 2:
    raise ValueError("Usage: python data_faker.py <client_name> [rows_per_entity]")
CLIENT_NAME = sys.argv[1]
ROWS_PER_ENTITY = int(sys.argv[2]) if len(sys.argv) > 2 else int(os.getenv("FAKER_ROWS", "25"))

INFRA_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(INFRA_DIR, ".."))
CLIENT_DIR = os.path.join(ROOT_DIR, "clients", CLIENT_NAME)
ENTITIES_PATH = os.path.join(CLIENT_DIR, "entities.py")
ENTITIES_DATA_PATH = os.path.join(CLIENT_DIR, "entities.data.py")

# Optional reproducibility
seed = os.getenv("FAKER_SEED")
if seed is not None:
    seed = int(seed)
    random.seed(seed)
    Faker.seed(seed)

# -------------------- Load entities.py --------------------
spec = importlib.util.spec_from_file_location("entities", ENTITIES_PATH)
entities_mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(entities_mod)  # type: ignore

entities_config: Dict[str, Any] = getattr(entities_mod, "entities")
def _augment_sample_data_with_required_ids(entities_cfg: Dict[str, Any]) -> Dict[str, Any]:
    def _ensure(entity, rows):
        ent = entities_cfg.get(entity) or {}
        sd = ent.get("sample_data") or []
        existing_ids = {r.get("id") for r in sd if isinstance(r, dict)}
        for r in rows:
            if r.get("id") not in existing_ids:
                sd.append(r)
        ent["sample_data"] = sd
        entities_cfg[entity] = ent

    # test prerequisites (ids used in your tests)
    _ensure("invoice", [{"id": 2}, {"id": 804802}])
    _ensure("item", [{"id": 804803, "name": "Seeded Item"}])
    return entities_cfg

entities_config = _augment_sample_data_with_required_ids(entities_config)



# -------------------- Helpers --------------------
TYPE_SYNONYMS = {
    "int": "int",
    "integer": "int",
    "number": "float",
    "float": "float",
    "double": "float",
    "decimal": "float",
    "str": "str",
    "string": "str",
    "text": "str",
    "bool": "bool",
    "boolean": "bool",
    "datetime": "datetime",
    "timestamp": "datetime",
    "date": "date",
    "json": "json",
}

def norm_type(t: Optional[str]) -> str:
    if not t:
        return "str"
    return TYPE_SYNONYMS.get(t.lower(), t.lower())

def parse_fk_target(val: Any) -> Optional[str]:
    """Return target entity name from 'foreign_key' meta: 'state.id' -> 'state'."""
    if not val:
        return None
    s = str(val)
    if "." in s:
        return s.split(".", 1)[0]
    return s

def generate_faker_value(expr: str):
    # expr like: "name()", "email()", "address()", "pyint(min_value=1, max_value=9999)", ...
    try:
        return eval(f"faker.{expr}", {"faker": faker})
    except Exception:
        return None

def generate_default_value(field_type: str) -> Any:
    t = norm_type(field_type)
    if t == "int":
        return random.randint(1, 9999)
    if t == "float":
        return round(random.uniform(1, 9999), 2)
    if t == "bool":
        return random.choice([True, False])
    if t == "datetime":
        return faker.date_time_this_year()
    if t == "date":
        return faker.date_this_year()
    if t == "json":
        return {"note": faker.sentence()}
    return faker.word()  # str

def is_required(field_cfg: Dict[str, Any]) -> bool:
    # Prefer explicit flags if present
    if field_cfg.get("required") is True:
        return True
    if field_cfg.get("nullable") is False:
        return True
    # If primary key, required
    if field_cfg.get("primary_key") is True:
        return True
    return False

def is_unique(field_cfg: Dict[str, Any]) -> bool:
    return bool(field_cfg.get("unique", False))

def primary_key_name(fields: Dict[str, Dict[str, Any]]) -> str:
    for k, v in fields.items():
        if v.get("primary_key"):
            return k
    return "id"

def dependency_graph(entities_conf: Dict[str, Any]) -> Dict[str, Set[str]]:
    """child -> set(parent) edges based on foreign_key metadata."""
    g: Dict[str, Set[str]] = {e: set() for e in entities_conf.keys()}
    for e, cfg in entities_conf.items():
        for fname, fcfg in (cfg.get("fields") or {}).items():
            target = parse_fk_target(fcfg.get("foreign_key"))
            if target and target in g and target != e:
                g[e].add(target)
            elif fname.endswith("_id") and fname[:-3] in g and fname[:-3] != e:
                g[e].add(fname[:-3])
    return g

def topo_sort(graph: Dict[str, Set[str]]) -> List[str]:
    """Kahn's algorithm; if cycle, fall back to original order at the end."""
    indeg = {n: 0 for n in graph}
    for n in graph:
        for m in graph[n]:
            indeg[n] += 1
    q = [n for n in graph if indeg[n] == 0]
    out = []
    while q:
        n = q.pop()
        out.append(n)
        for m in graph:
            if n in graph[m]:
                indeg[m] -= 1
                if indeg[m] == 0:
                    q.append(m)
    # Append any leftovers (cycles) in original order
    for n in graph:
        if n not in out:
            out.append(n)
    return out

# -------------------- Generation --------------------
entities_data: Dict[str, Any] = {}
id_pools: Dict[str, List[int]] = {}   # entity -> list of ids we've generated
unique_track: Dict[Tuple[str, str], Set[Any]] = {}  # (entity, field) -> values

order = topo_sort(dependency_graph(entities_config))

for entity_name in order:
    cfg = entities_config.get(entity_name) or {}
    fields: Dict[str, Dict[str, Any]] = cfg.get("fields") or {}
    pk = primary_key_name(fields)

    rows: List[Dict[str, Any]] = []
    used_ids: Set[int] = set()

    # Pre-compute parent choices for FKs
    fk_fields: List[Tuple[str, str]] = []  # (field_name, parent_entity)
    for fname, fcfg in fields.items():
        target = parse_fk_target(fcfg.get("foreign_key"))
        if target and target in entities_config:
            fk_fields.append((fname, target))
        elif fname.endswith("_id") and (fname[:-3] in entities_config):
            fk_fields.append((fname, fname[:-3]))
