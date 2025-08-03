export const item_category = {
  options: () => ['id', 'name', 'description'],
  get: () => [{'id': 1, 'name': 'Beverages', 'description': 'Cold drinks and juices'}],
  getOne: (id) => [{'id': 1, 'name': 'Beverages', 'description': 'Cold drinks and juices'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};