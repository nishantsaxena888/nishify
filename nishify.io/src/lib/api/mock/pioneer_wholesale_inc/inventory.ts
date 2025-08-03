export const inventory = {
  options: () => ['id', 'item_id', 'location_id', 'quantity'],
  get: () => [{'id': 313, 'item_id': 1610, 'location_id': 6076, 'quantity': 5379}, {'id': 8065, 'item_id': 2452, 'location_id': 9277, 'quantity': 7887}, {'id': 3635, 'item_id': 8795, 'location_id': 8248, 'quantity': 8345}, {'id': 2520, 'item_id': 9326, 'location_id': 7581, 'quantity': 8701}, {'id': 9009, 'item_id': 3483, 'location_id': 4010, 'quantity': 2455}],
  getOne: (id) => [{'id': 313, 'item_id': 1610, 'location_id': 6076, 'quantity': 5379}, {'id': 8065, 'item_id': 2452, 'location_id': 9277, 'quantity': 7887}, {'id': 3635, 'item_id': 8795, 'location_id': 8248, 'quantity': 8345}, {'id': 2520, 'item_id': 9326, 'location_id': 7581, 'quantity': 8701}, {'id': 9009, 'item_id': 3483, 'location_id': 4010, 'quantity': 2455}][0],
  post: (payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) }),
  update: (payload) => payload,
};