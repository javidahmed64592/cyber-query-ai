"use client";

import { useRouter, usePathname } from "next/navigation";
import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useRef,
} from "react";

import { login as apiLogin } from "@/lib/api";
import { getApiKey, saveApiKey, removeApiKey } from "@/lib/auth";
import type { AuthContextType } from "@/lib/types";

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [apiKey, setApiKey] = useState<string | null>(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const router = useRouter();
  const pathname = usePathname();
  const hasRedirected = useRef(false);

  // Initialize API key from localStorage
  useEffect(() => {
    const initializeAuth = () => {
      const storedKey = getApiKey();
      setApiKey(storedKey);
      setIsInitialized(true);
    };

    initializeAuth();
  }, []);

  // Redirect logic after initialization
  useEffect(() => {
    if (!isInitialized) return;

    const isLoginPage = pathname === "/login/";
    const isAuthenticated = apiKey !== null;

    // Redirect to login if not authenticated and not on login page
    if (!isAuthenticated && !isLoginPage && !hasRedirected.current) {
      hasRedirected.current = true;
      router.replace("/login/");
      return;
    }

    // Redirect to assistant page if authenticated and on login page
    if (isAuthenticated && isLoginPage && !hasRedirected.current) {
      hasRedirected.current = true;
      router.replace("/assistant/");
      return;
    }

    // Reset redirect flag when on correct page
    if (
      (isAuthenticated && !isLoginPage) ||
      (!isAuthenticated && isLoginPage)
    ) {
      hasRedirected.current = false;
    }
  }, [isInitialized, apiKey, pathname, router]);

  const login = async (newApiKey: string): Promise<void> => {
    // Test API key by calling login endpoint
    await apiLogin(newApiKey);

    // If successful, save and update state
    saveApiKey(newApiKey);
    setApiKey(newApiKey);

    // Explicitly redirect to assistant page
    router.replace("/assistant/");
  };

  const logout = (): void => {
    removeApiKey();
    setApiKey(null);
    router.replace("/login/");
  };

  const value: AuthContextType = {
    apiKey,
    isAuthenticated: apiKey !== null,
    login,
    logout,
  };

  // Show a loading state during initialization and redirects
  if (!isInitialized) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-4 border-neon-blue border-t-transparent rounded-full mx-auto"></div>
          <p className="mt-4 text-text-muted">Loading...</p>
        </div>
      </div>
    );
  }

  // Show loading state while redirecting unauthenticated users
  if (!apiKey && pathname !== "/login/") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-4 border-neon-blue border-t-transparent rounded-full mx-auto"></div>
          <p className="mt-4 text-text-muted">Redirecting to login...</p>
        </div>
      </div>
    );
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
