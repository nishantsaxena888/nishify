export const vendor = {
  options: () => ['id', 'name'],
  get: () => [{'id': 1, 'name': 'Vendor A'}, {'id': 2, 'name': 'Vendor B'}],
  getOne: (id) => [{'id': 1, 'name': 'Vendor A'}, {'id': 2, 'name': 'Vendor B'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};