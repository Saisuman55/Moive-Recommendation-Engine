/** In dev, use same-origin `/api` (Vite proxy → FastAPI). In production, use `VITE_API_URL`. */
function resolveUrl(path: string): string {
  const p = path.startsWith("/") ? path : `/${path}`;
  if (import.meta.env.DEV) {
    return `/api${p}`;
  }
  const raw = import.meta.env.VITE_API_URL as string | undefined;
  const base = (raw && raw.length > 0 ? raw : "http://127.0.0.1:8000").replace(/\/$/, "");
  return `${base}${p}`;
}

export async function api<T>(
  path: string,
  opts: RequestInit & { token?: string | null } = {}
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(opts.headers ?? {}),
  };
  if (opts.token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${opts.token}`;
  }
  const { token, ...rest } = opts;
  const url = resolveUrl(path);

  let res: Response;
  try {
    res = await fetch(url, { ...rest, headers });
  } catch (e) {
    const msg = e instanceof Error ? e.message : "Network error";
    const hint = import.meta.env.DEV
      ? " Start the API on port 8000 (e.g. from the backend folder: uvicorn app.main:app --reload --host 127.0.0.1 --port 8000)."
      : " Set VITE_API_URL to your API base URL and ensure the server is reachable.";
    throw new Error(`Failed to fetch (${msg}).${hint}`);
  }

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const j = await res.json();
      if (j.detail) detail = typeof j.detail === "string" ? j.detail : JSON.stringify(j.detail);
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}
