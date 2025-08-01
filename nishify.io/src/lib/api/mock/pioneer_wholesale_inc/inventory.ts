export const inventory = {
  options: () => ['id', 'item_id', 'quantity'],
  get: () => [{'id': 1, 'item_id': 1, 'quantity': 100}, {'id': 2, 'item_id': 2, 'quantity': 50}],
  getOne: (id) => [{'id': 1, 'item_id': 1, 'quantity': 100}, {'id': 2, 'item_id': 2, 'quantity': 50}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};