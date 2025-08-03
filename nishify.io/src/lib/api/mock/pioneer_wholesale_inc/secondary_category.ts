export const secondary_category = {
  options: () => ['id', 'name', 'description'],
  get: () => [{'description': 'other', 'id': 3288, 'name': 'property'}, {'description': 'hot', 'id': 402, 'name': 'firm'}, {'description': 'because', 'id': 8182, 'name': 'girl'}, {'description': 'cell', 'id': 5712, 'name': 'artist'}, {'description': 'decade', 'id': 2471, 'name': 'support'}],
  getOne: (id) => [{'description': 'other', 'id': 3288, 'name': 'property'}, {'description': 'hot', 'id': 402, 'name': 'firm'}, {'description': 'because', 'id': 8182, 'name': 'girl'}, {'description': 'cell', 'id': 5712, 'name': 'artist'}, {'description': 'decade', 'id': 2471, 'name': 'support'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};