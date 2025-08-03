export const salesperson = {
  options: () => ['id', 'name', 'email', 'phone'],
  get: () => [{'id': 1, 'name': 'Ravi', 'email': 'ravi@jnq.com'}],
  getOne: (id) => [{'id': 1, 'name': 'Ravi', 'email': 'ravi@jnq.com'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};