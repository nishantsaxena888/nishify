########## 1 
```
npx create-next-app@latest nishinvent
npx shadcn@latest init 

npx shadcn@latest add button card input form table dialog

npx shadcn@latest add button card input form table dialog

✔ Checking registry.
✔ Installing dependencies.
✔ Created 7 files:
  - src/components/ui/button.tsx
  - src/components/ui/card.tsx
  - src/components/ui/input.tsx
  - src/components/ui/form.tsx
  - src/components/ui/label.tsx
  - src/components/ui/table.tsx
  - src/components/ui/dialog.tsx


```

######### 2
``` How To Add shadcn components
nishantsaxena@Nishants-MacBook-Pro nishinvent % npx shadcn@latest add button card input form table dialog

✔ Checking registry.
✔ Installing dependencies.
ℹ Skipped 7 files: (files might be identical, use --overwrite to overwrite)
  - src/components/ui/button.tsx
  - src/components/ui/card.tsx
  - src/components/ui/input.tsx
  - src/components/ui/form.tsx
  - src/components/ui/label.tsx
  - src/components/ui/table.tsx
  - src/components/ui/dialog.tsx

nishantsaxena@Nishants-MacBook-Pro nishinvent % ls src/components/ui                                     
button.tsx	card.tsx	dialog.tsx	form.tsx	input.tsx	label.tsx	table.tsx
nishantsaxena@Nishants-MacBook-Pro nishinvent % git diff package.json 
diff --git a/nishinvent/package.json b/nishinvent/package.json
index 5ec9ff6..7b657a9 100644
--- a/nishinvent/package.json
+++ b/nishinvent/package.json
@@ -9,13 +9,19 @@
     "lint": "next lint"
   },
   "dependencies": {
+    "@hookform/resolvers": "^5.2.0",
+    "@radix-ui/react-dialog": "^1.1.14",
+    "@radix-ui/react-label": "^2.1.7",
+    "@radix-ui/react-slot": "^1.2.3",
     "class-variance-authority": "^0.7.1",
     "clsx": "^2.1.1",
     "lucide-react": "^0.526.0",
     "next": "15.4.4",
     "react": "19.1.0",
     "react-dom": "19.1.0",
-    "tailwind-merge": "^3.3.1"
+    "react-hook-form": "^7.61.1",
+    "tailwind-merge": "^3.3.1",
+    "zod": "^4.0.10"
   },
   "devDependencies": {
     "@eslint/eslintrc": "^3"
```

#########3 

```
Add lucid react components : 


npm install lucide-react.

🧩 Common Icons You May Use:
Icon	Component Name	Use-case
🏠	Home	Dashboard/Home link
📦	Package	Inventory/Products
🧾	ClipboardList	Orders
🧑‍💼	User	Users/Admin
⚙️	Settings	Settings Panel
➕	Plus	Create/Add Button
✏️	Pencil	Edit Action

Lucide Icons ka React version install karta hai — ek modern, lightweight, and open-source icon library 
jo Heroicons jaisa feel deta hai lekin zyaada customizable aur developer-friendly hai.
Purpose: 500+ SVG icons as React components
Size: Tree-shakable, only imports what you use
Because building a clean admin panel with side nav + forms + tables, 
Lucide gives you production-grade icons with very low setup.

lucide-react gives you high-quality, modern SVG icons as React components that 
fit perfectly with shadcn/ui and Tailwind.


```
############## 4 

```

npx storybook@latest init --builder vite

npm run storybook
```


