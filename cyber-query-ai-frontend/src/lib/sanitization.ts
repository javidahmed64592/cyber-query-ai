import DOMPurify from "dompurify";

/**
 * Sanitizes user input by escaping HTML characters to prevent XSS attacks
 * @param input - The raw user input string
 * @returns Sanitized string safe for backend processing
 */
export function sanitizeInput(input: string): string {
  if (!input) return "";

  // Escape HTML characters
  return input.replace(/[&<>"']/g, char => {
    switch (char) {
      case "&":
        return "&amp;";
      case "<":
        return "&lt;";
      case ">":
        return "&gt;";
      case '"':
        return "&quot;";
      case "'":
        return "&#39;";
      default:
        return char; // Fallback, though regex ensures only matched chars
    }
  });
}

/**
 * Sanitizes HTML content for safe rendering in the DOM
 * @param html - The HTML string to sanitize
 * @returns Sanitized HTML string safe for rendering
 */
export function sanitizeOutput(html: string): string {
  if (!html) return "";

  // Use DOMPurify to clean any potentially dangerous HTML
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [], // No HTML tags allowed, only text
    ALLOWED_ATTR: [], // No attributes allowed
  });
}

/**
 * Checks if a command contains potentially dangerous patterns
 * @param command - The command string to check
 * @returns True if the command appears safe, false if potentially dangerous
 */
export function isCommandSafe(command: string): boolean {
  if (!command) return true;

  const riskyPatterns = [
    "rm -rf",
    ":(){",
    "shutdown",
    "mkfs",
    "dd if=",
    "curl | sh",
    "wget | sh",
    "chmod 777",
    "sudo rm",
    "format",
    "del /f /s /q",
    "rd /s /q",
    "powershell -c",
    "cmd /c",
    "bash -c",
    "sh -c",
    "eval(",
    "exec(",
    "system(",
    "popen(",
  ];

  return !riskyPatterns.some(pattern =>
    command.toLowerCase().includes(pattern.toLowerCase())
  );
}
