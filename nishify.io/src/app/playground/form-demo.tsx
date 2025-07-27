'use client'

import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'

export default function ProductForm() {
  return (
    <form className="space-y-4 max-w-md">
      <div>
        <Label htmlFor="name">Product Name</Label>
        <Input id="name" placeholder="Enter product name" />
      </div>
      <div>
        <Label htmlFor="price">Price</Label>
        <Input id="price" type="number" placeholder="Enter price" />
      </div>
      <Button type="submit">Submit</Button>
    </form>
  )
}
