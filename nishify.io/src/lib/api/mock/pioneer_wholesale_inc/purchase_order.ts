export const purchase_order = {
  options: () => ['id', 'vendor_id', 'date', 'status'],
  get: () => [{'id': 1, 'vendor_id': 1, 'date': '2024-07-01T10:00:00', 'status': 'Submitted'}],
  getOne: (id) => [{'id': 1, 'vendor_id': 1, 'date': '2024-07-01T10:00:00', 'status': 'Submitted'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};