// src/lib/api/mocks/runtime.ts
type Row = Record<string, any>;

const store: Record<string, Row[]> = Object.create(null);
const fieldsCache: Record<string, string[]> = Object.create(null);

function ensureEntity(entity: string) {
  if (!store[entity]) {
    store[entity] = [
      { id: 1, name: `${entity}-1` },
      { id: 2, name: `${entity}-2` },
      { id: 3, name: `${entity}-3` },
    ];
  }
}

function inferFields(entity: string): string[] {
  if (fieldsCache[entity]) return fieldsCache[entity];
  ensureEntity(entity);
  const rows = store[entity];
  const s = new Set<string>();
  for (const r of rows) Object.keys(r).forEach(k => s.add(k));
  const out = Array.from(s);
  fieldsCache[entity] = out.length ? out : ["id", "name"];
  return fieldsCache[entity];
}

export async function importMock(entity: string) {
  ensureEntity(entity);
  return {
    async options(): Promise<string[]> {
      return inferFields(entity);
    },
    async get(): Promise<Row[]> {
      return [...store[entity]];
    },
    async getOne(id: number | string): Promise<Row> {
      const n = typeof id === "string" ? Number(id) : id;
      return store[entity].find(r => (r.id ?? r.ID ?? r.Id) == n) ?? { id: n };
    },
    async post(payload: Row): Promise<Row> {
      const rows = store[entity];
      const max = rows.reduce((m, r) => Math.max(m, Number(r.id ?? 0)), 0) || 0;
      const created = { id: max + 1, ...payload };
      rows.push(created);
      fieldsCache[entity] = undefined as any;
      return created;
    },
    async update(payload: Row): Promise<Row> {
      const id = payload.id ?? payload.ID ?? payload.Id;
      if (id == null) throw new Error("update() requires payload.id");
      const rows = store[entity];
      const idx = rows.findIndex(r => (r.id ?? r.ID ?? r.Id) == id);
      if (idx === -1) {
        const created = { id, ...payload };
        rows.push(created);
        fieldsCache[entity] = undefined as any;
        return created;
      }
      const merged = { ...rows[idx], ...payload };
      rows[idx] = merged;
      fieldsCache[entity] = undefined as any;
      return merged;
    },
  };
}
