export const secondary_category = {
  options: () => ['id', 'name', 'description'],
  get: () => [{'id': 1, 'name': 'Energy Drinks', 'description': 'Boost, Red Bull'}],
  getOne: (id) => [{'id': 1, 'name': 'Energy Drinks', 'description': 'Boost, Red Bull'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};