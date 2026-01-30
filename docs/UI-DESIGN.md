# UI Design

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
