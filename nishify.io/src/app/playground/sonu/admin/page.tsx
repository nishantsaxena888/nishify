// src/app/admin/page.tsx
'use client'

import { useEffect, useState } from 'react'
import { loadEntityOptions } from '../../lib/api/mock'
import { MenuItem } from '@/types'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

export default function AdminPage() {
  const [menuItems, setMenuItems] = useState<MenuItem[]>([])

  useEffect(() => {
    async function fetchMenu() {
      try {
        const data = await loadEntityOptions('menu')
        setMenuItems(data.fields || [])
      } catch (err) {
        console.error('Failed to load menu', err)
      }
    }
    fetchMenu()
  }, [])

  return (
    <div className="min-h-screen bg-background text-foreground p-6">
      <h1 className="text-2xl font-bold mb-4">🧭 Admin Dashboard</h1>

      <div className="grid grid-cols-2 gap-4 max-w-md">
        {menuItems.map((item) => (
          <Link href={item.path} key={item.label}>
            <Button className="w-full justify-start gap-2" variant="outline">
              {item.icon && <span className="text-lg">{item.icon}</span>}
              {item.label}
            </Button>
          </Link>
        ))}
      </div>
    </div>
  )
}
