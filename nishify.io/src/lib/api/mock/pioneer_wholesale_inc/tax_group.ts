export const tax_group = {
  options: () => ['id', 'name', 'tax_percent'],
  get: () => [{'id': 3319, 'name': 'southern', 'tax_percent': 701.95}, {'id': 646, 'name': 'country', 'tax_percent': 7501.0}, {'id': 8103, 'name': 'food', 'tax_percent': 170.41}, {'id': 9283, 'name': 'value', 'tax_percent': 9023.69}, {'id': 2526, 'name': 'able', 'tax_percent': 8375.47}],
  getOne: (id) => [{'id': 3319, 'name': 'southern', 'tax_percent': 701.95}, {'id': 646, 'name': 'country', 'tax_percent': 7501.0}, {'id': 8103, 'name': 'food', 'tax_percent': 170.41}, {'id': 9283, 'name': 'value', 'tax_percent': 9023.69}, {'id': 2526, 'name': 'able', 'tax_percent': 8375.47}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};