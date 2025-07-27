export const productMockOptions = {
  fields: [
    { name: 'title', type: 'text', required: true },
    { name: 'description', type: 'textarea' },
    { name: 'price', type: 'number', required: true },
    { name: 'available', type: 'checkbox', label: 'In Stock' },
  ],
  layout: ['title', 'description', 'price', 'available'],
  pagination: true,
};