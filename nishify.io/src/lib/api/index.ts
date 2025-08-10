/* eslint-disable @typescript-eslint/no-explicit-any */
// src/lib/api/index.ts
import { USE_MOCK, API_BASE_URL, CLIENT } from "./config";

// ---- Mock loader ------------------------------------------------------------
async function loadMock(entity: string): Promise<any | null> {
  try {
    const mod = await import(`@/clients/${CLIENT}/mock/${entity}.ts`);
    return (mod as any).default || (mod as any)[entity] || mod;
  } catch {
    try {
      const mod = await import(`@/lib/api/${entity}.ts`);
      return (mod as any).default || (mod as any)[entity] || mod;
    } catch {
      return null;
    }
  }
}

// ---- HTTP -------------------------------------------------------------------
async function httpJson(url: string, init?: RequestInit): Promise<any> {
  const resp = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...init,
  } as RequestInit);
  if (!resp.ok) {
    const txt = await resp.text().catch(() => "");
    throw new Error(`${resp.status} ${resp.statusText}: ${txt || url}`);
  }
  return resp.json();
}

// ---- Inferred schema --------------------------------------------------------
type SchemaField = { name: string; type?: string; label?: string; primary_key?: boolean };
function inferSchemaFromRow(row: any): SchemaField[] {
  const names = Object.keys(row || {});
  return names.map((n) => ({ name: n }));
}

// ---- Operation aliases ------------------------------------------------------
const MOCK_ALIASES: Record<
  "get" | "update" | "post" | "delete" | "options" | "getOne",
  string[]
> = {
  get: ["list", "fetch", "findAll"],
  update: ["put"],
  post: ["create", "add"],
  delete: ["remove", "del"],
  options: ["schema"],
  getOne: ["getById"],
};

// ---- Runtime fallback mock (always available) -------------------------------
type Row = Record<string, any>;
const __memStore: Record<string, Row[]> = Object.create(null);

function ensureEntityStore(entity: string) {
  if (!__memStore[entity]) {
    __memStore[entity] = [
      { id: 1, name: `${entity}-1` },
      { id: 2, name: `${entity}-2` },
      { id: 3, name: `${entity}-3` },
    ];
  }
}

function runtimeMock(entity: string) {
  ensureEntityStore(entity);
  return {
    async options(): Promise<string[]> {
      const row = __memStore[entity][0] || { id: 1, name: `${entity}-1` };
      return Object.keys(row);
    },
    async get(): Promise<Row[]> {
      return [...__memStore[entity]];
    },
    async getOne(id: number | string): Promise<Row> {
      const n = typeof id === "string" ? Number(id) : id;
      const row = __memStore[entity].find((r) => r.id === n);
      if (!row) throw new Error("Not found");
      return row;
    },
    async post(payload: Row): Promise<Row> {
      const arr = __memStore[entity];
      const id = Math.max(...arr.map((r) => Number(r.id) || 0), 0) + 1;
      const row = { id, ...payload };
      arr.push(row);
      return row;
    },
    async update(payload: Row): Promise<Row> {
      const arr = __memStore[entity];
      const idx = arr.findIndex((r) => r.id === payload.id);
      if (idx === -1) throw new Error("Not found");
      arr[idx] = { ...arr[idx], ...payload };
      return arr[idx];
    },
    async delete(id: number | string): Promise<{ success: true }> {
      const n = typeof id === "string" ? Number(id) : id;
      const arr = __memStore[entity];
      const idx = arr.findIndex((r) => r.id === n);
      if (idx !== -1) arr.splice(idx, 1);
      return { success: true };
    },
  };
}

// ---- Live API op ------------------------------------------------------------
async function callApiOp(entity: string, op: "options" | "get" | "getOne" | "post" | "update" | "delete", payload?: any) {
  switch (op) {
    case "options": {
      const full = await httpJson(`${API_BASE_URL}/${entity}/options?schema=full`).catch(() => null);
      if (full) return full;
      return httpJson(`${API_BASE_URL}/${entity}/options`);
    }
    case "get":
      return httpJson(`${API_BASE_URL}/${entity}`);
    case "getOne":
      return httpJson(`${API_BASE_URL}/${entity}/${payload?.id ?? payload}`);
    case "post":
      return httpJson(`${API_BASE_URL}/${entity}`, {
        method: "POST",
        body: JSON.stringify(payload ?? {}),
      });
    case "update":
      if (payload?.id == null) throw new Error("update requires payload.id");
      return httpJson(`${API_BASE_URL}/${entity}/${payload.id}`, {
        method: "PUT",
        body: JSON.stringify(payload ?? {}),
      });
    case "delete": {
      const id = payload?.id ?? payload;
      if (id == null) throw new Error("delete requires id");
      return httpJson(`${API_BASE_URL}/${entity}/${id}`, { method: "DELETE" });
    }
  }
}

// ---- Main Fetch (MOCK-FIRST with runtime fallback) --------------------------
export async function fetchEntityData(
  entity: string,
  op: "options" | "get" | "getOne" | "post" | "update" | "delete",
  payload?: any
): Promise<any> {
  if (USE_MOCK) {
    const perEntityMock = await loadMock(entity);
    const fallback = runtimeMock(entity);

    const mock = {
      options: perEntityMock?.options ?? fallback.options,
      get: perEntityMock?.get ?? perEntityMock?.list ?? fallback.get,
      getOne: perEntityMock?.getOne ?? perEntityMock?.getById ?? fallback.getOne,
      delete: perEntityMock?.delete ?? perEntityMock?.remove ?? fallback.delete,
      post: perEntityMock?.post ?? fallback.post,
      update:
        perEntityMock?.update ??
        (perEntityMock as any)?.put ??
        fallback.update,
    } as {
      options: () => Promise<string[] | { schema?: any[]; fields?: string[] }>;
      get: () => Promise<Row[]>;
      getOne: (id: number | string) => Promise<Row>;
      post: (payload: Row) => Promise<Row>;
      update: (payload: Row) => Promise<Row>;
    };

    switch (op) {
      case "options": {
        // Always return an ARRAY for tests
        const out = await mock.options();
        if (Array.isArray(out)) return out;
        if (out && Array.isArray((out as any).fields)) return (out as any).fields;
        // Infer from list as a last resort
        const rows = await mock.get();
        const schema = inferSchemaFromRow(rows[0] || {});
        return schema.map((s) => s.name);
      }
      case "get":
        return mock.get();
      case "getOne":
        return mock.getOne(payload?.id ?? payload);
      case "post":
        return mock.post(payload ?? {});
      case "update":
        if (payload?.id == null) throw new Error("update requires payload.id");
        return mock.update(payload);
      case "delete":
        return fallback.delete(payload?.id ?? payload);
    }
  }

  // LIVE API path
  return callApiOp(entity, op as any, payload);
}

// ---- Shortcuts ---------------------------------------------------------------
export const options = (entity: string) => fetchEntityData(entity, "options");
export const getList = (entity: string) => fetchEntityData(entity, "get");
export const getOne = (entity: string, id: number | string) =>
  fetchEntityData(entity, "getOne", id);
export const create = (entity: string, payload: any) =>
  fetchEntityData(entity, "post", payload);
export const update = (entity: string, payload: any) =>
  fetchEntityData(entity, "update", payload);
export const remove = (entity: string, id: number | string) =>
  fetchEntityData(entity, "delete", id);
