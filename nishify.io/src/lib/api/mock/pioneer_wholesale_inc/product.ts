export const product = {
  options: () => ['id', 'name', 'price', 'in_stock'],
  get: () => [{'id': 1, 'name': 'Sample Product', 'price': 9.99, 'in_stock': True}],
  getOne: (id) => [{'id': 1, 'name': 'Sample Product', 'price': 9.99, 'in_stock': True}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};