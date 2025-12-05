export type HealthResponse = {
  status: string;
  database: string;
};

type Props = {
  health: HealthResponse | null;
};

export function HealthPanel({health}: Readonly<Props>) {
  const ok = health?.status === "ok" && health?.database === "connected";

  if (health === null) {
    return (
      <p style={{color: "#b91c1c"}}>
        Cannot reach backend at{" "}
        <code>{process.env.NEXT_PUBLIC_API_BASE_URL}/health</code>.
      </p>
    );
  }

  if (ok) {
    return (
      <>
        <p
          style={{
            color: "#15803d",
            fontWeight: 600,
            marginBottom: "0.5rem",
          }}
        >
          ✅ Healthy
        </p>
        <p style={{color: "#4b5563"}}>
          Status: <code>{health.status}</code>, DB:{" "}
          <code>{health.database}</code>
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
        ⚠️ Unhealthy
      </p>
      <p style={{color: "#4b5563"}}>
        Status: <code>{health.status}</code>, DB:{" "}
        <code>{health.database}</code>
      </p>
    </>
  );
}
