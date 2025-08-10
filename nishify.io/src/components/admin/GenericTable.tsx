// src/components/admin/GenericTable.tsx
'use client'
import { useMemo, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { useEntityList, useEntityOptions } from './hooks'
import { fetchEntityData } from '@/lib/api'

type Props = {
  entity: string
  onSelectRow?: (row: Record<string, any>) => void
}

export default function GenericTable({ entity, onSelectRow }: Props) {
  const [tab, setTab] = useState<'all'|'active'|'inactive'|'recent'>('all')
  const { rows, loading } = useEntityList(entity, tab)
  const { fields } = useEntityOptions(entity)

  const cols = useMemo(() => {
    // pick first 6 readable fields
    const preferred = ['id', 'name', 'code', 'item_code', 'status', 'amount', 'price', 'quantity', 'active']
    const byPref = preferred.filter((p) => fields.includes(p))
    const rest = fields.filter((f) => !byPref.includes(f)).slice(0, Math.max(0, 6 - byPref.length))
    return [...byPref, ...rest]
  }, [fields])

  const handleDelete = async (row: any) => {
    const id = row?.id
    if (!id) return
    await fetchEntityData(entity, 'delete', undefined, id)
    // soft refresh: just let useEntityList re-run by toggling tab
    setTab((t) => (t === 'all' ? 'recent' : 'all'))
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="capitalize">{entity} list</CardTitle>
          <Tabs value={tab} onValueChange={(v) => setTab(v as any)}>
            <TabsList>
              <TabsTrigger value="all">All</TabsTrigger>
              <TabsTrigger value="active">Active</TabsTrigger>
              <TabsTrigger value="inactive">Inactive</TabsTrigger>
              <TabsTrigger value="recent">Recent</TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      </CardHeader>

      <CardContent className="max-h-[55dvh] overflow-auto">
        {loading ? (
          <div className="p-6 text-sm text-muted-foreground">Loading…</div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                {cols.map((c) => (
                  <TableHead key={c} className="capitalize">{c.replaceAll('_', ' ')}</TableHead>
                ))}
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {rows.map((r, i) => (
                <TableRow key={r.id ?? i} className="cursor-pointer hover:bg-muted/50" onClick={() => onSelectRow?.(r)}>
                  {cols.map((c) => (
                    <TableCell key={c}>
                      {formatCell(r[c])}
                    </TableCell>
                  ))}
                  <TableCell className="text-right">
                    <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); onSelectRow?.(r) }}>Edit</Button>
                    <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); handleDelete(r) }}>Delete</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  )
}

function formatCell(v: any) {
  if (v === null || v === undefined) return ''
  if (typeof v === 'boolean') return v ? 'Yes' : 'No'
  if (typeof v === 'string' && /^\d{4}-\d{2}-\d{2}/.test(v)) return v.slice(0, 10)
  return String(v)
}
