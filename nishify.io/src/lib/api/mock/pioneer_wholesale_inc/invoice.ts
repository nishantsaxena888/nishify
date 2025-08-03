export const invoice = {
  options: () => ['id', 'customer_id', 'date', 'status'],
  get: () => [{'id': 1, 'customer_id': 1, 'date': '2024-08-01T09:00:00', 'status': 'Draft'}],
  getOne: (id) => [{'id': 1, 'customer_id': 1, 'date': '2024-08-01T09:00:00', 'status': 'Draft'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};