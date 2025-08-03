export const tax_group = {
  options: () => ['id', 'name', 'tax_percent'],
  get: () => [{'id': 1, 'name': 'Standard Tax', 'tax_percent': 7.5}],
  getOne: (id) => [{'id': 1, 'name': 'Standard Tax', 'tax_percent': 7.5}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};