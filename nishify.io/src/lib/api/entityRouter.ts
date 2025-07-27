import { USE_MOCK } from './config'

export function shouldUseMock(entity: string, operation: 'options' | 'get' | 'post' | 'update' | 'getOne') {
  if (USE_MOCK) return true;

  // Fine-grained logic:
  const mockMap = {
    inventory: ['options'],
    products: ['options', 'get'],
  };

  return mockMap[entity]?.includes(operation) ?? false;
}
