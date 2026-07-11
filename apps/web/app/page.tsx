import CitizenPanel from "../components/CitizenPanel";
import type { Citizen } from "../components/CitizenPanel";
import TickButton from "../components/TickButton";
import WorldCard from "../components/WorldCard";
import type { World } from "../components/WorldCard";

type ChronicleEvent = {
  day: number;
  title: string;
  description: string;
  impact: Record<string, number>;
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

async function fetchData<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${apiBase}${path}`, { cache: "no-store" });
    if (!response.ok) {
      return fallback;
    }
    const payload = (await response.json()) as ApiResponse<T>;
    return payload.data;
  } catch {
    return fallback;
  }
}

export default async function Home() {
  const [world, citizens, history] = await Promise.all([
    fetchData<World | null>("/world", null),
    fetchData("/agents", defaultCitizens),
    fetchData("/history", defaultHistory),
  ]);

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
          <CitizenPanel citizens={citizens.items} />

          <section className="panel history-panel">
            <h2>Civilization Chronicle</h2>
            {history.items.length > 0 ? (
              <ol className="history-list">
                {history.items.map((item) => (
                  <li key={`${item.day}-${item.title}`}>
                    <span>Day {item.day}</span>
                    <h3>{item.title}</h3>
                    <p>{item.description}</p>
                    <p className="event-impact">
                      {Object.entries(item.impact)
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
          <h2>API Offline</h2>
          <p className="muted">Start the FastAPI service to load the civilization state.</p>
        </section>
      )}
    </main>
  );
}
