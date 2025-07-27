import { BASE_URL } from './config';
import { shouldUseMock } from './entityRouter';
import { mocks } from './mock';

export async function fetchEntityData(entity: string, operation: 'options' | 'get' | 'getOne' | 'post' | 'update') {
  if (shouldUseMock(entity, operation)) {
    return mocks[entity]?.[operation];
  }

  const url = `${BASE_URL}/entity/${entity}/${operation}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch ${entity} ${operation}`);
  return res.json();
}
