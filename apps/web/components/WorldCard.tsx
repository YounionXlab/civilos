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

export default function WorldCard({ world }: Props) {
  return (
    <section className="panel world-panel">
      <div className="world-heading">
        <div>
          <p className="eyebrow">{world.planet}</p>
          <h2>{world.city}</h2>
        </div>
        <div className="day-counter">
          <span>Day</span>
          <strong>{world.day}</strong>
        </div>
      </div>

      <div className="metric-grid">
        {metrics.map(([label, key]) => (
          <div className="metric" key={key}>
            <span>{label}</span>
            <strong>{world[key]}</strong>
          </div>
        ))}
        <div className="metric">
          <span>CQ</span>
          <strong>{Math.round(world.cq * 100)}%</strong>
        </div>
      </div>
    </section>
  );
}
