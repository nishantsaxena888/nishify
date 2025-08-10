// src/components/admin/hooks.ts
'use client'
import { useEffect, useMemo, useState } from 'react'
import { fetchEntityData } from '../../lib/api'

export function inferType(field: string): 'number'|'bool'|'date'|'fk'|'string' {
  const f = field.toLowerCase()
  if (f.endsWith('_id')) return 'fk'
  if (/(^is_|^has_|active$)/.test(f)) return 'bool'
  if (/(^qty$|quantity|amount|price|total|limit|boro)/.test(f)) return 'number'
  if (/(date|_at$)/.test(f)) return 'date'
  return 'string'
}

export function useEntityOptions(entity: string) {
  const [fields, setFields] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let alive = true
    setLoading(true)
    fetchEntityData(entity, 'options')
      .then((res) => alive && setFields(res ?? []))
      .catch((e) => alive && setError(String(e?.message || e)))
      .finally(() => alive && setLoading(false))
    return () => { alive = false }
  }, [entity])

  const schema = useMemo(
    () => fields.map((name) => ({ name, kind: inferType(name) })),
    [fields]
  )

  return { fields, schema, loading, error }
}

export function useEntityList(entity: string, tab: string) {
  const [rows, setRows] = useState<Record<string, any>[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let alive = true
    setLoading(true)
    fetchEntityData(entity, 'get')
      .then((res) => {
        if (!alive) return
        let data = Array.isArray(res) ? res : []
        // built-in tabs: All / Active / Inactive / Recent(30d if *_at/date exists)
        if (tab === 'active') data = data.filter((r) => r.active === true)
        if (tab === 'inactive') data = data.filter((r) => r.active === false)
        if (tab === 'recent') {
          const now = Date.now()
          data = data.filter((r) => {
            const k = Object.keys(r).find((kk) => /date|_at$/i.test(kk))
            if (!k) return false
            const t = Date.parse(r[k])
            return Number.isFinite(t) && now - t < 30 * 864e5
          })
        }
        setRows(data)
      })
      .finally(() => alive && setLoading(false))
    return () => { alive = false }
  }, [entity, tab])

  return { rows, loading }
}
