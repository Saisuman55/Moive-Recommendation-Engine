/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Production / non-dev: full API origin, e.g. https://api.example.com */
  readonly VITE_API_URL?: string;
  /** Optional; dev server only. Override proxy target (default http://127.0.0.1:8000). */
  readonly VITE_PROXY_TARGET?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
