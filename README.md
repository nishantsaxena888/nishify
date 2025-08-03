```
python -m infra.code_generator pioneer_wholesale_inc

PYTHONPATH=.  pytest backend/tests/pioneer_wholesale_inc


PYTHONPATH=. alembic revision --autogenerate -m "initial schema"

PYTHONPATH=. alembic upgrade head



python3 -m venv .venv 
source .venv/bin/activate 
pip install -r requirements.txt 
cd nishify.io 
npm install 
npm run dev 

nishify/
├── infra/
│   ├── code_generator.py
│   └── pioneer_wholesale_inc/
│       └── entities.py
│   └── shareaplace/
│       └── entities.py
├── backend/
│   └── clients/
│       └── pioneer_wholesale_inc/
│           ├── models/
│           └── test_data/
├── nishify.io/
│   └── src/lib/api/mock/
│       └── pioneer_wholesale_inc/
│           ├── customer.ts
│           ├── invoice.ts

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

