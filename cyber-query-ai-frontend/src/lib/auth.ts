/**
 * Authentication utilities for API key management.
 */

const API_KEY_STORAGE_KEY = "cyberquery_api_key";

/**
 * Save API key to localStorage.
 */
export function saveApiKey(apiKey: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem(API_KEY_STORAGE_KEY, apiKey);
  }
}

/**
 * Get API key from localStorage.
 */
export function getApiKey(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem(API_KEY_STORAGE_KEY);
  }
  return null;
}

/**
 * Remove API key from localStorage.
 */
export function removeApiKey(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem(API_KEY_STORAGE_KEY);
  }
}

/**
 * Check if user is authenticated (has API key stored).
 */
export function isAuthenticated(): boolean {
  return getApiKey() !== null;
}
