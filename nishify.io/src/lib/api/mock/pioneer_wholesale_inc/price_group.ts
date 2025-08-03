export const price_group = {
  options: () => ['id', 'name', 'markup_percent'],
  get: () => [{'id': 4770, 'markup_percent': 1513.34, 'name': 'full'}, {'id': 5034, 'markup_percent': 5653.3, 'name': 'again'}, {'id': 8232, 'markup_percent': 9500.44, 'name': 'space'}, {'id': 9605, 'markup_percent': 8268.94, 'name': 'question'}, {'id': 2023, 'markup_percent': 4319.93, 'name': 'understand'}],
  getOne: (id) => [{'id': 4770, 'markup_percent': 1513.34, 'name': 'full'}, {'id': 5034, 'markup_percent': 5653.3, 'name': 'again'}, {'id': 8232, 'markup_percent': 9500.44, 'name': 'space'}, {'id': 9605, 'markup_percent': 8268.94, 'name': 'question'}, {'id': 2023, 'markup_percent': 4319.93, 'name': 'understand'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};