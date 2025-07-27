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

```
npm install -D postcss autoprefixer
npx shadcn@latest init
npx shadcn@latest add button card input form table dialog
ls src/components/ui
    button.tsx	card.tsx	dialog.tsx	form.tsx	input.tsx	label.tsx	table.tsx
```


```
✅ 1. ThemeProvider (from next-themes)
Yeh dark / light mode ke liye hai.
It works via <html class="dark"> or <html class="light">
<ThemeProvider attribute="class" defaultTheme="light" enableSystem>

✅ 2. ThemeSwitcher (your own)
Yeh brand theme ke liye hai — jaise amberland, emeraldline, etc.
Iska kaam hai data-theme="amberland" ya class theme-amberland lagana.
But: this is separate from light/dark theme.
✅ ✅ Final Goal
💡 Light/Dark via next-themes
🎨 Branded Themes via your own ThemeSwitcher
🍪 Persistent theme using localStorage/cookie
🔁 Fully integrated without conflict

```

