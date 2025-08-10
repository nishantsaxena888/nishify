// src/lib/api/api.ts

import { API_BASE_URL } from "./config";
import { shouldUseMock, Operation } from "./entityRouter";

const CLIENT = process.env.NEXT_PUBLIC_CLIENT_NAME || "pioneer_wholesale_inc";

/**
 * Try to load a mock module for the entity.
 * 1) client-scoped:  src/clients/<client>/mock/<entity>.ts
 * 2) common fallback: src/lib/api/mock/<entity>.ts
 *
 * The module can export:
 *  - default (function or object)
 *  - named export with the entity name
 *  - keys per operation (options/get/getOne/post/update)
 */
async function loadMock(entity: string) {
  try {
    const mod = await import(`@/clients/${CLIENT}/mock/${entity}.ts`);
    return (mod as any).default || (mod as any)[entity] || mod;
  } catch {
    // fall through
  }
  try {
    const mod = await import(`@/lib/api/${entity}.ts`);
    return (mod as any).default || (mod as any)[entity] || mod;
  } catch {
    return null;
  }
}

function buildUrl(entity: string, operation: Operation): string {
  const base = API_BASE_URL.replace(/\/+$/, "");
  const seg = `entity/${entity}/${operation}`;
  return `${base}/${seg}`;
}

export async function fetchEntityData(
  entity: string,
  operation: Operation,
  payload?: unknown
): Promise<any> {
  // MOCK PATH (no network in mock mode)
  if (shouldUseMock(entity, operation)) {
    const mod = await loadMock(entity);
    if (!mod) {
      // Clear signal so you add the missing mock instead of silently hitting network
      throw new Error(
        `Mock not found for client="${CLIENT}" entity="${entity}" operation="${operation}"`
      );
    }

    // prefer operation-specific handler
    if (typeof (mod as any)[operation] === "function") {
      return await (mod as any)[operation](payload);
    }
    // or a generic function
    if (typeof mod === "function") {
      return await (mod as any)(entity, operation, payload);
    }
    // or keyed data
    if (Object.prototype.hasOwnProperty.call(mod, operation)) {
      return (mod as any)[operation];
    }
    // last resort: return the module
    return mod;
  }

  // DIRECT (network) PATH
  const url = buildUrl(entity, operation);
  const method: "GET" | "POST" =
    operation === "post" || operation === "update" || operation === "getOne"
      ? "POST"
      : "GET";

  const options: RequestInit = {
    method,
    headers: { "Content-Type": "application/json" },
    ...(method === "POST" && payload ? { body: JSON.stringify(payload) } : {}),
  };

  const res = await fetch(url, options);
  if (!res.ok) throw new Error(`API failed: ${res.status}`);
  return res.json();
}
