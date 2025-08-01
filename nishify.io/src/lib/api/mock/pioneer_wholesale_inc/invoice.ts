export const invoice = {
  options: () => ['id', 'customer_id', 'date'],
  get: () => [{'id': 1, 'customer_id': 1, 'date': '2024-08-01T10:00:00'}, {'id': 2, 'customer_id': 2, 'date': '2024-08-02T11:00:00'}],
  getOne: (id) => [{'id': 1, 'customer_id': 1, 'date': '2024-08-01T10:00:00'}, {'id': 2, 'customer_id': 2, 'date': '2024-08-02T11:00:00'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};