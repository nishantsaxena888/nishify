export const item = {
  options: () => ['id', 'item_code', 'name', 'category_id', 'secondary_category_id', 'vendor_id', 'tax_group_id', 'price_group_id', 'cash_discount_group_id', 'upc_code', 'unit', 'price', 'description', 'active'],
  get: () => [{'id': 1, 'item_code': 'COKE500', 'name': 'Coke 500ml', 'price': 1.25}],
  getOne: (id) => [{'id': 1, 'item_code': 'COKE500', 'name': 'Coke 500ml', 'price': 1.25}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};