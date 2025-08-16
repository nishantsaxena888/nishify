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

