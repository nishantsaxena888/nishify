'use client'

import { Button } from '@/components/ui/button'
import { ModeToggle } from '@/components/mode-toggle'
import ProductForm from './form-demo'
import { ThemeSwitcher } from '@/components/ThemeSwitcher'



export default function PlaygroundPage() {
  return (

    <div className="min-h-screen bg-background text-foreground p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">🧪 Playground</h1>
        <ModeToggle />
        <ThemeSwitcher />
      </div>
<div className="bg-background text-foreground p-4">
  Check Theme: Background and text color should change.
</div>
      <section className="space-y-4">
        <h2 className="text-lg font-semibold mb-2">Buttons</h2>
        <div className="flex gap-2">
          <Button variant="default">Default</Button>
          <Button variant="destructive">Destructive</Button>
          <Button variant="outline">Outline</Button>
        </div>
      </section>

      <section className="mt-10 space-y-4">
        <h2 className="text-lg font-semibold mb-2">Form</h2>
        <ProductForm />
      </section>
    </div>
  )
}
