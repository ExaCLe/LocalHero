export type HealthResponse = {
  status: "ok" | "error";
  database: "connected" | "disconnected";
  backend: "convex";
  timestampIso: string;
};

type Props = {
  health: HealthResponse | null;
};

export function HealthPanel({health}: Readonly<Props>) {
  const isHealthy =
    health?.status === "ok" && health?.database === "connected";

  if (health === null) {
    return (
      <p style={{color: "#b91c1c"}}>
        Cannot reach Convex backend. Set <code>NEXT_PUBLIC_CONVEX_URL</code> and
        run <code>npm run convex:dev</code>.
      </p>
    );
  }

  if (isHealthy) {
    return (
      <>
        <p
          style={{
            color: "#15803d",
            fontWeight: 600,
            marginBottom: "0.5rem",
          }}
        >
          Healthy
        </p>
        <p style={{color: "#4b5563"}}>
          Status: <code>{health.status}</code>, DB: <code>{health.database}</code>,
          Backend: <code>{health.backend}</code>
        </p>
      </>
    );
  }

  return (
    <>
      <p
        style={{
          color: "#b91c1c",
          fontWeight: 600,
          marginBottom: "0.5rem",
        }}
      >
        Unhealthy
      </p>
      <p style={{color: "#4b5563"}}>
        Status: <code>{health.status}</code>, DB: <code>{health.database}</code>,
        Backend: <code>{health.backend}</code>
      </p>
    </>
  );
}
