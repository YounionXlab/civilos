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

  async function advance() {
    setError(null);
    setIsAdvancing(true);
    try {
      const response = await fetch(`${apiBase}/tick`, { method: "POST" });
      if (!response.ok) {
        throw new Error("Tick request failed");
      }
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Tick request failed");
    } finally {
      setIsAdvancing(false);
    }
  }

  return (
    <div className="tick-control">
      <button className="primary-action" disabled={isAdvancing} onClick={advance} type="button">
        {isAdvancing ? "Advancing..." : "Advance One Day"}
      </button>
      {error ? <p className="error-text">{error}</p> : null}
    </div>
  );
}
