```


### TODO : Separate test db and make following success and asdd more test cases as well. 
PYTHONPATH=.  pytest backend/tests/pioneer_wholesale_inc


```
✅ Copy-Paste URLs (Assume localhost:8000)
🔍 Text Filters
1. Name contains "success"

http://localhost:8000/api/item?name__contains=success
2. Description contains "girl"

http://localhost:8000/api/item?description__contains=girl
3. Unit starts with "mi" (like “million”)

http://localhost:8000/api/item?unit__startswith=mi
🔢 Numeric Filters
4. Price > 8000

http://localhost:8000/api/item?price__gt=8000
5. Price < 1000

http://localhost:8000/api/item?price__lt=1000
6. Price between 1000 and 2000

http://localhost:8000/api/item?price__gte=1000&price__lte=2000
🆔 ID / Foreign Key Filters
7. category_id = 9558

http://localhost:8000/api/item?category_id=9558
8. vendor_id in [5432, 684, 2278]

http://localhost:8000/api/item?vendor_id__in=5432,684,2278
9. cash_discount_group_id = 3900

http://localhost:8000/api/item?cash_discount_group_id=3900
🟢 Boolean Field
10. Only Active Items

http://localhost:8000/api/item?active=true
11. Only Inactive Items

http://localhost:8000/api/item?active=false
📄 Pagination and Sorting
12. Page 2, 10 items per page

http://localhost:8000/api/item?skip=10&limit=10
13. Sorted by price (ASC)

http://localhost:8000/api/item?sort=price
14. Sorted by price (DESC)

http://localhost:8000/api/item?sort=-price
🎯 Combined Filters
15. Active items with price > 5000

http://localhost:8000/api/item?active=true&price__gt=5000
16. Items with name="success" and vendor_id=116

http://localhost:8000/api/item?name=success&vendor_id=116
17. Search "success" and sort by price desc

http://localhost:8000/api/item?name__contains=success&sort=-price

```












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




python -m infra.data_faker pioneer_wholesale_inc
python -m infra.code_generator pioneer_wholesale_inc


PYTHONPATH=. alembic revision --autogenerate -m "initial schema"

PYTHONPATH=. alembic upgrade head


PYTHONPATH=. python backend/scripts/load_sample_data.py
PYTHONPATH=. python backend/scripts/show_counts.py  item

PYTHONPATH=. python backend/search_elastic/indexer.py


uvicorn backend.main:app --reload


