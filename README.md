```mermaid

flowchart TD
  %% ---------- Infra ----------
  subgraph INFRA["Infra"]
    A["infra/data_faker.py — generate seed/sample data"] --> B["clients/&lt;client&gt;/entities.data.py — generated sample_data + ids"]
    B --> C["infra/code_generator.py — reads entities.data.py, entities.py, elastic_entities.py"]
  end

  %% ---------- Codegen Outputs ----------
  subgraph OUT["Codegen Outputs"]
    C --> M["backend/clients/&lt;client&gt;/models/*.py — SQLAlchemy models"]
    C --> T["backend/clients/&lt;client&gt;/testdata/*.json — API & DB test payloads"]
    C --> X["backend/clients/&lt;client&gt;/excel/sample_output.xlsx — sample export"]
    C --> U["backend/tests/&lt;client&gt;/test_*.py — pytest integration tests"]
    C --> CF["copy client files → {entities.py, elastic_entities.py}"]
    C --> CFG["backend/clients/&lt;client&gt;/config/* — generated config (optional)"]
  end

  %% ---------- DB & Migrations ----------
  subgraph DBMIG["DB & Migrations"]
    CF --> ALE["alembic autogenerate"]
    ALE --> UP["alembic upgrade"]
    UP --> DB["Database Ready — SQLite/Postgres schema"]
  end

  %% ---------- Runtime Services ----------
  subgraph RUNTIME["Runtime Services"]
    DB --> API["FastAPI CRUD — backend/routers/entity_router.py"]
    DB --> IDX["backend/search_elastic/indexer.py — build indices"]
    IDX -. "if configured" .-> ES["Elasticsearch indices"]
    ES -. "search results" .-> API
    API --> FE["Frontend (GenericTable, hooks, api)"]
  end

```
```
flowchart LR
  FE["Frontend (GenericTable, hooks, api)"]
    --> |"/api/{entity}?filters,sort,limit,offset"| R["FastAPI Router: backend/routers/entity_router.py"]

  %% Domain configs feeding router behavior
  ENT["clients/&lt;client&gt;/entities.py — fields, defaults, validators, options schema"] --> R
  ESE["clients/&lt;client&gt;/elastic_entities.py — indexing rules"] --> R

  %% Router internals
  subgraph ROUTER["Router"]
    direction TB
    R --> |"/options"| OPT["Options: basic or schema=full (fields + defaults + validators)"]
    R --> |"GET list"| GETL["Query builder → SQL or ES + pagination"]
    R --> |"GET one"| GET1["Select by primary key"]
    R --> |"POST"| POST["Validate → apply defaults → insert → audit"]
    R --> |"PUT"| PUT["Partial validate → update by PK → audit"]
    R --> |"DELETE"| DEL["Delete by PK"]
  end

  %% Models + DB
  R --> |"model resolution"| MDL["backend/clients/&lt;client&gt;/models/*.py — SQLAlchemy"]
  MDL --> DB["DB (SQLite/Postgres)"]

  %% Optional ES path
  R -. "if indexed" .-> ES["Elasticsearch"]
  ES -. "search results" .-> R

  %% Response back to UI
  R --> RESP["JSON: {items, count} or {item} or {error[]}"]
  RESP --> FE
```


```mermaid
flowchart TD
  A["infra/data_faker.py - generate sample data"] --> B["clients/<client>/entities.data.py"]
  B --> C["infra/code_generator.py - backend focus"]
  C --> C1["backend models: backend/clients/<client>/models/*.py"]
  C --> C2["backend test data: backend/clients/<client>/testdata/*.json"]
  C --> C3["excel dump: backend/clients/<client>/excel/sample_output.xlsx"]
  C --> C4["backend tests: backend/tests/<client>/test_*.py"]
  C --> C5["copy client files: entities.py, elastic_entities.py"]
  C5 --> D["alembic autogenerate → upgrade"]
  D --> E["backend DB ready"]
  E --> G["backend/search_elastic/indexer.py - index to Elasticsearch"]
  E --> H["FastAPI CRUD live"]
  H --> I["Frontend tests/UI (optional)"]
```

```mermaid
flowchart LR
  FE["Frontend (GenericTable, hooks, api)"] --> |"/api/:entity?filters"| R["FastAPI Router: backend/routers/entity_router.py"]

  subgraph Router
    R --> |"/options"| O["options: basic OR schema=full"]
    R --> |"GET list"| L["SQL/ES query + pagination"]
    R --> |"GET one"| G1["select by PK"]
    R --> |"POST"| P1["validate + defaults + insert"]
    R --> |"PUT"| U1["partial validate + update"]
    R --> |"DELETE"| D1["delete by PK"]
  end

  R --> MDL["SQLAlchemy Models: backend/clients/&lt;client&gt;/models/*.py"]
  MDL --> DB["(SQLite/Postgres)"]
  R -. "if indexed" .-> ES["(Elasticsearch)"]

```
```
$ Nonpx create-next-app@latest nishify.io 
✔ Would you like to use TypeScript? … No / Yes
✔ Would you like to use ESLint? … No / Yes
✔ Would you like to use Tailwind CSS? … No / Yes
✔ Would you like your code inside a `src/` directory? … No / Yes
✔ Would you like to use App Router? (recommended) … No / Yes
✔ Would you like to use Turbopack for `next dev`? … No / Yes
✔ Would you like to customize the import alias (`@/*` by default)? … No / Yes    => @ bole to src and import easy no need of .././ just use @
Creating a new Next.js app in /Users/nishantsaxena/workspace/nishify/nishify.io


nishify.io/
├── public/
├── src/
│   ├── app/              # App Router enabled
│   ├── components/       # Reusable components (Nav, Hero, Footer, etc.)
│   ├── sections/         # Page sections (Hero, About, Projects, etc.)
│   ├── styles/           # Tailwind + any custom styles
│   └── utils/            # Any helper functions or constants
├── tailwind.config.ts
├── tsconfig.json
├── next.config.js
└── package.json

$ git remote -v 
origin	https://github.com/nishantsaxena888/nishify.git (fetch)
origin	https://github.com/nishantsaxena888/nishify.git (push)

# Note : not  https but git i.e. ssh is set , so it won't prompt for password
git remote set-url origin git@github.com:nishantsaxena888/nishify.git
> Idea : TOC main FAQ 
>> move all this to TOC
```

