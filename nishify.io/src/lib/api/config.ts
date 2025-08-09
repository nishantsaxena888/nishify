// src/lib/api/config.ts
export type ClientConfig = {
  env: { dev_url: string; prod_url: string };
  use_mock?: boolean;
  theme?: string;
  auth_mode?: string;
};

let __mockOverride: boolean | null = null;

/** Jest uses this to force mock/direct routing in tests */
export function __setMockOverrideForTests(v: boolean | null) {
  __mockOverride = v;
}

export function getClientName(): string {
  // NEXT_PUBLIC_* works in Next.js + Jest envs
  return process.env.NEXT_PUBLIC_CLIENT_NAME || "default_client";
}

export function loadClientConfig(): ClientConfig {
  const name = getClientName();
  try {
    // resolved relative to this file: src/lib/api/clients/<client>/config.json
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const cfg = require(`../clients/${name}/config.json`);
    return cfg as ClientConfig;
  } catch {
    // safe fallback so tests never crash
    return {
      env: {
        dev_url: "http://localhost:8000/api",
        prod_url: "http://localhost:8000/api",
      },
      use_mock: true,
      theme: "default",
      auth_mode: "none",
    };
  }
}

export function isMockMode(): boolean {
  if (__mockOverride !== null) return __mockOverride;
  const fromEnv = process.env.NEXT_PUBLIC_USE_MOCK;
  if (fromEnv === "true" || fromEnv === "1") return true;
  if (fromEnv === "false" || fromEnv === "0") return false;
  const cfg = loadClientConfig();
  return !!cfg.use_mock;
}

export function apiBase(): string {
  const cfg = loadClientConfig();
  const base = process.env.NEXT_PUBLIC_API_BASE || cfg.env?.dev_url || "http://localhost:8000/api";
  return base.replace(/\/+$/, "");
}

export function urlFor(entity: string): string {
  return `${apiBase()}/${entity}`;
}
