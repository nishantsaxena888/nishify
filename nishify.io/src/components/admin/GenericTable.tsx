// src/components/admin/GenericTable.tsx
'use client'
import { useEffect, useMemo, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { fetchEntityData } from '@/lib/api'

type Props = {
  entity: string
  onSelectRow?: (row: Record<string, any>) => void
  refreshKey?: number
}

type SchemaField = { name: string; kind?: string } | string

function toNameList(input: any): string[] {
  // full schema: { fields: [{name,...}] }
  if (input && Array.isArray(input.fields)) {
    return input.fields
      .map((f: any) => (typeof f === 'string' ? f : f?.name))
      .filter(Boolean)
  }
  // older shape: { schema: [{name,...}] }
  if (input && Array.isArray(input.schema)) {
    return input.schema
      .map((s: any) => (typeof s === 'string' ? s : s?.name))
      .filter(Boolean)
  }
  // minimal array: ["id", "name", ...]
  if (Array.isArray(input)) return input as string[]
  return []
}

export default function GenericTable({ entity, onSelectRow, refreshKey = 0 }: Props) {
  const [tab, setTab] = useState<'all'|'active'|'inactive'|'recent'>('all')
  const [rows, setRows] = useState<Record<string, any>[]>([])
  const [fields, setFields] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Load options (fields/schema)
  useEffect(() => {
    let alive = true
    ;(async () => {
      try {
        const res = await fetchEntityData(entity, 'options') // should be calling ?schema=full in the api layer
        if (!alive) return
        setFields(toNameList(res))
      } catch {
        setFields([])
      }
    })()
    return () => { alive = false }
  }, [entity])

  // Load list
  async function loadList() {
    setLoading(true)
    setError(null)
    try {
      const data = await fetchEntityData(entity, 'get')
      // support paginated { items, page, size, total } or raw array
      let list: Record<string, any>[] = Array.isArray(data) ? data : (Array.isArray(data?.items) ? data.items : [])

      if (tab === 'active')   list = list.filter(r => r.active === true)
      if (tab === 'inactive') list = list.filter(r => r.active === false)
      if (tab === 'recent') {
        const now = Date.now()
        list = list.filter((r) => {
          const k = Object.keys(r).find((kk) => /date|_at$/i.test(kk))
          if (!k) return false
          const t = Date.parse(r[k] as any)
          return Number.isFinite(t) && now - t < 30 * 864e5
        })
      }

      setRows(list)

      // If fields empty, infer from first row
      if ((!fields || fields.length === 0) && list.length > 0) {
        setFields(Object.keys(list[0]))
      }
    } catch (e: any) {
      setError(String(e?.message || e))
      setRows([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadList() }, [entity, tab])
  useEffect(() => { loadList() }, [refreshKey])

  const cols = useMemo(() => {
    if (!fields || fields.length === 0) return []
    const preferred = ['id', 'name', 'code', 'item_code', 'status', 'amount', 'price', 'quantity', 'active']
    const byPref = preferred.filter((p) => fields.includes(p))
    const rest = fields.filter((f) => !byPref.includes(f)).slice(0, Math.max(0, 6 - byPref.length))
    return [...byPref, ...rest]
  }, [fields])

  const handleDelete = async (row: any) => {
    const id = row?.id
    if (!id) return
    await fetchEntityData(entity, 'delete', id)
    await loadList()
  }

  const headerLabel = (c: unknown) =>
    String(c).replace(/_/g, ' ') // safer than .replaceAll and works for non-strings too

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
        ) : error ? (
          <div className="p-6 text-sm text-red-500">{error}</div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                {cols.map((c) => (
                  <TableHead key={String(c)} className="capitalize">
                    {headerLabel(c)}
                  </TableHead>
                ))}
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {rows.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={Math.max(1, cols.length + 1)} className="text-center text-sm text-muted-foreground">
                    No data found
                  </TableCell>
                </TableRow>
              ) : (
                rows.map((r, i) => (
                  <TableRow key={r.id ?? i} className="cursor-pointer hover:bg-muted/50" onClick={() => onSelectRow?.(r)}>
                    {cols.map((c) => (
                      <TableCell key={String(c)}>{formatCell(r[String(c)])}</TableCell>
                    ))}
                    <TableCell className="text-right">
                      <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); onSelectRow?.(r) }}>Edit</Button>
                      <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); handleDelete(r) }}>Delete</Button>
                    </TableCell>
                  </TableRow>
                ))
              )}
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
