import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./e2e",
  workers: 1,
  retries: 0,
  timeout: 45000,
  use: {
    baseURL: process.env.BASE_URL || "http://127.0.0.1:8000",
    viewport: { width: 1440, height: 1000 },
    ...(process.env.CI ? {} : { channel: "chrome" }),
  },
});
