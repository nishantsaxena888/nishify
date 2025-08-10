// src/components/admin/AdminShell.tsx
'use client'
import { useEffect, useState } from 'react'
import cfg from '@/clients/pioneer_wholesale_inc/frontend.api.config.json'
import GenericForm from './GenericForm'
import GenericTable from './GenericTable'

export type Row = Record<string, any>

export default function AdminShell({ entity }: { entity: string }) {
  const [selected, setSelected] = useState<Row | null>(null)
  const [refreshTick, setRefreshTick] = useState(0)

  useEffect(() => setSelected(null), [entity])

  const entities = Object.keys(cfg.routing)

  return (
    <div className="grid grid-cols-[240px_1fr] h-full">
      <aside className="border-r p-4 space-y-2">
        <div className="text-sm font-semibold mb-2">Entities</div>
        <ul className="space-y-1">
          {entities.map((e) => (
            <li key={e}>
              <a
                href={`/dashboard/${e}`}
                className={`block rounded px-2 py-1 text-sm hover:bg-muted ${e === entity ? 'bg-muted font-medium' : ''}`}
              >
                {e}
              </a>
            </li>
          ))}
        </ul>
      </aside>

      <main className="p-4 space-y-6">
        <GenericForm
          entity={entity}
          value={selected}
          onSaved={() => {
            setSelected(null)
            setRefreshTick(t => t + 1)
          }}
          onCancel={() => setSelected(null)}
        />

        <GenericTable
          entity={entity}
          refreshKey={refreshTick}
          onSelectRow={(row) => setSelected(row)}
        />
      </main>
    </div>
  )
}
