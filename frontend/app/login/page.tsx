import Link from "next/link";

export default function LoginPage() {
  return (
    <main style={{ padding: "2rem", fontFamily: "system-ui, sans-serif" }}>
      <h1>Login</h1>
      <form style={{ display: "grid", gap: "0.75rem", maxWidth: 360 }}>
        <label>
          Email
          <input type="email" name="email" />
        </label>
        <label>
          Password
          <input type="password" name="password" />
        </label>
        <button type="submit">Login</button>
      </form>
      <p style={{ marginTop: "1rem" }}>
        <Link href="/register">Create an account</Link>
      </p>
    </main>
  );
}
