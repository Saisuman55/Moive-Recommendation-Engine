const base = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

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
  const res = await fetch(`${base}${path}`, { ...rest, headers });
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
