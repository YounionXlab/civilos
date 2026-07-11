"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

type Props = {
  apiBase: string;
};

export default function TickButton({ apiBase }: Props) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [isAdvancing, setIsAdvancing] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  function pause(milliseconds: number) {
    return new Promise((resolve) => window.setTimeout(resolve, milliseconds));
  }

  async function advance() {
    setError(null);
    setIsAdvancing(true);
    setStatus("Processing...");
    try {
      await pause(250);
      setStatus("Running Simulation...");
      const response = await fetch(`${apiBase}/tick`, { method: "POST" });
      if (!response.ok) {
        throw new Error("Tick request failed");
      }
      setStatus("Updating Citizens...");
      await pause(250);
      setStatus("Saving World...");
      await pause(250);
      setStatus("Done.");
      await pause(350);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Tick request failed");
      setStatus(null);
    } finally {
      setIsAdvancing(false);
    }
  }

  return (
    <div className="tick-control">
      <button className="primary-action" disabled={isAdvancing} onClick={advance} type="button">
        {isAdvancing ? "Advancing..." : "Advance One Day"}
      </button>
      {status ? <p className="tick-status">{status}</p> : null}
      {error ? <p className="error-text">{error}</p> : null}
    </div>
  );
}
