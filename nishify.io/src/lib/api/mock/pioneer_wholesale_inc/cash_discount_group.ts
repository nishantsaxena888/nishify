export const cash_discount_group = {
  options: () => ['id', 'name', 'discount_percent', 'terms'],
  get: () => [{'id': 1, 'name': '5% Net 15', 'discount_percent': 5.0, 'terms': 'Net 15 days'}],
  getOne: (id) => [{'id': 1, 'name': '5% Net 15', 'discount_percent': 5.0, 'terms': 'Net 15 days'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};