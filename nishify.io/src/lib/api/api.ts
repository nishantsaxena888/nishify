// src/lib/api/api.ts
import { BASE_URL } from "./config";
import { shouldUseMock } from "./entityRouter";

const CLIENT =
  process.env.NEXT_PUBLIC_CLIENT_NAME || "pioneer_wholesale_inc";

async function loadMock(entity: string) {
  try {
    // NEW: client-scoped mocks
    const mod = await import(`@/clients/${CLIENT}/mock/${entity}.ts`);
    return (mod as any).default || (mod as any)[entity] || mod;
  } catch (e) {
    console.warn(`Mock not found for client=${CLIENT} entity=${entity}`, e);
    return null;
  }
}

export async function fetchEntityData(
  entity: string,
  operation: "options" | "get" | "getOne" | "post" | "update",
  payload?: any,
  forceMock = false
) {
  if (forceMock || shouldUseMock(entity, operation)) {
    const mock = await loadMock(entity);
    if (!mock || !mock[operation]) {
      throw new Error(`Mock not implemented for ${entity} ${operation}`);
    }
    return mock[operation](payload);
  }

  const url = `${BASE_URL}/entity/${entity}/${operation}`;
  const method = ["post", "update", "getOne"].includes(operation)
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
