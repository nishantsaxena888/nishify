export const item_category = {
  options: () => ['id', 'name', 'description'],
  get: () => [{'description': 'skill', 'id': 8100, 'name': 'bed'}, {'description': 'late', 'id': 8027, 'name': 'send'}, {'description': 'anyone', 'id': 8212, 'name': 'population'}, {'description': 'executive', 'id': 9131, 'name': 'simply'}, {'description': 'clear', 'id': 6971, 'name': 'provide'}],
  getOne: (id) => [{'description': 'skill', 'id': 8100, 'name': 'bed'}, {'description': 'late', 'id': 8027, 'name': 'send'}, {'description': 'anyone', 'id': 8212, 'name': 'population'}, {'description': 'executive', 'id': 9131, 'name': 'simply'}, {'description': 'clear', 'id': 6971, 'name': 'provide'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};