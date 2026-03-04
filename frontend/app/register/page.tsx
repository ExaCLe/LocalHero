import Link from "next/link";

export default function RegisterPage() {
  return (
    <main style={{ padding: "2rem", fontFamily: "system-ui, sans-serif" }}>
      <h1>Register</h1>
      <form style={{ display: "grid", gap: "0.75rem", maxWidth: 360 }}>
        <label>
          Email
          <input type="email" name="email" />
        </label>
        <label>
          Password
          <input type="password" name="password" />
        </label>
        <label>
          Confirm Password
          <input type="password" name="confirmPassword" />
        </label>
        <button type="submit">Register</button>
      </form>
      <p style={{ marginTop: "1rem" }}>
        <Link href="/login">Already have an account?</Link>
      </p>
    </main>
  );
}
