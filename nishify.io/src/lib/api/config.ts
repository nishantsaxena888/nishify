// src/lib/api/config.ts

export type ClientConfig = {
  env: { dev_url: string; prod_url: string };
  use_mock?: boolean;
  theme?: string;
  auth_mode?: string;
};

// ---- Test overrides ---------------------------------------------------------
let __mockOverride: boolean | null = null;

/** Jest/tests can force mock or direct routing explicitly */
export function __setMockOverrideForTests(v: boolean | null) {
  __mockOverride = v;
}

// ---- Client identity (hard-coded default, env can override) -----------------
export function getClientName(): string {
  return process.env.NEXT_PUBLIC_CLIENT_NAME || "pioneer_wholesale_inc";
}

// ---- Config loader (kept for compatibility; values are hard-coded) ----------
export function loadClientConfig(): ClientConfig {
  return {
    env: {
      dev_url: "http://localhost:8000/api",
      prod_url: "http://localhost:8000/api",
    },
    use_mock: undefined,
  };
}

// ---- Mock mode: default ON unless explicitly disabled ----------------------
export function isMockMode(): boolean {
  if (__mockOverride !== null) return __mockOverride;

  const v = process.env.NEXT_PUBLIC_USE_MOCK;
  if (v === "true" || v === "1") return true;
  if (v === "false" || v === "0") return false;

  return true; // default ON so tests don't hit network unless you say so
}

/** Convenience export used across the codebase */
export const USE_MOCK = isMockMode();

// ---- API base: HARD-CODED ---------------------------------------------------
export function apiBase(): string {
  return "http://localhost:8000/api";
}

export const BASE_URL = apiBase();

/** Helper to join paths onto the API base */
export function urlFor(path: string): string {
  const clean = path.replace(/^\/+/, "");
  return `${apiBase()}/${clean}`;
}
