import {
  saveApiKey,
  getApiKey,
  removeApiKey,
  isAuthenticated,
} from "@/lib/auth";

describe("Auth Utils", () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
  });

  afterEach(() => {
    localStorage.clear();
  });

  describe("saveApiKey", () => {
    it("should save API key to localStorage", () => {
      const apiKey = "test-api-key-123";
      saveApiKey(apiKey);

      expect(localStorage.getItem("cyberquery_api_key")).toBe(apiKey);
    });

    it("should overwrite existing API key", () => {
      saveApiKey("old-key");
      saveApiKey("new-key");

      expect(localStorage.getItem("cyberquery_api_key")).toBe("new-key");
    });
  });

  describe("getApiKey", () => {
    it("should return API key from localStorage", () => {
      const apiKey = "test-api-key-123";
      localStorage.setItem("cyberquery_api_key", apiKey);

      expect(getApiKey()).toBe(apiKey);
    });

    it("should return null when no API key is stored", () => {
      expect(getApiKey()).toBeNull();
    });
  });

  describe("removeApiKey", () => {
    it("should remove API key from localStorage", () => {
      const apiKey = "test-api-key-123";
      localStorage.setItem("cyberquery_api_key", apiKey);

      removeApiKey();

      expect(localStorage.getItem("cyberquery_api_key")).toBeNull();
    });

    it("should not throw error when removing non-existent key", () => {
      expect(() => removeApiKey()).not.toThrow();
    });
  });

  describe("isAuthenticated", () => {
    it("should return true when API key exists", () => {
      localStorage.setItem("cyberquery_api_key", "test-key");

      expect(isAuthenticated()).toBe(true);
    });

    it("should return false when API key does not exist", () => {
      expect(isAuthenticated()).toBe(false);
    });

    it("should return false after removing API key", () => {
      localStorage.setItem("cyberquery_api_key", "test-key");
      removeApiKey();

      expect(isAuthenticated()).toBe(false);
    });
  });
});
