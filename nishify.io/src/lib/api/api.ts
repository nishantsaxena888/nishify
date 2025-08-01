import { BASE_URL } from "./config";
import { shouldUseMock } from "./entityRouter";

async function loadMock(entity: string) {
  try {
    const mod = await import(`./mock/${entity}.ts`);
    return mod.default;
  } catch (e) {
    console.warn(`Mock not found for entity: ${entity}`);
    return null;
  }
}

export async function fetchEntityData(
  entity: string,
  operation: 'options' | 'get' | 'getOne' | 'post' | 'update',
  payload?: any,
  forceMock = false
) {
  if (forceMock || shouldUseMock(entity, operation)) {
    const mock = await loadMock(entity);
    if (!mock || !mock[operation]) throw new Error(`Mock not implemented for ${entity} ${operation}`);
    return mock[operation](payload);
  }

  const url = `${BASE_URL}/entity/${entity}/${operation}`;
  const method = ['post', 'update', 'getOne'].includes(operation) ? 'POST' : 'GET';

  const options: RequestInit = {
    method,
    headers: { 'Content-Type': 'application/json' },
    ...(method === 'POST' && payload ? { body: JSON.stringify(payload) } : {}),
  };

  const res = await fetch(url, options);
  if (!res.ok) throw new Error(`API failed: ${res.status}`);
  return res.json();
}
