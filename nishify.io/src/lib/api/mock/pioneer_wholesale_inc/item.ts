export const item = {
  options: () => ['id', 'name', 'price', 'vendor_id'],
  get: () => [{'id': 1, 'name': 'Widget', 'price': 10.5, 'vendor_id': 1}, {'id': 2, 'name': 'Gadget', 'price': 5.75, 'vendor_id': 2}],
  getOne: (id) => [{'id': 1, 'name': 'Widget', 'price': 10.5, 'vendor_id': 1}, {'id': 2, 'name': 'Gadget', 'price': 5.75, 'vendor_id': 2}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};