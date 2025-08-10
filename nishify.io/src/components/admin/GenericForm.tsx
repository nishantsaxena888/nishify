// src/components/admin/GenericForm.tsx
'use client'
import { useEffect, useMemo, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { useEntityOptions } from './hooks'
import { fetchEntityData } from '@/lib/api'
import { DatePicker } from '@/components/ui/date-picker' // if you have one; else use Input type="date"

type Props = {
  entity: string
  value?: Record<string, any> | null
  onSaved?: () => void
  onCancel?: () => void
}

export default function GenericForm({ entity, value, onSaved, onCancel }: Props) {
  const { schema, loading, error } = useEntityOptions(entity)
  const [form, setForm] = useState<Record<string, any>>({})

  // initialize form for create/edit
  useEffect(() => {
    if (value) setForm(value)
    else {
      const blank: Record<string, any> = {}
      schema.forEach(({ name, kind }) => {
        if (name === 'id') return
        blank[name] = kind === 'bool' ? false : ''
      })
      setForm(blank)
    }
  }, [value, schema])

  const pk = useMemo(() => schema.find((f) => f.name === 'id'), [schema])
  const isEdit = Boolean(value && (value as any).id)

  const update = (k: string, v: any) => setForm((s) => ({ ...s, [k]: v }))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const payload = { ...form }
    // never send empty string for booleans
    schema.forEach(({ name, kind }) => {
      if (kind === 'bool' && payload[name] === '') payload[name] = false
    })
    if (isEdit && pk) {
      await fetchEntityData(entity, 'put', payload)
    } else {
      await fetchEntityData(entity, 'post', payload)
    }
    onSaved?.()
  }

  if (loading) return <Card><CardContent className="p-6">Loading form…</CardContent></Card>
  if (error) return <Card><CardContent className="p-6 text-red-500">{error}</CardContent></Card>

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg capitalize">
          {isEdit ? `Edit ${entity}` : `Create ${entity}`}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-3">
          {schema
            .filter((f) => f.name !== 'id')
            .map(({ name, kind }) => (
              <div key={name} className="flex flex-col gap-2">
                <Label className="capitalize">{name.replaceAll('_', ' ')}</Label>

                {kind === 'bool' ? (
                  <div className="flex items-center gap-2 py-2">
                    <Switch
                      checked={!!form[name]}
                      onCheckedChange={(v) => update(name, v)}
                    />
                    <span className="text-sm text-muted-foreground">{String(!!form[name])}</span>
                  </div>
                ) : kind === 'number' ? (
                  <Input
                    type="number"
                    value={form[name] ?? ''}
                    onChange={(e) => update(name, e.target.value === '' ? '' : Number(e.target.value))}
                  />
                ) : kind === 'date' ? (
                  // If you don’t have a DatePicker, fallback to native input
                  <Input
                    type="date"
                    value={form[name]?.slice(0, 10) ?? ''}
                    onChange={(e) => update(name, e.target.value)}
                  />
                ) : (
                  <Input
                    value={form[name] ?? ''}
                    onChange={(e) => update(name, e.target.value)}
                  />
                )}
              </div>
            ))}

          <div className="col-span-full flex gap-2 pt-2">
            <Button type="submit" className="w-28">Save</Button>
            <Button type="button" variant="outline" className="w-28" onClick={() => onCancel?.()}>
              Cancel
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
