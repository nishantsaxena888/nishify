// jest.config.js
const { createDefaultPreset } = require("ts-jest");

const tsJestTransformCfg = createDefaultPreset().transform;

/** @type {import("jest").Config} **/
module.exports = {
  rootDir: ".", // repo root is the nishify.io folder for tests
  testEnvironment: "node",
  transform: {
    ...tsJestTransformCfg,
  },
  moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json"],
  // Make "@/..." imports work in tests
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/src/$1",
  },
  // Pick up our tests under src
  testMatch: ["<rootDir>/src/**/*.test.ts"],
  // Optional but handy
  passWithNoTests: true,
};
