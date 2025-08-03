export const cash_discount_group = {
  options: () => ['id', 'name', 'discount_percent', 'terms'],
  get: () => [{'discount_percent': 5478.38, 'id': 4747, 'name': 'important', 'terms': 'contain'}, {'discount_percent': 5602.62, 'id': 2865, 'name': 'a', 'terms': 'care'}, {'discount_percent': 821.55, 'id': 3070, 'name': 'seem', 'terms': 'through'}, {'discount_percent': 2347.69, 'id': 9882, 'name': 'same', 'terms': 'prove'}, {'discount_percent': 5935.58, 'id': 577, 'name': 'also', 'terms': 'group'}],
  getOne: (id) => [{'discount_percent': 5478.38, 'id': 4747, 'name': 'important', 'terms': 'contain'}, {'discount_percent': 5602.62, 'id': 2865, 'name': 'a', 'terms': 'care'}, {'discount_percent': 821.55, 'id': 3070, 'name': 'seem', 'terms': 'through'}, {'discount_percent': 2347.69, 'id': 9882, 'name': 'same', 'terms': 'prove'}, {'discount_percent': 5935.58, 'id': 577, 'name': 'also', 'terms': 'group'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};