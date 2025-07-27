// src/components/ClientShell.tsx
'use client'

import { ReactNode } from 'react'
import { ThemeSwitcher } from '@/components/ThemeSwitcher'
import { ModeToggle } from '@/components/mode-toggle'
import AdminMenu from './AdminMenu'

export default function ClientShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen bg-background text-foreground">
      <aside className="w-64 border-r border-border p-4">
        <div className="mb-6 text-lg font-bold">Client Admin</div>
        <AdminMenu />
      </aside>
      <main className="flex-1 p-4">
        <div className="flex justify-end gap-2 mb-4">
          <ThemeSwitcher />
          <ModeToggle />
        </div>
        {children}
      </main>
    </div>
  )
}