"use client";

type Props = {
  error: Error;
  reset: () => void;
};

export default function Error({ error, reset }: Props) {
  return (
    <main className="dashboard">
      <section className="panel state-panel">
        <p className="eyebrow">CivilOS Alpha 0.1</p>
        <h1>Dashboard Error</h1>
        <p className="muted">{error.message || "Unable to render the dashboard."}</p>
        <button className="primary-action" onClick={reset} type="button">
          Try Again
        </button>
      </section>
    </main>
  );
}
