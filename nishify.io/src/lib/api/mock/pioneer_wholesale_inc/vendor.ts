export const vendor = {
  options: () => ['id', 'name', 'address', 'email', 'phone', 'contact_person'],
  get: () => [{'id': 1, 'name': 'Coca-Cola Co.', 'phone': '1234567890'}],
  getOne: (id) => [{'id': 1, 'name': 'Coca-Cola Co.', 'phone': '1234567890'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};