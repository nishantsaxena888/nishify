import { USE_MOCK } from "./config";
import { mockOptionModules } from "./mock/meta/registry";

export async function loadEntityOptions(entity: string) {
  if (USE_MOCK) {
    const mod = mockOptionModules[entity];
    if (!mod) {
      throw new Error(`Mock options not found for entity: ${entity}`);
    }
    return mod;
  }

  const res = await fetch(`/api/${entity}/options`);
  if (!res.ok) {
    throw new Error(`API error: ${res.statusText}`);
  }
  return await res.json();
}
