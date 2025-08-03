export const purchase_order_item = {
  options: () => ['po_id', 'item_id', 'quantity', 'unit_price'],
  get: () => [{'po_id': 1, 'item_id': 1, 'quantity': 100, 'unit_price': 1.05}],
  getOne: (id) => [{'po_id': 1, 'item_id': 1, 'quantity': 100, 'unit_price': 1.05}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};