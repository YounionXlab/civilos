"use client";

import { useState } from "react";

export type Citizen = {
  id: string;
  name: string;
  profession: string;
  mood: string;
  current_task: string;
  latest_memory: Memory | null;
};

type Memory = {
  day: number;
  type: string;
  description: string;
  impact: string;
};

type CitizenProfile = Citizen & {
  aliases: string[];
  age: number;
  gender: string;
  birth_sol: number;
  skills: string[];
  traits: string[];
  personality: string;
  goal: string;
  energy: number;
  health: number;
  memories: Memory[];
};

type Props = {
  citizens: Citizen[];
  error?: string | null;
  apiBase: string;
};

export default function CitizenPanel({ citizens, error, apiBase }: Props) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [selectedCitizen, setSelectedCitizen] = useState<CitizenProfile | null>(null);
  const [detailError, setDetailError] = useState<string | null>(null);
  const [isLoadingDetail, setIsLoadingDetail] = useState(false);

  async function selectCitizen(citizenId: string) {
    setSelectedId(citizenId);
    setSelectedCitizen(null);
    setDetailError(null);
    setIsLoadingDetail(true);
    try {
      const response = await fetch(`${apiBase}/agents/${citizenId}`);
      if (!response.ok) {
        throw new Error("Unable to load citizen profile.");
      }
      const payload = (await response.json()) as { data: CitizenProfile };
      setSelectedCitizen(payload.data);
    } catch (caught) {
      setDetailError(caught instanceof Error ? caught.message : "Unable to load citizen profile.");
    } finally {
      setIsLoadingDetail(false);
    }
  }

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
            onClick={() => selectCitizen(citizen.id)}
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

      {isLoadingDetail ? <p className="muted">Loading citizen profile...</p> : null}
      {detailError ? <p className="error-text">{detailError}</p> : null}
      {selectedCitizen ? (
        <article className="citizen-detail">
          <div className="detail-heading">
            <div>
              <p className="eyebrow">Citizen Detail</p>
              <h3>{selectedCitizen.name}</h3>
            </div>
            <button className="text-action" onClick={() => { setSelectedId(null); setSelectedCitizen(null); }} type="button">
              Close
            </button>
          </div>
          <dl className="detail-grid">
            <div><dt>Profession</dt><dd>{selectedCitizen.profession}</dd></div>
            <div><dt>Mood</dt><dd>{selectedCitizen.mood}</dd></div>
            <div><dt>Energy</dt><dd>{selectedCitizen.energy}%</dd></div>
            <div><dt>Health</dt><dd>{selectedCitizen.health}%</dd></div>
            <div><dt>Goal</dt><dd>{selectedCitizen.goal}</dd></div>
            <div><dt>Current Task</dt><dd>{selectedCitizen.current_task}</dd></div>
            <div><dt>Skills</dt><dd>{selectedCitizen.skills.join(", ")}</dd></div>
            <div><dt>Traits</dt><dd>{selectedCitizen.traits.join(", ")}</dd></div>
            <div><dt>Latest Memory</dt><dd>{selectedCitizen.latest_memory?.description || "No important memories yet."}</dd></div>
          </dl>
        </article>
      ) : null}
    </section>
  );
}
