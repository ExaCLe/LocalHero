"use client";

import Link from "next/link";
import { useAuth } from "@/contexts/auth-context";

export function CTASection() {
  const { isAuthenticated } = useAuth();

  return (
    <section className="bg-primary py-24 text-primary-foreground">
      <div className="container mx-auto px-4 text-center">
        <h2 className="mb-6 text-3xl font-bold tracking-tight sm:text-4xl">
          Bereit, ein Local Hero zu werden?
        </h2>
        <p className="mx-auto mb-10 max-w-2xl text-lg opacity-90">
          Werde Teil unserer Community und mach deine Nachbarschaft zu einem besseren Ort. 
          Jede Hilfe zählt.
        </p>
        
        <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
          {isAuthenticated ? (
            <Link
              href="/dashboard"
              className="inline-flex h-12 w-full items-center justify-center rounded-md bg-background px-8 text-sm font-medium text-primary shadow transition-colors hover:bg-background/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 sm:w-auto"
            >
              Zum Dashboard
            </Link>
          ) : (
            <>
              <Link
                href="/register"
                className="inline-flex h-12 w-full items-center justify-center rounded-md bg-background px-8 text-sm font-medium text-primary shadow transition-colors hover:bg-background/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 sm:w-auto"
              >
                Jetzt registrieren
              </Link>
              <Link
                href="/login"
                className="inline-flex h-12 w-full items-center justify-center rounded-md border border-primary-foreground/20 bg-transparent px-8 text-sm font-medium text-primary-foreground shadow-sm transition-colors hover:bg-primary-foreground/10 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 sm:w-auto"
              >
                Anmelden
              </Link>
            </>
          )}
        </div>
      </div>
    </section>
  );
}
