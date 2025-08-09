// src/lib/api/entityRouter.ts
import { isMockMode, getClientName } from "./config";

export type Operation = "options" | "get" | "getOne" | "post" | "update";

// Optional per-client override map: src/lib/api/clients/<client>/mock.behavior.json
// Example format: { "invoice_item": ["options","get"], "invoice": ["options"] }
let MOCK_BEHAVIOR: Record<string, Operation[]> = {};
try {
  const client = getClientName();
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  const cfg = require(`./clients/${client}/mock.behavior.json`);
  if (cfg && typeof cfg === "object") {
    MOCK_BEHAVIOR = cfg;
  }
} catch {
  // no file is fine; default to empty map
}

export function shouldUseMock(entity: string, operation: Operation): boolean {
  const ops = (MOCK_BEHAVIOR && MOCK_BEHAVIOR[entity]) || [];
  if (Array.isArray(ops) && ops.includes(operation)) return true;
  return isMockMode();
}
