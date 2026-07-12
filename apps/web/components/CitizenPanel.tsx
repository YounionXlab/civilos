"use client";

import { useState } from "react";

export type Citizen = {
  id: string;
  name: string;
  profession: string;
  goal: string;
  mood: string;
  energy: number;
  current_task: string;
  last_log: string;
};

type Props = {
  citizens: Citizen[];
  error?: string | null;
};

export default function CitizenPanel({ citizens, error }: Props) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const selectedCitizen = citizens.find((citizen) => citizen.id === selectedId);

  return (
    <section className="panel">
      <h2>Citizens</h2>
      {error ? <p className="error-text">{error}</p> : null}
      {!error && citizens.length === 0 ? <p className="muted">No citizens recorded.</p> : null}
      <div className="agent-list">
        {citizens.map((citizen) => (
          <button
            aria-pressed={citizen.id === selectedId}
            className="agent-card"
            key={citizen.id}
            onClick={() => setSelectedId(citizen.id)}
            type="button"
          >
            <div>
              <h3>{citizen.name}</h3>
              <p>{citizen.profession}</p>
            </div>
            <p>{citizen.current_task}</p>
          </button>
        ))}
      </div>

      {selectedCitizen ? (
        <article className="citizen-detail">
          <div className="detail-heading">
            <div>
              <p className="eyebrow">Citizen Detail</p>
              <h3>{selectedCitizen.name}</h3>
            </div>
            <button className="text-action" onClick={() => setSelectedId(null)} type="button">
              Close
            </button>
          </div>
          <dl className="detail-grid">
            <div><dt>Profession</dt><dd>{selectedCitizen.profession}</dd></div>
            <div><dt>Mood</dt><dd>{selectedCitizen.mood}</dd></div>
            <div><dt>Energy</dt><dd>{selectedCitizen.energy}%</dd></div>
            <div><dt>Goal</dt><dd>{selectedCitizen.goal}</dd></div>
            <div><dt>Current Task</dt><dd>{selectedCitizen.current_task}</dd></div>
            <div><dt>Last Log</dt><dd>{selectedCitizen.last_log}</dd></div>
          </dl>
        </article>
      ) : null}
    </section>
  );
}
