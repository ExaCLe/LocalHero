"use client";

import Link from "next/link";
import { useAuth } from "@/contexts/auth-context";

export function HeroSection() {
  const { isAuthenticated } = useAuth();

  return (
    <section className="relative flex h-screen min-h-[600px] w-full items-center overflow-hidden">
      {/* Video Background */}
      <video
        autoPlay
        loop
        muted
        playsInline
        className="absolute right-0 top-0 h-full w-full object-cover"
      >
        <source
          src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"
          type="video/mp4"
        />
        Your browser does not support the video tag.
      </video>

      {/* Dark Overlay for Readability */}
      <div className="absolute inset-0 bg-black/50 bg-gradient-to-r from-black/80 via-black/40 to-transparent" />

      <div className="container relative z-10 mx-auto px-4">
        <h1 className="max-w-4xl text-6xl font-black tracking-tighter text-white drop-shadow-xl sm:text-7xl md:text-8xl">
          Finde dein Match <br></br>für <span className="bg-gradient-to-r from-primary to-blue-400 bg-clip-text text-transparent">gute Taten</span>
        </h1>
        <p className="mt-8 max-w-xl text-xl font-light leading-relaxed text-gray-100 drop-shadow-md sm:text-2xl">
          LocalHero verbindet dich mit Projekten und Menschen, die Hilfe brauchen. 
          Wie eine Dating-App – nur für das Ehrenamt. Spontan, flexibel und mit Impact.
        </p>
        
        <div className="mt-12 flex flex-col items-start gap-6 sm:flex-row">
          {isAuthenticated ? (
            <Link
              href="/dashboard"
              className="group relative inline-flex h-14 w-full items-center justify-center overflow-hidden rounded-full bg-primary px-10 text-base font-bold text-primary-foreground shadow-lg shadow-primary/30 transition-all hover:scale-105 hover:shadow-xl hover:shadow-primary/40 sm:w-auto"
            >
              Projekte finden
            </Link>
          ) : (
            <Link
              href="/register"
              className="group relative inline-flex h-14 w-full items-center justify-center overflow-hidden rounded-full bg-primary px-10 text-base font-bold text-primary-foreground shadow-lg shadow-primary/30 transition-all hover:scale-105 hover:shadow-xl hover:shadow-primary/40 sm:w-auto"
            >
              Jetzt starten
            </Link>
          )}
          
          <Link
            href="/about"
            className="group relative inline-flex h-14 w-full items-center justify-center overflow-hidden rounded-full border border-white/30 bg-white/10 px-10 text-base font-bold text-white backdrop-blur-md transition-all hover:bg-white/20 hover:scale-105 sm:w-auto"
          >
            Mehr erfahren
          </Link>
        </div>
      </div>
    </section>
  );
}
