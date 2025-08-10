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

// ---- Helpers ----------------------------------------------------------------
async function httpJson(url: string, init?: RequestInit) {
  const res = await fetch(url, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${init?.method || "GET"} ${url} -> ${res.status} ${text}`);
  }
  return res.status === 204 ? null : res.json();
}

function inferSchemaFromRow(row: Record<string, any>) {
  return Object.keys(row || {}).map((name) => {
    const v = row[name];
    let kind: "text" | "number" | "bool" | "date" = "text";
    if (typeof v === "number") kind = "number";
    else if (typeof v === "boolean") kind = "bool";
    else if (typeof v === "string" && /^\d{4}-\d{2}-\d{2}/.test(v)) kind = "date";
    return { name, kind };
  });
}

const MOCK_ALIASES: Record<string, string[]> = {
  get: ["list"],
  update: ["put"],
  delete: ["remove", "del"],
  options: ["schema"],
  getOne: ["getById"],
};

type Operation = "options" | "get" | "getOne" | "post" | "update" | "delete" | "put";

// ---- Main Fetch --------------------------------------------------------------
export async function fetchEntityData(entity: string, operation: Operation, payload?: any) {
  const op: Exclude<Operation, "put"> = operation === "put" ? "update" : operation;

  if (USE_MOCK) {
    const mock = await loadMock(entity);
    if (!mock) return callApiOp(entity, op, payload);

    let fn = typeof mock[op] === "function" ? mock[op] : undefined;
    if (!fn) {
      for (const alias of MOCK_ALIASES[op] || []) {
        if (typeof mock[alias] === "function") {
          fn = mock[alias];
          break;
        }
      }
    }

    if (!fn && op === "options") {
      if (Array.isArray(mock.schema)) {
        const fields = mock.schema.map((f: any) => f.name);
        return { schema: mock.schema, fields };
      }
      const listFn = typeof mock.get === "function" ? mock.get : mock.list;
      if (listFn) {
        const rows = await listFn();
        const schema = inferSchemaFromRow(rows[0] || {});
        return { schema, fields: schema.map((s) => s.name) };
      }
    }

    if (!fn && op === "get") fn = mock.get || mock.list;
    if (!fn && op === "getOne") fn = mock.getOne || mock.getById;

    if (fn) return fn(payload);

    return callApiOp(entity, op, payload);
  }

  return callApiOp(entity, op, payload);
}

// ---- API Calls ---------------------------------------------------------------
async function callApiOp(entity: string, operation: Exclude<Operation, "put">, payload?: any) {
  switch (operation) {
    case "options":
      return httpJson(`${API_BASE_URL}/${entity}/options?schema=full`);
    case "get":
      return httpJson(`${API_BASE_URL}/${entity}`);
    case "getOne":
      return httpJson(`${API_BASE_URL}/${entity}/${payload?.id ?? payload}`);
    case "post":
      return httpJson(`${API_BASE_URL}/${entity}`, { method: "POST", body: JSON.stringify(payload ?? {}) });
    case "update":
      if (payload?.id == null) throw new Error("update requires payload.id");
      return httpJson(`${API_BASE_URL}/${entity}/${payload.id}`, { method: "PUT", body: JSON.stringify(payload ?? {}) });
    case "delete":
      const id = payload?.id ?? payload;
      if (id == null) throw new Error("delete requires id");
      return httpJson(`${API_BASE_URL}/${entity}/${id}`, { method: "DELETE" });
    default:
      throw new Error(`Unknown operation: ${operation}`);
  }
}

// ---- Shortcuts ---------------------------------------------------------------
export const options = (entity: string) => fetchEntityData(entity, "options");
export const getList = (entity: string) => fetchEntityData(entity, "get");
export const getOne = (entity: string, id: number | string) => fetchEntityData(entity, "getOne", id);
export const create = (entity: string, payload: any) => fetchEntityData(entity, "post", payload);
export const update = (entity: string, payload: any) => fetchEntityData(entity, "update", payload);
export const remove = (entity: string, id: number | string) => fetchEntityData(entity, "delete", id);
