<!-- omit from toc -->
# Software Maintenance Guide

This document outlines how to configure and setup a development environment to work on the CyberQueryAI application.

<!-- omit from toc -->
## Table of Contents
- [Backend (Python)](#backend-python)
  - [Directory Structure](#directory-structure)
  - [Installing Dependencies](#installing-dependencies)
  - [Running the Backend](#running-the-backend)
  - [Testing, Linting, and Type Checking](#testing-linting-and-type-checking)
- [Frontend (TypeScript)](#frontend-typescript)
  - [Directory Structure](#directory-structure-1)
  - [Installing Dependencies](#installing-dependencies-1)
  - [Running the Frontend](#running-the-frontend)
  - [UI Design System](#ui-design-system)
    - [Color Palette](#color-palette)
    - [Typography](#typography)
    - [Visual Effects](#visual-effects)
    - [Component Styling Patterns](#component-styling-patterns)
    - [Layout Structure](#layout-structure)
    - [Responsive Design](#responsive-design)
    - [Key UI Patterns](#key-ui-patterns)
    - [Icons \& Emojis](#icons--emojis)
    - [Accessibility](#accessibility)
    - [Dependencies](#dependencies)
  - [Testing, Linting, and Type Checking](#testing-linting-and-type-checking-1)
- [Creating a New Release Version](#creating-a-new-release-version)
  - [Steps to Update Version](#steps-to-update-version)

## Backend (Python)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=ffd343)](https://docs.python.org/3.13/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=flat-square)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Langchain](https://img.shields.io/badge/Langchain-Latest-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://python.langchain.com/)

### Directory Structure

```
cyber_query_ai/
├── chatbot.py      # LLM integration with RAG support
├── helpers.py      # Utility functions (sanitization, JSON cleaning, static file serving, filepath helpers)
├── main.py         # Application entry point
├── models.py       # Pydantic models (requests, responses, config)
├── rag.py          # RAG system with semantic search
└── server.py       # CyberQueryAIServer class (extends TemplateServer)
```

### Installing Dependencies

This repository is managed using the `uv` Python project manager: https://docs.astral.sh/uv/

Install the required dependencies:

```sh
uv sync
```

To include development dependencies:

```sh
uv sync --extra dev
```

After installing dev dependencies, set up pre-commit hooks:

```sh
uv run pre-commit install
```

### Running the Backend

**Prerequisites:**
1. Ensure Ollama is running:
   ```sh
   ollama serve
   ```

2. Pull required models:
   ```sh
   ollama pull mistral
   ollama pull bge-m3
   ```

3. Generate API authentication token:
   ```sh
   uv run generate-new-token
   # Save the displayed token for authentication!
   ```

**Configuration:**
Edit `configuration/config.json` to customize server settings.

**Start the server:**
```sh
uv run cyber-query-ai
```

The backend will be available at `https://localhost:443` by default (HTTPS only).

### Testing, Linting, and Type Checking

- **Run all pre-commit checks:** `uv run pre-commit run --all-files`
- **Lint code:** `uv run ruff check .`
- **Format code:** `uv run ruff format .`
- **Type check:** `uv run mypy .`
- **Run tests:** `uv run pytest`
- **Security scan:** `uv run bandit -r cyber_query_ai/`
- **Audit dependencies:** `uv run pip-audit`


## Frontend (TypeScript)

[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat-square&logo=node.js&logoColor=white)](https://nodejs.org/)
[![ESLint](https://img.shields.io/badge/ESLint-9-4B32C3?style=flat-square&logo=eslint&logoColor=white)](https://eslint.org/)
[![Prettier](https://img.shields.io/badge/Prettier-3-F7B93E?style=flat-square&logo=prettier&logoColor=black)](https://prettier.io/)

### Directory Structure

```
cyber-query-ai-frontend/
├── src/
│   ├── app/
│   │   ├── about/               # About page
│   │   ├── code-explanation/    # Code explanation interface
│   │   ├── code-generation/     # Code generation interface
│   │   ├── exploit-search/      # Exploit search interface
│   │   ├── login/               # Login page for API key authentication
│   │   ├── 404/                 # Custom 404 page
│   │   ├── globals.css          # UI style configuration
│   │   ├── layout.tsx           # Root layout with AuthProvider and navigation
│   │   ├── not-found.tsx        # Not found page
│   │   └── page.tsx             # Homepage (AI Assistant with conversational chat)
│   ├── components/
│   │   ├── ChatMessage.tsx      # Individual message rendering with code blocks
│   │   ├── ChatWindow.tsx       # Conversational chat interface
│   │   ├── ErrorNotification.tsx # Portal-based error notifications
│   │   ├── ExplanationBox.tsx   # AI explanation display
│   │   ├── ExploitList.tsx      # Exploit references display
│   │   ├── Footer.tsx           # App footer with version info
│   │   ├── HealthIndicator.tsx  # Server health status indicator
│   │   ├── Navigation.tsx       # Main navigation bar with logout
│   │   ├── ScriptBox.tsx        # Generated code display
│   │   └── TextInput.tsx        # Text input component
│   ├── contexts/
│   │   └── AuthContext.tsx      # Authentication context and route protection
│   ├── lib/
│   │   ├── api.ts               # API client with authentication interceptors
│   │   ├── auth.ts              # localStorage API key management
│   │   ├── sanitization.ts      # Input/output sanitization utilities
│   │   └── types.ts             # TypeScript type definitions (matches backend models)
├── jest.config.js               # Jest configuration for testing
├── jest.setup.js                # Jest setup for mocking and environment
├── next.config.ts               # Next.js configuration
├── package.json                 # Dependencies and scripts
└── postcss.config.mjs           # Tailwind CSS configuration
```

### Installing Dependencies

Install the required dependencies:

```bash
npm install
```

### Running the Frontend

**Prerequisites:**
Ensure the backend server is running (see [Running the Backend](#running-the-backend))

**Start the development server:**
```bash
cd cyber-query-ai-frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`.

**Authentication in Development:**
- The development server proxies `/api` requests to the HTTPS backend (`https://localhost:443`)
- On first visit, you'll be redirected to `/login/`
- Enter the API token generated via `uv run generate-new-token`
- The token is stored in localStorage and included in all API requests via the `X-API-KEY` header

**Building for Production:**
```bash
npm run build        # Standard Next.js build
npm run build:static # Static export to ../static/ directory
```

### UI Design System

CyberQueryAI uses a **cybersecurity hacker theme** with a terminal-inspired aesthetic.
All styling is based on CSS custom properties defined in `src/app/globals.css`.

#### Color Palette

```css
/* Primary Colors */
--background: #0a0a0a;              /* Main background (very dark black) */
--foreground: #00ff41;              /* Primary text (matrix green) */
--background-secondary: #111111;    /* Secondary surfaces (cards, nav) */
--background-tertiary: #1a1a1a;     /* Tertiary surfaces (hover states) */

/* Border Colors */
--border: #333333;                  /* Default border (subtle gray) */
--border-accent: #00ff41;           /* Accent border (matrix green) */
--terminal-border: #30363d;         /* Terminal-style borders */

/* Text Colors */
--text-primary: #00ff41;            /* Primary text (matrix green) */
--text-secondary: #ffffff;          /* Secondary text (white) */
--text-muted: #888888;              /* Muted text (gray) */

/* Neon Accent Colors */
--neon-green: #00ff41;              /* Matrix green for emphasis */
--neon-purple: #bf00ff;             /* Purple for special highlights */
--neon-blue: #00bfff;               /* Cyan blue for links/actions */
--neon-red: #ff0040;                /* Red for errors/warnings */

/* Terminal Theme */
--terminal-bg: #0d1117;             /* Code blocks & terminal backgrounds */
```

#### Typography

- **Font Family**: `"JetBrains Mono", "Fira Code", "Consolas", monospace` (monospace for terminal aesthetic)
- **Base Font Size**: Browser default (16px)
- **Line Height**: 1.6 for body text
- **Headings**: Use `neon-glow` class for glowing text effect
- **Code**: Inline code uses `'Courier New', monospace` at 0.875rem

#### Visual Effects

**Neon Glow Effect** (`.neon-glow`):
```css
text-shadow: 0 0 1px currentColor, 0 0 1px currentColor, 0 0 2px currentColor;
```
- Applied to: Logo, headings, active navigation items, primary text

**Terminal Border Style** (`.terminal-border`):
```css
border: 1px solid var(--terminal-border);
background: var(--terminal-bg);
```
- Applied to: Input fields, code blocks, command outputs

**Neon Border Effect** (`.neon-border`):
```css
border: 1px solid var(--border-accent);
box-shadow: 0 0 5px var(--border-accent);
```
- Applied to: Focus states, active elements

**Custom Scrollbar**:
- Width: 8px
- Track: `--background-secondary`
- Thumb: `--border` (gray), `--border-accent` on hover (green glow)

**Animations**:
- `animate-pulse-neon`: Loading states with opacity pulse (1 → 0.5 → 1, 2s infinite)

#### Component Styling Patterns

**Cyber Input** (`.cyber-input`):
```css
background: var(--terminal-bg);
border: 1px solid var(--terminal-border);
color: var(--text-primary);
padding: 0.75rem;
border-radius: 0.375rem;
/* Focus state */
border-color: var(--border-accent);
box-shadow: 0 0 2px var(--border-accent);
```

**Cyber Button** (`.cyber-button`):
```css
background: var(--background-secondary);
border: 1px solid var(--border-accent);
color: var(--text-primary);
padding: 0.75rem 1.5rem;
border-radius: 0.375rem;
text-transform: uppercase;
letter-spacing: 0.05em;
/* Hover state */
background: var(--border-accent);
color: var(--background);
box-shadow: 0 0 2px var(--border-accent);
```

**Command Box** (`.command-box`):
```css
background: var(--terminal-bg);
border: 1px solid var(--terminal-border);
border-radius: 0.5rem;
padding: 1rem;
color: var(--text-secondary);
/* Used for code outputs, scripts, terminal-like content */
```

**Navigation Bar**:
- Sticky top positioning (`sticky top-0 z-50`)
- Background: `--background-secondary`
- Border bottom: `--terminal-border`
- Active items: Green text with `neon-glow` effect
- Inactive items: White text, hover to green

**Footer**:
- Fixed bottom positioning (`fixed bottom-0 left-0 right-0 z-40`)
- Terminal prompt style: `cyber@query:~$ ai --version=vX.X.X --model=mistral --rag_model=bge-m3`
- Background: `--background-secondary`
- Border top: `--terminal-border`

**Code Blocks** (ChatGPT-inspired):
```css
/* Wrapper */
margin: 1rem 0;
border-radius: 0.5rem;
background: var(--background);
border: 1px solid var(--terminal-border);

/* Header */
background: var(--background-tertiary);
padding: 0.5rem 0.75rem;
display: flex;
justify-content: space-between;
/* Shows language name and copy button */

/* Code Content */
padding: 1rem;
background: var(--background);
font-family: 'Courier New', monospace;
color: var(--neon-green);
font-size: 0.875rem;
```

**Inline Code**:
```css
background: var(--background-tertiary);
color: var(--neon-green);
padding: 0.125rem 0.375rem;
border-radius: 0.25rem;
border: 1px solid var(--border);
font-family: 'Courier New', monospace;
```

**Error Notifications** (Portal-based, top-right):
```css
position: fixed;
top: 1rem;
right: 1rem;
z-index: 9999;
background: var(--terminal-bg);
border: 2px solid var(--neon-red);
border-radius: 0.5rem;
padding: 1rem;
/* Includes ❌ icon and close button */
```

**Health Indicator** (Status Dot):
- Online: `background: var(--neon-green)` with green glow
- Offline: `background: var(--neon-red)` with red glow
- Checking: Yellow with pulse animation
- Size: 12px × 12px rounded circle

#### Layout Structure

**Page Layout**:
```tsx
<body>
  <AuthProvider>
    <div className="min-h-screen bg-[var(--background)]">
      <Navigation />  {/* Sticky top */}
      <main className="container mx-auto px-4 py-8 max-w-6xl pb-20">
        {children}
      </main>
      <Footer />  {/* Fixed bottom */}
    </div>
  </AuthProvider>
</body>
```

**Container Widths**:
- Standard content: `max-w-6xl` (1152px)
- Input/output sections: `max-w-4xl` (896px)
- Text content: `max-w-2xl` (672px)
- Login form: `max-w-md` (448px)

**Spacing**:
- Page padding: `px-4 py-8` (mobile), `sm:px-6 lg:px-8` (responsive)
- Section spacing: `space-y-8` (2rem vertical gap)
- Component spacing: `space-y-4` or `space-y-6` (1-1.5rem)
- Footer bottom padding: `pb-20` to prevent content overlap

#### Responsive Design

**Breakpoints** (Tailwind defaults):
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

**Mobile Navigation**:
- Hamburger menu below `lg` (1024px)
- Full-width mobile nav items with hover states
- Logo text size reduces on small screens
- Version badge hidden below `sm` (640px)

**Responsive Typography**:
- Headings scale down on mobile: `text-4xl` → `text-3xl` or `text-2xl`
- Logo: `text-xl` on mobile, `text-2xl` on desktop

#### Key UI Patterns

1. **Welcome/Empty States**: Large emoji (text-6xl), centered text, usage examples
2. **Loading States**: `animate-pulse-neon` with muted text ("Generating...", "Loading...")
3. **Error States**: Red neon border/text with ❌ icon
4. **Interactive Elements**: Uppercase text, letter-spacing, hover color transitions
5. **Chat Messages**: User messages right-aligned with blue accent, AI messages left-aligned with green
6. **Copy Buttons**: Small, secondary style with clipboard icon (📋), shows checkmark (✓) on copy

#### Icons & Emojis

- Uses native emojis for icons throughout (🧠, 🚀, 📜, 💬, ❌, ✓, 📋, etc.)
- No icon libraries required
- Emojis provide visual hierarchy and personality

#### Accessibility

- Focus states with green neon glow (`focus:ring-2 focus:ring-[var(--border-accent)]`)
- Semantic HTML structure
- ARIA labels for icon buttons (`aria-label="Close notification"`)
- Keyboard navigation support (Enter, Shift+Enter for chat)
- High contrast colors (white/green on black)

#### Dependencies

```json
{
  "dependencies": {
    "tailwindcss": "^4.1.16",
    "@tailwindcss/postcss": "^4.1.18",
    "dompurify": "^3.3.1",            // HTML sanitization
    "axios": "^1.13.2",               // API client
    "clsx": "^2.1.1",                 // Conditional classNames
    "framer-motion": "^12.26.0",      // Animations (if needed)
    "react-hot-toast": "^2.6.0",      // Toast notifications (backup)
    "zustand": "^5.0.10"              // State management (if needed)
  }
}
```

**Note**: Portal-based error notifications use `createPortal(component, document.body)` to avoid z-index stacking issues.

### Testing, Linting, and Type Checking

- **Run tests:** `npm run test`
- **Run all quality checks:** `npm run quality`
- **Fix all quality issues:** `npm run quality:fix`
- **Type check:** `npm run type-check`
- **Lint code:** `npm run lint`
- **Fix lint issues:** `npm run lint:fix`
- **Check formatting:** `npm run format`
- **Format code:** `npm run format:fix`

## Creating a New Release Version

When preparing a new release, you must update version numbers across multiple files to maintain consistency. The CI pipeline enforces version alignment between backend and frontend.

### Steps to Update Version

1. **Update `pyproject.toml`** (backend version):
   ```toml
   [project]
   name = "cyber-query-ai"
   version = "X.Y.Z"  # Update this line
   ```

2. **Update `cyber-query-ai-frontend/package.json`** (frontend version):
   ```json
   {
     "name": "cyber-query-ai-frontend",
     "version": "X.Y.Z"  // Update this line to match backend
   }
   ```

3. **Synchronize `uv.lock`** (from project root):
   ```sh
   uv lock
   ```

4. **Synchronize `package-lock.json`** (from `cyber-query-ai-frontend` directory):
   ```sh
   cd cyber-query-ai-frontend
   npm install --package-lock-only
   ```
