'use client'

// import { Button } from '@/components/ui/button'
// import { Card } from '@/components/ui/card'
// import ProductForm from './form-demo'
// import ProductTable from './table-demo'

export default function PlaygroundPage() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-xl font-bold">🧪 Component Playground</h1>

      <section>
        <h2 className="text-lg font-semibold mb-2">Button Variants</h2>
        <div className="flex gap-2">
          {/* <Button variant="default">Default</Button>
          <Button variant="destructive">Destructive</Button>
          <Button variant="outline">Outline</Button>*/}
        </div> 
      </section>

      <section>
        <h2 className="text-lg font-semibold mt-6 mb-2">Form Preview</h2>
        {/* <ProductForm /> */}
      </section>

      <section>
        <h2 className="text-lg font-semibold mt-6 mb-2">Table Preview</h2>
        {/* <ProductTable /> */}
      </section>
    </div>
  )
}
