"""
Data Faker (deterministic, FK-aware)
------------------------------------
ENV:
  CLIENT_NAME=<client>   # required
  SEED=1337              # optional deterministic seed
"""
import os, importlib, random, hashlib, datetime, pprint
from typing import Dict, Any

CLIENT = os.environ.get("CLIENT_NAME")
if not CLIENT:
    raise SystemExit("ERROR: Set CLIENT_NAME env.")

SEED = int(os.environ.get("SEED", "1337"))

def _stable_id(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:16]

def _dt_now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"

def _import(path: str):
    return importlib.import_module(path)

def _normalize_fields(cfg: dict) -> dict:
    fields = {}
    for fname, spec in (cfg.get("fields") or {}).items():
        s = dict(spec)
        if s.get("primary_key") and not s.get("pk"):
            s["pk"] = True
        if s.get("foreign_key") and not s.get("fk"):
            s["fk"] = s["foreign_key"]
        fields[fname] = s
    return {**cfg, "fields": fields}

def _topo_order(entities: Dict[str, Any]):
    graph = {n:set() for n in entities}
    for n,cfg in entities.items():
        for _, fcfg in (cfg.get("fields") or {}).items():
            fk = fcfg.get("fk") or fcfg.get("foreign_key")
            if fk:
                parent = fk.split(".")[0].strip()
                if parent in entities and parent != n:
                    graph[n].add(parent)
    resolved, seen, temp = [], set(), set()
    def visit(node):
        if node in seen: return
        if node in temp: raise RuntimeError(f"Cyclic FK at {node}")
        temp.add(node)
        for dep in graph[node]:
            visit(dep)
        temp.remove(node)
        seen.add(node)
        resolved.append(node)
    for n in graph: visit(n)
    return resolved

def _gen_value(field_name, spec, i):
    t = (spec.get("type") or "string").lower()
    if t in ("string","text","keyword"):
        return f"{field_name}_{i}"
    if t in ("int","integer"):
        return i+1
    if t in ("float","double","number"):
        return round(100 + i*1.1, 2)
    if t in ("bool","boolean"):
        return (i % 2) == 0
    if t in ("date","datetime","timestamp"):
        base = datetime.date(2025, 1, 1)
        return base + datetime.timedelta(days=i%365)
    return f"{field_name}_{i}"

def generate_sample(entities_in: Dict[str, Any]):
    entities = {name: _normalize_fields(cfg) for name, cfg in entities_in.items()}
    random.seed(SEED)
    order = _topo_order(entities)
    out = {}
    for name in order:
        cfg = entities[name]
        fields = cfg.get("fields", {})
        n = int(cfg.get("seed_rows", 5))
        rows = []
        uniques = {f for f,s in fields.items() if s.get("unique")}
        ut_specs = cfg.get("unique_together", [])
        ut_sets = [set() for _ in ut_specs]
        # inject surrogate PK in-memory if missing
        if not any((isinstance(v, dict) and v.get("pk")) for v in fields.values()):
            fields = {"id": {"type": "string", "pk": True}, **fields}
        for i in range(n):
            row = {}
            # pass 1: non-FK
            for fname, spec in fields.items():
                if spec.get("pk") or spec.get("primary_key"):
                    # typed PK (int/string/etc.)
                    row[fname] = _gen_value(fname, spec, i)
                elif spec.get("fk"):
                    continue
                else:
                    row[fname] = _gen_value(fname, spec, i)
            # pass 2: FK resolve
            for fname, spec in fields.items():
                fk = spec.get("fk")
                if not fk: continue
                parent, pfield = [x.strip() for x in fk.split(".")]
                parent_rows = out.get(parent) or []
                if not parent_rows:
                    raise RuntimeError(f"FK {name}.{fname} -> {fk} missing parents")
                row[fname] = parent_rows[i % len(parent_rows)][pfield]
            # uniques
            for u in uniques:
                v = row.get(u)
                if any(r.get(u)==v for r in rows):
                    row[u] = f"{v}_{i}"
            for j, ut in enumerate(ut_specs):
                key = tuple(row.get(f) for f in ut)
                if key in ut_sets[j]:
                    last = ut[-1]
                    row[last] = f"{row[last]}_{i}"
                    key = tuple(row.get(f) for f in ut)
                ut_sets[j].add(key)
            rows.append(row)
        out[name] = rows
    return out

def write_outputs(client, sample):
    client_dir = os.path.join("clients", client)
    os.makedirs(client_dir, exist_ok=True)
    meta = {
        "generated_at": _dt_now_iso(),
        "client": client,
        "seed": SEED,
        "checksum": hashlib.sha1(repr(sample).encode("utf-8")).hexdigest(),
    }
    content = (
        f"# AUTO-GENERATED for {client}. Do not edit by hand.\n"
        f"# Source: clients/{client}/entities.py\n"
        f"# Seed: {SEED}\n\n"
        f"import datetime\n\n"
        f"sample_data = {pprint.pformat(sample, width=100, sort_dicts=True)}\n"
        f"entities_data = sample_data\n"
        f"\n__meta__ = {pprint.pformat(meta, width=100, sort_dicts=True)}\n"
    )
    with open(os.path.join(client_dir, "entities.data.py"), "w", encoding="utf-8") as f:
        f.write(content)
    with open(os.path.join(client_dir, "entities_data.py"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[data_faker] Wrote {client_dir}/entities.data.py and entities_data.py")

def main():
    mod = _import(f"clients.{CLIENT}.entities")
    entities = getattr(mod, "entities", None)
    if not isinstance(entities, dict):
        raise SystemExit("ERROR: entities.py must define `entities` dict")
    sample = generate_sample(entities)
    write_outputs(CLIENT, sample)
    print("[data_faker] Done.")

if __name__ == "__main__":
    main()
