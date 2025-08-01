export const USE_MOCK = true; // Set to false in prod

export const MOCK_BEHAVIOR: Record<string, ('options' | 'get' | 'post' | 'update' | 'getOne')[]> = {
  products: ['options', 'get', 'post', 'update'],
  inventory: ['options'],
};

export const BASE_URL = "http://localhost:8000/api";
