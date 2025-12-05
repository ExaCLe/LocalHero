import type {components} from "@/src/lib/openapi-types";

export type HealthResponse = components["schemas"]["HealthResponse"];

type Props = {
  health: HealthResponse | null;
};

export function HealthPanel({health}: Readonly<Props>) {
  const isHealthy =
    health?.status === "ok" && health?.database === "connected";

  if (health === null) {
    return (
      <p style={{color: "#b91c1c"}}>
        Cannot reach backend at{" "}
        <code>{process.env.NEXT_PUBLIC_API_BASE_URL}/health</code>.
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
