import {HealthPanel, HealthResponse} from "../components/HealthPanel";

async function getHealth(): Promise<HealthResponse | null> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

  if (!baseUrl) {
    console.error("NEXT_PUBLIC_API_BASE_URL is not set");
    return null;
  }

  try {
    const res = await fetch(`${baseUrl}/health`, {cache: "no-store"});

    if (!res.ok) {
      console.error("Health check failed:", res.status, res.statusText);
      return null;
    }

    return res.json();
  } catch (err) {
    console.error("Error calling /health:", err);
    return null;
  }
}

export default async function HomePage() {
  const health = await getHealth();

  return (
    <main
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div
        style={{
          padding: "2rem 3rem",
          borderRadius: "0.75rem",
          border: "1px solid #ddd",
          boxShadow: "0 10px 30px rgba(0,0,0,0.05)",
          textAlign: "center",
        }}
      >
        <h1 style={{fontSize: "1.8rem", marginBottom: "1rem"}}>
          Backend Health
        </h1>
        <HealthPanel health={health}/>
      </div>
    </main>
  );
}
