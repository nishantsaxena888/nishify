export const inventory_location = {
  options: () => ['id', 'name', 'address'],
  get: () => [{'id': 1, 'name': 'Warehouse A'}],
  getOne: (id) => [{'id': 1, 'name': 'Warehouse A'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};