export const inventoryMockOptions = {
  fields: [
    { name: 'sku', type: 'text', required: true },
    { name: 'quantity', type: 'number' },
    { name: 'location', type: 'text' },
  ],
  layout: ['sku', 'quantity', 'location'],
};
