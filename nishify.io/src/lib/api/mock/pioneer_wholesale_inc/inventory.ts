export const inventory = {
  options: () => ['id', 'item_id', 'location_id', 'quantity'],
  get: () => [{'id': 1, 'item_id': 1, 'location_id': 1, 'quantity': 150}],
  getOne: (id) => [{'id': 1, 'item_id': 1, 'location_id': 1, 'quantity': 150}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};