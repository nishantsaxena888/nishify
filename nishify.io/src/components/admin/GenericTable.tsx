'use client'
import { useEffect, useMemo, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useEntityOptions } from './hooks'
import { fetchEntityData } from '@/lib/api'

type Props = {
  entity: string
  onSelectRow?: (row: Record<string, any>) => void
  refreshKey?: number
}

type Row = Record<string, any>

export default function GenericTable({ entity, onSelectRow, refreshKey }: Props) {
  const [tab, setTab] = useState<'all'|'active'|'inactive'|'recent'>('all')
  const [rows, setRows] = useState<Row[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string| null>(null)

  // table state
  const [globalSearch, setGlobalSearch] = useState('')
  const [columnFilters, setColumnFilters] = useState<Record<string, string>>({})
  const [sortBy, setSortBy] = useState<string | null>(null)
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('asc')
  const [page, setPage] = useState(1)

  const { schema, admin } = useEntityOptions(entity)
  const pageSize = admin?.table?.page_size ?? 20

  const cols = useMemo(() => {
    const preferred = ['id', 'name', 'code', 'item_code', 'status', 'amount', 'price', 'quantity', 'active']
    const names = schema.map(f => f.name)
    const byPref = preferred.filter((p) => names.includes(p))
    const rest = names.filter((f) => !byPref.includes(f))
    return [...byPref, ...rest]
  }, [schema])

  async function loadList() {
    setLoading(true)
    setError(null)
    try {
      const data = await fetchEntityData(entity, 'get')
      let list: Record<string, any>[] = Array.isArray(data) ? data : (Array.isArray(data?.items) ? data.items : [])

      if (tab === 'active') list = list.filter((r) => r.active === true)
      if (tab === 'inactive') list = list.filter((r) => r.active === false)
      if (tab === 'recent') {
        const now = Date.now()
        list = list.filter((r: any) => {
          const k = Object.keys(r).find(k => /date|_at$/i.test(k))
          if (!k) return false
          const t = Date.parse(String(r[k]))
          return Number.isFinite(t) && now - t < 30 * 864e5
        })
      }

      setRows(list)
    } catch (e: any) {
      setError(String(e?.message || e))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadList() }, [entity, tab, refreshKey])

  const paginatedRows = useMemo(() => {
    const start = (page - 1) * pageSize
    return rows.slice(start, start + pageSize)
  }, [rows, page, pageSize])

  const handleDelete = async (row: any) => {
    if (admin?.table?.delete_confirmation) {
      if (!confirm(`Delete record ${row.id}?`))
        return
    }
    await fetchEntityData(entity, 'delete', row.id)
    await loadList()
  }

  // filtering + sorting
  const processed = useMemo(() => {
    let list = [...rows]

    // global search
    if (admin?.table?.global_search && globalSearch.trim()) {
      const term = globalSearch.toLowerCase()
      list = list.filter(row =>
        Object.values(row).some(val => String(val).toLowerCase().includes(term))
      )
    }

    // column search
    if (admin?.table?.column_search) {
      Object.entries(columnFilters).forEach(([col, val]) => {
        if (val?.trim()) {
          const term = val.toLowerCase()
          list = list.filter(row => String(row[col] ?? '').toLowerCase().includes(term))
        }
      })
    }

    // sorting
    if (admin?.table?.sortable && sortBy) {
      list.sort((a, b) => {
        const av = a[sortBy!]
        const bv = b[sortBy!]
        const na = av == null ? '' : String(av).toLowerCase()
        const nb = bv == null ? '' : String(bv).toLowerCase()
        if (na < nb) return sortDir === 'asc' ? -1 : 1
        if (na > nb) return sortDir === 'asc' ? 1 : -1
        return 0
      })
    }

    return list
  }, [rows, admin?.table, globalSearch, columnFilters, sortBy, sortDir])

  useEffect(() => { setPage(1) }, [globalSearch, JSON.stringify(columnFilters), sortBy, sortDir, entity])

  const headerLabel = (k: string) => k.replace(/_/g, ' ')
  const totalPages = Math.max(1, Math.ceil(processed.length / pageSize))

  const visibleRows = useMemo(() => {
    const start = (page - 1) * pageSize
    return processed.slice(start, start + pageSize)
  }, [processed, page, pageSize])

  return (
    <Card className="w-full">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="capitalize">{entity}</CardTitle>

        <Tabs value={tab} onValueChange={(v) => setTab(v as any)}>
          <TabsList>
            <TabsTrigger value="all">All</TabsTrigger>
            <TabsTrigger value="active">Active</TabsTrigger>
            <TabsTrigger value="inactive">Inactive</TabsTrigger>
            <TabsTrigger value="recent">Recent</TabsTrigger>
          </TabsList>
        </Tabs>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* Global Search */}
        {admin?.table?.global_search && (
          <div className="max-w-sm">
            <Input
              placeholder="Search..."
              value={globalSearch}
              onChange={(e) => setGlobalSearch(e.target.value)}
            />
          </div>
        )}

        <div className="rounded-md border max-h-[55dvh] overflow-auto">
          <Table>
            <TableHeader className={admin?.table?.sticky_header ? 'sticky top-0 z-10 bg-background shadow-sm' : ''}>
              <TableRow>
                {cols.map((c) => (
                  <TableHead
                    key={String(c)}
                    className="capitalize cursor-pointer select-none"
                    onClick={() => {
                      if (!admin?.table?.sortable) return
                      if (sortBy === c) {
                        setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'))
                      } else {
                        setSortBy(String(c))
                        setSortDir('asc')
                      }
                    }}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span>{headerLabel(String(c))}</span>
                      {admin?.table?.sortable && sortBy === c && (
                        <span className="text-xs">{sortDir === 'asc' ? '▲' : '▼'}</span>
                      )}
                    </div>
                    {/* Column search inputs */}
                    {admin?.table?.column_search && (
                      <div className="mt-1">
                        <Input
                          value={columnFilters[String(c)] ?? ''}
                          onChange={(e) =>
                            setColumnFilters((m) => ({ ...m, [String(c)]: e.target.value }))
                          }
                          placeholder="Filter..."
                          className="h-8"
                        />
                      </div>
                    )}
                  </TableHead>
                ))}
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>

            <TableBody>
              {loading && (
                <TableRow><TableCell colSpan={cols.length + 1} className="text-sm text-muted-foreground">Loading…</TableCell></TableRow>
              )}
              {error && !loading && (
                <TableRow><TableCell colSpan={cols.length + 1} className="text-sm text-red-500">{error}</TableCell></TableRow>
              )}
              {!loading && !error && visibleRows.length === 0 && (
                <TableRow><TableCell colSpan={cols.length + 1} className="text-sm text-muted-foreground">No records.</TableCell></TableRow>
              )}
              {!loading && !error && visibleRows.map((r, i) => (
                <TableRow key={r.id ?? i} className="cursor-pointer hover:bg-muted/50" onClick={() => onSelectRow?.(r)}>
                  {cols.map((c) => (
                    <TableCell key={c}>{formatCell(r[c])}</TableCell>
                  ))}
                  <TableCell className="text-right">
                    <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); onSelectRow?.(r) }}>Edit</Button>
                    <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); handleDelete(r) }}>Delete</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between pt-2">
          <div className="text-sm text-muted-foreground">
            Page {page} / {totalPages} • {processed.length} rows
          </div>
          <div className="space-x-2">
            <Button variant="outline" size="sm" onClick={() => setPage(1)} disabled={page === 1}>« First</Button>
            <Button variant="outline" size="sm" onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>‹ Prev</Button>
            <Button variant="outline" size="sm" onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page === totalPages}>Next ›</Button>
            <Button variant="outline" size="sm" onClick={() => setPage(totalPages)} disabled={page === totalPages}>Last »</Button>
          </div>
        </div>
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
