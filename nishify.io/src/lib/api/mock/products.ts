const fields = [
  { name: "id", type: "text" },
  { name: "name", type: "text" },
  { name: "price", type: "number" },
];

let records = [
  { id: "p1", name: "Phone", price: 800 },
  { id: "p2", name: "Laptop", price: 1200 },
];

export default {
  options: () => ({ fields }),     // ✅ fixed

  get: () => records,

  getOne: ({ id }: any) => records.find((r) => r.id === id) || null,

  post: (data: any) => {
    const newItem = { id: `id-${Date.now()}`, ...data };
    records.push(newItem);
    return newItem;
  },

  update: (data: any) => {
    const i = records.findIndex((r) => r.id === data.id);
    if (i === -1) return null;
    records[i] = { ...records[i], ...data };
    return records[i];
  }
};
