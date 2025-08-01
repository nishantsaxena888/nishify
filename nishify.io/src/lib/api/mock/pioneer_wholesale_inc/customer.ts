export const customer = {
  options: () => ['id', 'name', 'email'],
  get: () => [{'id': 1, 'name': 'Alice Corp', 'email': 'alice@example.com'}, {'id': 2, 'name': 'Beta LLC', 'email': 'beta@example.com'}],
  getOne: (id) => [{'id': 1, 'name': 'Alice Corp', 'email': 'alice@example.com'}, {'id': 2, 'name': 'Beta LLC', 'email': 'beta@example.com'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};