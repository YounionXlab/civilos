"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

type Props = {
  apiBase: string;
};

export default function TickButton({ apiBase }: Props) {
  const router = useRouter();
  const [isAdvancing, setIsAdvancing] = useState(false);

  async function advance() {
    setIsAdvancing(true);
    try {
      const response = await fetch(`${apiBase}/tick`, { method: "POST" });
      if (!response.ok) {
        throw new Error("Tick request failed");
      }
      router.refresh();
    } finally {
      setIsAdvancing(false);
    }
  }

  return (
    <button className="primary-action" disabled={isAdvancing} onClick={advance} type="button">
      {isAdvancing ? "Advancing..." : "Advance One Day"}
    </button>
  );
}
