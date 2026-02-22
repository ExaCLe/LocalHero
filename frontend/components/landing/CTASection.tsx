"use client";

import Link from "next/link";
import { useAuth } from "@/contexts/auth-context";
import { ArrowRight } from "lucide-react";

export function CTASection() {
  const { isAuthenticated } = useAuth();

  return (
    <section className="relative overflow-hidden py-24 sm:py-32">
      {/* Immersive Dark Gradient Background */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-blue-950 via-primary to-indigo-900" />
      
      {/* Abstract Noise/Texture Overlay (simulated with CSS pattern) */}
      <div className="absolute inset-0 -z-10 opacity-[0.03] mix-blend-overlay bg-[url('https://grainy-gradients.vercel.app/noise.svg')]" />
      
      {/* Decorative large glowing blobs */}
      <div className="absolute left-0 top-0 -z-10 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-blue-500/30 blur-[120px]" />
      <div className="absolute right-0 bottom-0 -z-10 h-[400px] w-[400px] translate-x-1/3 translate-y-1/3 rounded-full bg-indigo-500/30 blur-[120px]" />

      <div className="container relative z-10 mx-auto px-4 text-center">
        <h2 className="mb-6 drop-shadow-sm text-4xl font-black tracking-tight text-white sm:text-5xl md:text-6xl">
          Bereit, ein <span className="bg-gradient-to-r from-blue-200 to-white bg-clip-text text-transparent">Local Hero</span> zu werden?
        </h2>
        <p className="mx-auto mb-12 max-w-2xl text-xl font-light leading-relaxed text-blue-100/90">
          Werde Teil unserer Community und mach deine Nachbarschaft zu einem besseren Ort. 
          Jede Hilfe zählt und jeder Einsatz macht einen Unterschied.
        </p>
        
        <div className="flex flex-col items-center justify-center gap-5 sm:flex-row">
          {isAuthenticated ? (
            <Link
              href="/dashboard"
              className="group relative inline-flex h-14 w-full items-center justify-center overflow-hidden rounded-full bg-white px-10 text-base font-bold text-primary shadow-xl transition-all duration-300 hover:scale-[1.03] hover:bg-gray-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/50 sm:w-auto"
            >
              Zum Dashboard
              <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
            </Link>
          ) : (
            <>
              <Link
                href="/register"
                className="group relative inline-flex h-14 w-full items-center justify-center overflow-hidden rounded-full bg-white px-10 text-base font-bold text-primary shadow-xl transition-all duration-300 hover:scale-[1.03] hover:shadow-2xl hover:shadow-white/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/50 sm:w-auto"
              >
                Jetzt registrieren
                <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Link>
              <Link
                href="/login"
                className="group relative inline-flex h-14 w-full items-center justify-center overflow-hidden rounded-full border-2 border-white/20 bg-white/5 px-10 text-base font-bold text-white shadow-lg backdrop-blur-md transition-all duration-300 hover:border-white/40 hover:bg-white/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/50 sm:w-auto"
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
