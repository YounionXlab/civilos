export type World = {
  day: number;
  planet: string;
  city: string;
  population: number;
  energy: number;
  water: number;
  food: number;
  technology: number;
  cq: number;
};

type Props = {
  world: World;
};

const metrics = [
  ["Population", "population"],
  ["Energy", "energy"],
  ["Water", "water"],
  ["Food", "food"],
  ["Technology", "technology"],
] as const;

function statusFor(value: number) {
  if (value < 35) return "critical";
  if (value < 60) return "watch";
  return "stable";
}

export default function WorldCard({ world }: Props) {
  return (
    <section className="panel world-panel">
      <div className="world-heading">
        <div>
          <p className="eyebrow">{world.planet}</p>
          <h2>{world.city}</h2>
          <p className="panel-intro">Live operational state of the colony.</p>
        </div>
        <div className="day-counter">
          <span>Day</span>
          <strong>{world.day}</strong>
        </div>
      </div>

      <div className="metric-grid">
        {metrics.map(([label, key]) => {
          const value = world[key];
          const hasThreshold = key !== "population";
          const status = hasThreshold ? statusFor(value) : "neutral";
          return (
            <div className={`metric metric-${status}`} key={key}>
              <div className="metric-heading">
                <span>{label}</span>
                {hasThreshold ? <small>{status}</small> : null}
              </div>
              <strong>{value}</strong>
              {hasThreshold ? (
                <div aria-label={`${label}: ${value} percent, ${status}`} className="metric-track" role="img">
                  <span style={{ width: `${Math.max(0, Math.min(100, value))}%` }} />
                </div>
              ) : null}
            </div>
          );
        })}
        <div className={`metric metric-${statusFor(world.cq * 100)}`}>
          <div className="metric-heading"><span>CQ</span><small>{statusFor(world.cq * 100)}</small></div>
          <strong>{Math.round(world.cq * 100)}%</strong>
          <div aria-label={`CQ: ${Math.round(world.cq * 100)} percent`} className="metric-track" role="img">
            <span style={{ width: `${Math.round(world.cq * 100)}%` }} />
          </div>
        </div>
      </div>
    </section>
  );
}
