import Link from "next/link";
import { ConvexHttpClient } from "convex/browser";
import { anyApi } from "convex/server";
import { HealthPanel, type HealthResponse } from "../components/HealthPanel";

async function getHealth(): Promise<HealthResponse | null> {
  const convexUrl = process.env.NEXT_PUBLIC_CONVEX_URL;

  if (!convexUrl) {
    return null;
  }

  try {
    const client = new ConvexHttpClient(convexUrl);
    const response = await client.query(anyApi.health.status, {});
    return response as HealthResponse;
  } catch (error) {
    console.error("Failed to query Convex health status", error);
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
          minWidth: 360,
        }}
      >
        <h1 style={{fontSize: "1.8rem", marginBottom: "1rem"}}>Backend Health</h1>
        <HealthPanel health={health} />

        <nav
          style={{
            marginTop: "1.25rem",
            display: "flex",
            justifyContent: "center",
            gap: "1rem",
          }}
        >
          <Link href="/login">Login</Link>
          <Link href="/register">Register</Link>
        </nav>
      </div>
    </main>
  );
}
