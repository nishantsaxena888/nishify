// src/lib/api/options-merged.ts
import { CLIENT, API_BASE_URL } from "./config";

export type Field = {
  name: string;
  type?: string;
  label?: string;
  required?: boolean;
  read_only?: boolean;
  nullable?: boolean;
  primary_key?: boolean;
  foreign_key?: string | null;
  default?: any;
};

type AdminTable = {
  delete_confirmation?: boolean;
  inline_edit?: boolean;
  show_filters?: boolean;
  page_size?: number;
  global_search?: boolean;
  column_search?: boolean;
  sortable?: boolean;
  sticky_header?: boolean;
} | null;

type Admin = {
  table?: AdminTable;
  form?: any;
  list?: any;
} | null;

export type Options = {
  entity: string;
  title?: string;
  primary_key?: string | null;
  fields: Field[];
  admin?: Admin;
};

const ADMIN_DEFAULTS: Required<NonNullable<Admin>> = {
  table: {
    delete_confirmation: true,
    inline_edit: false,
    show_filters: true,
    page_size: 20,
    global_search: true,
    column_search: false,
    sortable: true,
    sticky_header: false,
  },
  form: null,
  list: null,
};

function withAdminDefaults(admin: Admin): Admin {
  if (!admin) return { ...ADMIN_DEFAULTS };
  const table = admin.table ?? {};
  return {
    table: {
      ...ADMIN_DEFAULTS.table,
      ...(table || {}),
    },
    form: admin.form ?? ADMIN_DEFAULTS.form,
    list: admin.list ?? ADMIN_DEFAULTS.list,
  };
}

function normalize(raw: any, entity: string): Options {
  if (!raw) return { entity, fields: [], admin: withAdminDefaults(null) };

  // Minimal array form: ["id","name",...]
  if (Array.isArray(raw)) {
    const names = raw.map((n) => String(n));
    return {
      entity,
      primary_key: names.includes("id") ? "id" : null,
      fields: names.map((n) => ({ name: n })),
      admin: withAdminDefaults(null),
    };
  }

  // Accept { fields } | { schema } | { admin/form/list } shapes
  const rawFields = Array.isArray(raw.fields)
    ? raw.fields
    : Array.isArray(raw.schema)
    ? raw.schema
    : [];

  const fields: Field[] = rawFields.map((f: any) =>
    typeof f === "string" ? { name: f } : f
  );
  const names = fields.map((f) => f.name).filter(Boolean);

  const admin: Admin =
    raw.admin ?? { form: raw.form, list: raw.list, table: raw.table_config };

  return {
    entity: raw.entity ?? entity,
    title: raw.title,
    primary_key: raw.primary_key ?? (names.includes("id") ? "id" : null),
    fields,
    admin: withAdminDefaults(admin),
  };
}

function mergeFields(live: Field[], mock: Field[]): Field[] {
  const byName = new Map<string, Field>();
  for (const f of mock) if (f?.name) byName.set(f.name, { ...f });
  for (const f of live)
    if (f?.name)
      byName.set(f.name, { ...(byName.get(f.name) || {}), ...f }); // live wins

  const order = live.map((f) => f.name);
  const out: Field[] = [];
  for (const n of order) {
    const v = byName.get(n);
    if (v) out.push(v);
  }
  for (const [n, v] of byName) if (!order.includes(n)) out.push(v);
  return out;
}

function deepMerge(a: any, b: any): any {
  if (!a) return b || {};
  if (!b) return a || {};
  const out: any = { ...a };
  for (const [k, v] of Object.entries(b)) {
    if (Array.isArray(v)) out[k] = v.slice(); // array: right side wins (live)
    else if (v && typeof v === "object") out[k] = deepMerge(out[k], v);
    else out[k] = v;
  }
  return out;
}

/** Mock-first; backend fallback; typically sufficient since codegen can pre-merge admin into mock. */
export async function fetchOptionsMerged(entity: string): Promise<Options> {
  // 1) mock first (preferred)
  try {
    const mod = await import(`@/clients/${CLIENT}/mock/${entity}.ts`);
    const mockRaw =
      (mod as any).default?.options?.() ??
      (mod as any).options?.() ??
      (mod as any).options ??
      null;
    return normalize(mockRaw, entity);
  } catch {
    // no mock => fallback to backend
  }

  // 2) backend fallback
  const liveRaw = await fetch(`${API_BASE_URL}/${entity}/options?schema=full`)
    .then((r) => (r.ok ? r.json() : null))
    .catch(() => null);

  return normalize(liveRaw, entity);
}

/** Backend-preferred + merge (live overrides mock) — use if you need live-first. */
export async function fetchOptionsMergedBackendPreferred(
  entity: string
): Promise<Options> {
  const [live, mock] = await Promise.allSettled([
    fetch(`${API_BASE_URL}/${entity}/options?schema=full`).then((r) =>
      r.ok ? r.json() : null
    ),
    import(`@/clients/${CLIENT}/mock/${entity}.ts`).then(
      (m) =>
        ((m as any).default?.options?.() ??
          (m as any).options?.() ??
          (m as any).options ??
          null) as any
    ),
  ]);

  const L = normalize(live.status === "fulfilled" ? live.value : null, entity);
  const M = normalize(mock.status === "fulfilled" ? mock.value : null, entity);

  return {
    entity: L.entity || M.entity || entity,
    title: L.title || M.title,
    primary_key: L.primary_key ?? M.primary_key,
    fields: mergeFields(L.fields, M.fields),
    admin: withAdminDefaults(deepMerge(M.admin, L.admin)), // live overrides mock
  };
}
