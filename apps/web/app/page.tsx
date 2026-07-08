import TickButton from "../components/TickButton";
import WorldCard from "../components/WorldCard";
import type { World } from "../components/WorldCard";

type Agent = {
  id: string;
  name: string;
  role: string;
  needs?: Record<string, number>;
  goals?: string[];
};

type HistoryItem = {
  day: number;
  title: string;
  deltas?: Record<string, number>;
};

const apiBase =
  process.env.API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  "http://localhost:8000";
const clientApiBase = process.env.NEXT_PUBLIC_API_BASE_URL || apiBase;

async function fetchJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${apiBase}${path}`, { cache: "no-store" });
    if (!response.ok) {
      return fallback;
    }
    return response.json();
  } catch {
    return fallback;
  }
}

export default async function Home() {
  const [world, agents, history] = await Promise.all([
    fetchJson<World | null>("/world", null),
    fetchJson<{ count: number; items: Agent[] }>("/agents", { count: 0, items: [] }),
    fetchJson<{ count: number; items: HistoryItem[] }>("/history", { count: 0, items: [] }),
  ]);

  return (
    <main className="dashboard">
      <header className="topbar">
        <div>
          <p className="eyebrow">CivilOS Alpha 0.1</p>
          <h1>{world ? world.city : "CivilOS"} Operations</h1>
        </div>
        <TickButton apiBase={clientApiBase} />
      </header>

      {world ? (
        <div className="dashboard-grid">
          <WorldCard world={world} />

          <section className="panel">
            <h2>Citizens</h2>
            <div className="agent-list">
              {agents.items.map((agent) => (
                <article className="agent-card" key={agent.id}>
                  <div>
                    <h3>{agent.name}</h3>
                    <p>{agent.role}</p>
                  </div>
                  <p>{agent.goals?.[0] || "Maintain colony stability"}</p>
                </article>
              ))}
            </div>
          </section>

          <section className="panel history-panel">
            <h2>History</h2>
            {history.items.length > 0 ? (
              <ol className="history-list">
                {history.items
                  .slice()
                  .reverse()
                  .map((item) => (
                    <li key={`${item.day}-${item.title}`}>
                      <span>Day {item.day}</span>
                      <p>{item.title}</p>
                    </li>
                  ))}
              </ol>
            ) : (
              <p className="muted">No recorded history yet.</p>
            )}
          </section>
        </div>
      ) : (
        <section className="panel">
          <h2>API Offline</h2>
          <p className="muted">Start the FastAPI service to load the civilization state.</p>
        </section>
      )}
    </main>
  );
}
