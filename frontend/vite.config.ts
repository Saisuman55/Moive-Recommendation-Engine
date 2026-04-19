import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

/** Browser calls `/api/*` on the Vite origin; Vite forwards to the real API (no CORS in dev). */
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const proxyTarget = env.VITE_PROXY_TARGET || "http://127.0.0.1:8000";

  return {
    plugins: [react()],
    server: {
      port: 5173,
      host: true,
      proxy: {
        "/api": {
          target: proxyTarget,
          changeOrigin: true,
          rewrite: (path) => {
            const rest = path.replace(/^\/api/, "");
            return rest.length ? rest : "/";
          },
        },
      },
    },
  };
});
