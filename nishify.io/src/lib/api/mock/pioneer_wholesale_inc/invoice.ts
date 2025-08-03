export const invoice = {
  options: () => ['id', 'customer_id', 'date', 'status'],
  get: () => [{'customer_id': 3919, 'date': '2025-04-05T10:46:03.390120', 'id': 1883, 'status': 'eat'}, {'customer_id': 3577, 'date': '2025-05-01T08:33:29.113025', 'id': 5536, 'status': 'no'}, {'customer_id': 7308, 'date': '2025-05-24T06:10:38.280398', 'id': 9710, 'status': 'treat'}, {'customer_id': 3763, 'date': '2025-06-25T14:55:45.067329', 'id': 4928, 'status': 'become'}, {'customer_id': 3326, 'date': '2025-05-13T15:32:57.519068', 'id': 4771, 'status': 'over'}],
  getOne: (id) => [{'customer_id': 3919, 'date': '2025-04-05T10:46:03.390120', 'id': 1883, 'status': 'eat'}, {'customer_id': 3577, 'date': '2025-05-01T08:33:29.113025', 'id': 5536, 'status': 'no'}, {'customer_id': 7308, 'date': '2025-05-24T06:10:38.280398', 'id': 9710, 'status': 'treat'}, {'customer_id': 3763, 'date': '2025-06-25T14:55:45.067329', 'id': 4928, 'status': 'become'}, {'customer_id': 3326, 'date': '2025-05-13T15:32:57.519068', 'id': 4771, 'status': 'over'}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};