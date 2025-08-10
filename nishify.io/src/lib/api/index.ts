// src/lib/api/index.ts
import { USE_MOCK, API_BASE_URL, CLIENT } from "./config";

// ---- Mock loader ------------------------------------------------------------
async function loadMock(entity: string): Promise<any | null> {
  try {
    const mod = await import(`@/clients/${CLIENT}/mock/${entity}.ts`);
    return (mod as any).default || (mod as any)[entity] || mod;
  } catch {
    return null;
  }
}

// ---- Direct fetch helper ----------------------------------------------------
async function callApi(path: string, options?: RequestInit) {
  const url = `${API_BASE_URL}/${path.replace(/^\/+/, "")}`;
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(`API failed: ${res.status}`);
  return res.json();
}

// ---- Single generic entry (what your hook is importing) ---------------------
export async function fetchEntityData(
  entity: string,
  operation: "options" | "get" | "getOne" | "post" | "update",
  payload?: any
) {
  if (USE_MOCK) {
    const mock = await loadMock(entity);
    if (!mock || typeof mock[operation] !== "function") {
      throw new Error(`Mock not implemented for ${entity} ${operation}`);
    }
    return mock[operation](payload);
  }

  // DIRECT mode
  switch (operation) {
    case "options":
      return callApi(`${entity}/options`);
    case "get":
      return callApi(entity);
    case "getOne": {
      const id = payload?.id ?? payload;
      return callApi(`${entity}/${id}`);
    }
    case "post":
      return callApi(entity, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload ?? {}),
      });
    case "update": {
      const id = payload?.id;
      if (id == null) throw new Error("update requires payload.id");
      return callApi(`${entity}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload ?? {}),
      });
    }
    default:
      throw new Error(`Unknown operation: ${operation as string}`);
  }
}

// ---- Convenience wrappers (optional, handy for UI code) ---------------------
export const options = (entity: string) =>
  fetchEntityData(entity, "options");
export const getList = (entity: string) =>
  fetchEntityData(entity, "get");
export const getOne = (entity: string, id: number | string) =>
  fetchEntityData(entity, "getOne", id);
export const create = (entity: string, payload: any) =>
  fetchEntityData(entity, "post", payload);
export const update = (entity: string, payload: any) =>
  fetchEntityData(entity, "update", payload);
