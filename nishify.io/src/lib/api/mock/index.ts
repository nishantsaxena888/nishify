import { USE_MOCK } from './config'

export async function loadEntityOptions(entity: string) {
  if (USE_MOCK) {
    try {
      const mod = await import(`../mock/meta/${entity}.options`)
      return mod.default || mod
    } catch (err) {
      throw new Error(`No mock options defined for entity: ${entity}`)
    }
  }

  const res = await fetch(`/api/${entity}/options`)
  if (!res.ok) throw new Error(`Failed to fetch options for ${entity}`)
  return res.json()
}
