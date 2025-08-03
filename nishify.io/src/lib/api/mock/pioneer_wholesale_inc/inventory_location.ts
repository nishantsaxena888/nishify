export const inventory_location = {
  options: () => ['id', 'name', 'address'],
  get: () => [{'address': 'fight', 'id': 5313, 'name': 'send'}, {'address': 'expect', 'id': 2380, 'name': 'stop'}, {'address': 'thousand', 'id': 6512, 'name': 'past'}, {'address': 'budget', 'id': 5364, 'name': 'social'}, {'address': 'box', 'id': 1756, 'name': 'enter'}],
  getOne: (id) => [{'address': 'fight', 'id': 5313, 'name': 'send'}, {'address': 'expect', 'id': 2380, 'name': 'stop'}, {'address': 'thousand', 'id': 6512, 'name': 'past'}, {'address': 'budget', 'id': 5364, 'name': 'social'}, {'address': 'box', 'id': 1756, 'name': 'enter'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};