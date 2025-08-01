export const invoice_item = {
  options: () => ['invoice_id', 'item_id', 'quantity'],
  get: () => [{'invoice_id': 1, 'item_id': 1, 'quantity': 2}, {'invoice_id': 1, 'item_id': 2, 'quantity': 3}],
  getOne: (id) => [{'invoice_id': 1, 'item_id': 1, 'quantity': 2}, {'invoice_id': 1, 'item_id': 2, 'quantity': 3}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};