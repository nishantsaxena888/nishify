export const customer = {
  options: () => ['id', 'name', 'address', 'email', 'phone', 'salesperson_id', 'credit_limit'],
  get: () => [{'id': 1, 'name': 'Big Retailer Inc', 'phone': '9999999999'}],
  getOne: (id) => [{'id': 1, 'name': 'Big Retailer Inc', 'phone': '9999999999'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};