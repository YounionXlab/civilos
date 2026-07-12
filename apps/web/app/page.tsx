import CitizenPanel from "../components/CitizenPanel";
import type { Citizen } from "../components/CitizenPanel";
import TickButton from "../components/TickButton";
import WorldCard from "../components/WorldCard";
import type { World } from "../components/WorldCard";

type ChronicleEvent = {
  day: number;
  title: string;
  description: string;
  event_impact: Record<string, number>;
};

type ApiResponse<T> = {
  status: string;
  message: string;
  data: T;
};

const defaultCitizens = { count: 0, items: [] as Citizen[] };
const defaultHistory = { count: 0, items: [] as ChronicleEvent[] };

const apiBase =
  process.env.API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  (process.env.VERCEL_PROJECT_PRODUCTION_URL
    ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
    : undefined) ||
  (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : undefined) ||
  "http://localhost:8000";
const clientApiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "";

type FetchResult<T> = { data: T; error: string | null };

async function fetchData<T>(path: string, fallback: T): Promise<FetchResult<T>> {
  try {
    const response = await fetch(`${apiBase}${path}`, { cache: "no-store" });
    if (!response.ok) {
      return { data: fallback, error: `API request failed (${response.status}).` };
    }
    const payload = (await response.json()) as ApiResponse<T>;
    return { data: payload.data, error: null };
  } catch {
    return { data: fallback, error: "API request failed." };
  }
}

export default async function Home() {
  const [worldResult, citizensResult, historyResult] = await Promise.all([
    fetchData<World | null>("/world", null),
    fetchData("/agents", defaultCitizens),
    fetchData("/history", defaultHistory),
  ]);
  const world = worldResult.data;
  const citizens = citizensResult.data;
  const history = historyResult.data;

  return (
    <main className="dashboard">
      <header className="topbar">
        <div>
          <p className="eyebrow">CivilOS Alpha 0.2</p>
          <h1>{world ? world.city : "CivilOS"} Operations</h1>
        </div>
        <TickButton apiBase={clientApiBase} />
      </header>

      {world ? (
        <div className="dashboard-grid">
          <WorldCard world={world} />
          <CitizenPanel citizens={citizens.items} error={citizensResult.error} />

          <section className="panel history-panel">
            <h2>Civilization Chronicle</h2>
            {historyResult.error ? (
              <p className="error-text">{historyResult.error}</p>
            ) : history.items.length > 0 ? (
              <ol className="history-list">
                {history.items.map((item) => (
                  <li key={`${item.day}-${item.title}`}>
                    <span>Day {item.day}</span>
                    <h3>{item.title}</h3>
                    <p>{item.description}</p>
                    <p className="event-impact">
                      {Object.entries(item.event_impact)
                        .map(([resource, change]) => `${resource} ${change > 0 ? "+" : ""}${change}`)
                        .join(" · ")}
                    </p>
                  </li>
                ))}
              </ol>
            ) : (
              <p className="muted">Advance one day to begin the civilization chronicle.</p>
            )}
          </section>
        </div>
      ) : (
        <section className="panel state-panel">
          <h2>{worldResult.error ? "API Error" : "No World Data"}</h2>
          <p className={worldResult.error ? "error-text" : "muted"}>
            {worldResult.error || "The API returned no civilization state."}
          </p>
        </section>
      )}
    </main>
  );
}
