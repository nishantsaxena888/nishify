export const price_group = {
  options: () => ['id', 'name', 'markup_percent'],
  get: () => [{'id': 1, 'name': 'Retail Pricing', 'markup_percent': 12.5}],
  getOne: (id) => [{'id': 1, 'name': 'Retail Pricing', 'markup_percent': 12.5}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};