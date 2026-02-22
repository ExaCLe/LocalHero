"use client";

import Link from "next/link";
import Image from "next/image";
import { useState } from "react";
import { useAuth } from "../contexts/auth-context";
import { useTheme } from "../contexts/theme-context";

export default function Navbar() {
  const { isAuthenticated, login, logout, user } = useAuth();
  const { theme, setTheme } = useTheme();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Logo / Brand */}
        <div className="flex shrink-0 items-center">
          <Link href="/" className="flex items-center gap-2 font-bold text-xl text-primary">
            <Image src="/images/localhero-logo-first.png" alt="Logo" width={54} height={54} />
          </Link>
        </div>

        {/* Desktop Navigation */}
        <div className="hidden md:flex md:items-center md:gap-6">
          <Link href="/" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">
            Home
          </Link>
          <Link href="/about" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">
            About
          </Link>
          
          <div className="ml-4 flex items-center gap-4 border-l border-border pl-4">
             {/* Theme Toggle Button */}
            <button
               onClick={toggleTheme}
               className="rounded-md p-2 text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-colors"
               aria-label="Toggle theme"
            >
              { theme === 'dark' ? (
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
              ) : (
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
              )}
            </button>

            {isAuthenticated ? (
              <div className="flex items-center gap-4">
                <span className="text-sm font-medium text-foreground">
                  Hi, {user?.name?.split(" ")[0]}
                </span>
                <button
                  onClick={logout}
                  className="rounded-md bg-secondary px-4 py-2 text-sm font-medium text-secondary-foreground transition-colors hover:bg-secondary/80"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <>
                <button
                    onClick={login} 
                    className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
                >
                  Sign In
                </button>
                <button
                    onClick={login}
                    className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                >
                  Get Started
                </button>
              </>
            )}
          </div>
        </div>

        {/* Mobile Menu Button */}
        <div className="flex md:hidden items-center gap-4">
          <button
            onClick={toggleTheme}
            className="rounded-md p-2 text-muted-foreground hover:bg-accent hover:text-accent-foreground"
          >
             { theme === 'dark' ? (
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
              ) : (
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
              )}
          </button>
          <button
            type="button"
            className="inline-flex items-center justify-center rounded-md p-2 text-muted-foreground hover:bg-accent hover:text-accent-foreground"
            aria-controls="mobile-menu"
            aria-expanded={isMobileMenuOpen}
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            <span className="sr-only">Open main menu</span>
            {isMobileMenuOpen ? (
              <svg className="block h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="block h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden" id="mobile-menu">
          <div className="space-y-1 px-4 pt-2 pb-3 sm:px-3">
            <Link
              href="/"
              className="block rounded-md px-3 py-2 text-base font-medium text-foreground hover:bg-accent hover:text-accent-foreground"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Home
            </Link>
            <Link
              href="/about"
              className="block rounded-md px-3 py-2 text-base font-medium text-foreground hover:bg-accent hover:text-accent-foreground"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              About
            </Link>
          </div>
          <div className="border-t border-border pt-4 pb-4">
            {isAuthenticated ? (
              <div className="px-4">
                <div className="flex items-center">
                    <div className="text-base font-medium leading-none text-foreground">{user?.name}</div>
                    <div className="ml-2 text-sm font-medium leading-none text-muted-foreground">{user?.email}</div>
                </div>
                <div className="mt-3 space-y-1">
                  <button
                    onClick={() => {
                        logout();
                        setIsMobileMenuOpen(false);
                    }}
                    className="block w-full rounded-md px-3 py-2 text-left text-base font-medium text-muted-foreground hover:bg-accent hover:text-foreground"
                  >
                    Sign Out
                  </button>
                </div>
              </div>
            ) : (
               <div className="space-y-1 px-4">
                  <button
                      onClick={() => {
                          login();
                          setIsMobileMenuOpen(false);
                      }}
                       className="block w-full rounded-md px-3 py-2 text-base font-medium text-muted-foreground hover:bg-accent hover:text-foreground text-left"
                  >
                        Sign In
                  </button>
                  <button
                      onClick={() => {
                          login();
                          setIsMobileMenuOpen(false);
                      }}
                       className="block w-full rounded-md bg-primary px-3 py-2 text-base font-medium text-primary-foreground hover:bg-primary/90 text-left"
                  >
                        Get Started
                  </button>
               </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
