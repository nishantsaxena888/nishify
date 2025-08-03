export const invoice_item = {
  options: () => ['invoice_id', 'item_id', 'quantity', 'price'],
  get: () => [{'invoice_id': 4740, 'item_id': 764, 'price': 981.69, 'quantity': 2597}, {'invoice_id': 7885, 'item_id': 7789, 'price': 1756.01, 'quantity': 6325}, {'invoice_id': 8797, 'item_id': 8804, 'price': 7522.97, 'quantity': 2338}, {'invoice_id': 8158, 'item_id': 5060, 'price': 2514.2, 'quantity': 6836}, {'invoice_id': 5073, 'item_id': 3441, 'price': 153.03, 'quantity': 3776}],
  getOne: (id) => [{'invoice_id': 4740, 'item_id': 764, 'price': 981.69, 'quantity': 2597}, {'invoice_id': 7885, 'item_id': 7789, 'price': 1756.01, 'quantity': 6325}, {'invoice_id': 8797, 'item_id': 8804, 'price': 7522.97, 'quantity': 2338}, {'invoice_id': 8158, 'item_id': 5060, 'price': 2514.2, 'quantity': 6836}, {'invoice_id': 5073, 'item_id': 3441, 'price': 153.03, 'quantity': 3776}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};