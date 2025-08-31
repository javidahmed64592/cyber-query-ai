import { useEffect, useState } from "react";

import type { HealthResponse } from "./types";

export type HealthStatus = "online" | "offline" | "checking";

export function useHealthStatus(): HealthStatus {
  const [status, setStatus] = useState<HealthStatus>("checking");

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch("/api/health");
        if (res.ok) {
          const data: HealthResponse = await res.json();
          if (data.status === "healthy") {
            setStatus("online");
          } else {
            setStatus("offline");
          }
        } else {
          setStatus("offline");
        }
      } catch {
        setStatus("offline");
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // every 30s
    return () => clearInterval(interval);
  }, []);

  return status;
}
