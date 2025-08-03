export const salesperson = {
  options: () => ['id', 'name', 'email', 'phone'],
  get: () => [{'email': 'type', 'id': 9150, 'name': 'drug', 'phone': 'behavior'}, {'email': 'bar', 'id': 1734, 'name': 'clearly', 'phone': 'safe'}, {'email': 'least', 'id': 4312, 'name': 'better', 'phone': 'if'}, {'email': 'security', 'id': 1438, 'name': 'ability', 'phone': 'available'}, {'email': 'raise', 'id': 2028, 'name': 'better', 'phone': 'generation'}],
  getOne: (id) => [{'email': 'type', 'id': 9150, 'name': 'drug', 'phone': 'behavior'}, {'email': 'bar', 'id': 1734, 'name': 'clearly', 'phone': 'safe'}, {'email': 'least', 'id': 4312, 'name': 'better', 'phone': 'if'}, {'email': 'security', 'id': 1438, 'name': 'ability', 'phone': 'available'}, {'email': 'raise', 'id': 2028, 'name': 'better', 'phone': 'generation'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};