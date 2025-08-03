export const invoice_item = {
  options: () => ['invoice_id', 'item_id', 'quantity', 'price'],
  get: () => [{'invoice_id': 1, 'item_id': 1, 'quantity': 5, 'price': 1.25}],
  getOne: (id) => [{'invoice_id': 1, 'item_id': 1, 'quantity': 5, 'price': 1.25}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};