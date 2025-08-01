import { USE_MOCK, MOCK_BEHAVIOR } from "./config";

export function shouldUseMock(
  entity: string,
  operation: 'options' | 'get' | 'getOne' | 'post' | 'update'
): boolean {
  if (MOCK_BEHAVIOR[entity]?.includes(operation)) return true;
  return USE_MOCK;
}
