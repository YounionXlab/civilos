"use client";

import { useMemo, useRef, useState } from "react";

import { createLatestRequestGuard } from "./latestRequest.mjs";

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
  const [query, setQuery] = useState("");
  const [profession, setProfession] = useState("all");
  const abortControllerRef = useRef<AbortController | null>(null);
  const requestGuardRef = useRef(createLatestRequestGuard());

  const professions = useMemo(
    () => Array.from(new Set(citizens.map((citizen) => citizen.profession))).sort(),
    [citizens],
  );
  const filteredCitizens = useMemo(() => {
    const normalizedQuery = query.trim().toLocaleLowerCase();
    return citizens.filter((citizen) => {
      const matchesProfession = profession === "all" || citizen.profession === profession;
      const matchesQuery =
        !normalizedQuery ||
        citizen.name.toLocaleLowerCase().includes(normalizedQuery) ||
        citizen.profession.toLocaleLowerCase().includes(normalizedQuery) ||
        citizen.current_task.toLocaleLowerCase().includes(normalizedQuery);
      return matchesProfession && matchesQuery;
    });
  }, [citizens, profession, query]);

  async function selectCitizen(citizenId: string) {
    abortControllerRef.current?.abort();
    const controller = new AbortController();
    abortControllerRef.current = controller;
    const requestToken = requestGuardRef.current.begin();
    setSelectedId(citizenId);
    setSelectedCitizen(null);
    setDetailError(null);
    setIsLoadingDetail(true);
    try {
      const response = await fetch(`${apiBase}/agents/${encodeURIComponent(citizenId)}`, {
        signal: controller.signal,
      });
      if (!response.ok) {
        throw new Error("Unable to load citizen profile.");
      }
      const payload = (await response.json()) as { data: CitizenProfile };
      if (requestGuardRef.current.isCurrent(requestToken)) {
        setSelectedCitizen(payload.data);
      }
    } catch (caught) {
      if (requestGuardRef.current.isCurrent(requestToken) && !controller.signal.aborted) {
        setDetailError(caught instanceof Error ? caught.message : "Unable to load citizen profile.");
      }
    } finally {
      if (requestGuardRef.current.isCurrent(requestToken)) {
        setIsLoadingDetail(false);
      }
    }
  }

  function closeCitizen() {
    requestGuardRef.current.cancel();
    abortControllerRef.current?.abort();
    setSelectedId(null);
    setSelectedCitizen(null);
    setDetailError(null);
    setIsLoadingDetail(false);
  }

  return (
    <section className="panel citizen-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Colony roster</p>
          <h2>Citizens</h2>
        </div>
        <span className="count-badge">{filteredCitizens.length}/{citizens.length}</span>
      </div>

      {error ? <p className="error-text" role="alert">{error}</p> : null}
      {citizens.length > 0 ? (
        <div className="citizen-tools">
          <label className="search-field">
            <span className="sr-only">Search citizens</span>
            <input
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search name, role, or task"
              type="search"
              value={query}
            />
          </label>
          <label>
            <span className="sr-only">Filter by profession</span>
            <select onChange={(event) => setProfession(event.target.value)} value={profession}>
              <option value="all">All professions</option>
              {professions.map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
          </label>
        </div>
      ) : null}

      {!error && citizens.length === 0 ? <p className="muted">No citizens recorded.</p> : null}
      {!error && citizens.length > 0 && filteredCitizens.length === 0 ? (
        <p className="empty-state">No citizens match these filters.</p>
      ) : null}

      <div className="agent-list">
        {filteredCitizens.map((citizen) => (
          <button
            aria-pressed={citizen.id === selectedId}
            className="agent-card"
            key={citizen.id}
            onClick={() => selectCitizen(citizen.id)}
            type="button"
          >
            <div className="agent-card-heading">
              <div>
                <h3>{citizen.name}</h3>
                <p>{citizen.profession}</p>
              </div>
              <span className={`mood-dot mood-${citizen.mood.toLowerCase()}`} title={`Mood: ${citizen.mood}`} />
            </div>
            <p className="agent-task">{citizen.current_task}</p>
          </button>
        ))}
      </div>

      <div aria-live="polite">
        {isLoadingDetail ? <div className="detail-skeleton">Loading citizen profile...</div> : null}
        {detailError ? <p className="error-text" role="alert">{detailError}</p> : null}
      </div>

      {selectedCitizen ? (
        <article className="citizen-detail">
          <div className="detail-heading">
            <div>
              <p className="eyebrow">Citizen detail</p>
              <h3>{selectedCitizen.name}</h3>
              <p className="detail-subtitle">{selectedCitizen.profession} · {selectedCitizen.mood}</p>
            </div>
            <button aria-label="Close citizen detail" className="text-action" onClick={closeCitizen} type="button">Close</button>
          </div>
          <dl className="detail-grid">
            <div><dt>Energy</dt><dd>{selectedCitizen.energy}%</dd></div>
            <div><dt>Health</dt><dd>{selectedCitizen.health}%</dd></div>
            <div className="detail-wide"><dt>Goal</dt><dd>{selectedCitizen.goal}</dd></div>
            <div className="detail-wide"><dt>Current task</dt><dd>{selectedCitizen.current_task}</dd></div>
            <div><dt>Skills</dt><dd>{selectedCitizen.skills.join(", ")}</dd></div>
            <div><dt>Traits</dt><dd>{selectedCitizen.traits.join(", ")}</dd></div>
            <div className="detail-wide"><dt>Latest memory</dt><dd>{selectedCitizen.latest_memory?.description || "No important memories yet."}</dd></div>
          </dl>
        </article>
      ) : null}
    </section>
  );
}
