import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "./api";

type Movie = { id: number; title: string; year: number | null; genres: string | null };
type Rec = { movie_id: number; title: string; year: number | null; genres: string | null; score: number };

export default function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [meEmail, setMeEmail] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("token"));
  const [movies, setMovies] = useState<Movie[]>([]);
  const [recs, setRecs] = useState<Rec[]>([]);
  const [ratingsDraft, setRatingsDraft] = useState<Record<number, string>>({});
  const [msg, setMsg] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const authed = useMemo(() => Boolean(token), [token]);

  const setTokenPersist = useCallback((t: string | null) => {
    setToken(t);
    if (t) localStorage.setItem("token", t);
    else localStorage.removeItem("token");
  }, []);

  const loadMovies = useCallback(async () => {
    const rows = await api<Movie[]>("/movies?limit=100");
    setMovies(rows);
  }, []);

  useEffect(() => {
    if (!token) {
      setMeEmail(null);
      return;
    }
    api<{ email: string }>("/auth/me", { token })
      .then((u) => setMeEmail(u.email))
      .catch(() => setMeEmail(null));
  }, [token]);

  useEffect(() => {
    if (!authed) return;
    loadMovies().catch((e) => setMsg(String(e.message)));
  }, [authed, loadMovies]);

  async function register() {
    setMsg(null);
    setBusy(true);
    try {
      await api("/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      setMsg("Registered — you can log in now.");
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Error");
    } finally {
      setBusy(false);
    }
  }

  async function login() {
    setMsg(null);
    setBusy(true);
    try {
      const t = await api<{ access_token: string }>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      setTokenPersist(t.access_token);
      setMsg("Signed in.");
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Error");
    } finally {
      setBusy(false);
    }
  }

  function logout() {
    setTokenPersist(null);
    setMovies([]);
    setRecs([]);
    setMsg(null);
  }

  async function submitRating(movieId: number) {
    if (!token) return;
    const raw = ratingsDraft[movieId];
    const rating = Number(raw);
    if (Number.isNaN(rating) || rating < 0.5 || rating > 5) {
      setMsg("Rating must be between 0.5 and 5.");
      return;
    }
    setMsg(null);
    setBusy(true);
    try {
      await api("/ratings", {
        method: "POST",
        token,
        body: JSON.stringify({ movie_id: movieId, rating }),
      });
      setMsg(`Saved rating for movie #${movieId}`);
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Error");
    } finally {
      setBusy(false);
    }
  }

  async function train() {
    if (!token) return;
    setMsg(null);
    setBusy(true);
    try {
      const r = await api<{ status: string; reason?: string }>("/recommendations/train", {
        method: "POST",
        token,
      });
      setMsg(JSON.stringify(r));
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Error");
    } finally {
      setBusy(false);
    }
  }

  async function loadRecs() {
    if (!token) return;
    setMsg(null);
    setBusy(true);
    try {
      const rows = await api<Rec[]>("/recommendations?limit=10", { token });
      setRecs(rows);
      setMsg(rows.length ? "Loaded recommendations." : "No rows yet — rate movies and train.");
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Error");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div style={{ maxWidth: 880, margin: "0 auto", padding: "1.5rem" }}>
      <header style={{ marginBottom: "1.5rem" }}>
        <h1 style={{ margin: "0 0 0.25rem", fontSize: "1.5rem" }}>Movie Recommendation Engine</h1>
        <p style={{ margin: 0, color: "#475569", fontSize: "0.95rem" }}>
          FastAPI · React 18 · Surprise SVD · Postgres
        </p>
      </header>

      {!authed ? (
        <section
          style={{
            background: "#fff",
            border: "1px solid #e2e8f0",
            borderRadius: 12,
            padding: "1rem 1.25rem",
            marginBottom: "1rem",
          }}
        >
          <h2 style={{ marginTop: 0, fontSize: "1.1rem" }}>Account</h2>
          <label style={{ display: "block", marginBottom: 8 }}>
            <span style={{ display: "block", fontSize: 13, color: "#64748b" }}>Email</span>
            <input
              style={{ width: "100%", maxWidth: 360, padding: "0.5rem 0.6rem" }}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
            />
          </label>
          <label style={{ display: "block", marginBottom: 12 }}>
            <span style={{ display: "block", fontSize: 13, color: "#64748b" }}>Password (min 8)</span>
            <input
              type="password"
              style={{ width: "100%", maxWidth: 360, padding: "0.5rem 0.6rem" }}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </label>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            <button type="button" disabled={busy} onClick={() => void register()}>
              Register
            </button>
            <button type="button" disabled={busy} onClick={() => void login()}>
              Log in
            </button>
          </div>
        </section>
      ) : (
        <>
          <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: "1rem" }}>
            <span style={{ color: "#475569", fontSize: 14 }}>Signed in as {meEmail ?? "…"}</span>
            <button type="button" onClick={logout}>
              Log out
            </button>
            <button type="button" disabled={busy} onClick={() => void loadRecs()}>
              Refresh recommendations
            </button>
            <button type="button" disabled={busy} onClick={() => void train()}>
              Train model (SVD)
            </button>
          </div>

          <section
            style={{
              background: "#fff",
              border: "1px solid #e2e8f0",
              borderRadius: 12,
              padding: "1rem 1.25rem",
              marginBottom: "1rem",
            }}
          >
            <h2 style={{ marginTop: 0, fontSize: "1.1rem" }}>Movies</h2>
            <p style={{ marginTop: 0, color: "#64748b", fontSize: 14 }}>
              Rate a few titles (0.5–5), then run <strong>Train model</strong>, then refresh recommendations.
            </p>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {movies.map((m) => (
                <li
                  key={m.id}
                  style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: 8,
                    alignItems: "center",
                    padding: "10px 0",
                    borderBottom: "1px solid #f1f5f9",
                  }}
                >
                  <span style={{ flex: "1 1 200px" }}>
                    <strong>{m.title}</strong>
                    {m.year != null ? ` (${m.year})` : ""}
                    {m.genres ? <span style={{ color: "#64748b" }}> — {m.genres}</span> : null}
                  </span>
                  <input
                    type="number"
                    step={0.5}
                    min={0.5}
                    max={5}
                    placeholder="rating"
                    style={{ width: 100 }}
                    value={ratingsDraft[m.id] ?? ""}
                    onChange={(e) =>
                      setRatingsDraft((d) => ({
                        ...d,
                        [m.id]: e.target.value,
                      }))
                    }
                  />
                  <button type="button" disabled={busy} onClick={() => void submitRating(m.id)}>
                    Save
                  </button>
                </li>
              ))}
            </ul>
          </section>

          <section
            style={{
              background: "#fff",
              border: "1px solid #e2e8f0",
              borderRadius: 12,
              padding: "1rem 1.25rem",
            }}
          >
            <h2 style={{ marginTop: 0, fontSize: "1.1rem" }}>Top picks for you</h2>
            {recs.length === 0 ? (
              <p style={{ color: "#64748b" }}>No recommendations loaded yet.</p>
            ) : (
              <ol style={{ margin: 0, paddingLeft: "1.1rem" }}>
                {recs.map((r) => (
                  <li key={r.movie_id} style={{ marginBottom: 6 }}>
                    <strong>{r.title}</strong>
                    <span style={{ color: "#64748b" }}> — score {r.score.toFixed(2)}</span>
                  </li>
                ))}
              </ol>
            )}
          </section>
        </>
      )}

      {msg ? (
        <p
          style={{
            marginTop: "1rem",
            padding: "0.75rem 1rem",
            background: "#eff6ff",
            border: "1px solid #bfdbfe",
            borderRadius: 8,
            color: "#1e3a8a",
            fontSize: 14,
          }}
        >
          {msg}
        </p>
      ) : null}
    </div>
  );
}
