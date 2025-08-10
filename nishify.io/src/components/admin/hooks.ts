'use client'
import { useEffect, useMemo, useState } from 'react'
import { fetchEntityData } from '@/lib/api'

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
    fetchEntityData(entity, 'options') // should call .../options?schema=full
      .then((res: any) => {
        if (!alive) return

        let names: string[] = []

        // full schema: { fields: [{name:...}, ...] }
        if (res && Array.isArray(res.fields)) {
          names = res.fields
            .map((f: any) => (typeof f === 'string' ? f : f?.name))
            .filter(Boolean)
        }
        // some older shape: { schema: [{name:...}] }
        else if (res && Array.isArray(res.schema)) {
          names = res.schema
            .map((s: any) => (typeof s === 'string' ? s : s?.name))
            .filter(Boolean)
        }
        // minimal array: ["id", "name", ...]
        else if (Array.isArray(res)) {
          names = res as string[]
        }

        setFields(names)
      })
      .catch((e: any) => alive && setError(String(e?.message ?? e)))
      .finally(() => alive && setLoading(false))

    return () => { alive = false }
  }, [entity])

  const schema = useMemo(
    () => fields.map((name) => ({ name, kind: inferType(name) })),
    [fields]
  )

  return { fields, schema, loading, error }
}
