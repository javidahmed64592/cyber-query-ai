<!-- omit from toc -->
# CyberQueryAI Frontend

A Next.js frontend for the CyberQueryAI cybersecurity assistant application.

<!-- omit from toc -->
## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Development](#development)
- [Project Structure](#project-structure)
- [Features](#features)
- [API Integration](#api-integration)
- [License](#license)

## Overview

This is the web interface for CyberQueryAI, providing an intuitive dark-themed UI for:

- Cybersecurity command generation
- Ethical penetration testing assistance
- Security research tool recommendations

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Theme**: Dark cybersecurity/hacker aesthetic
- **API Integration**: FastAPI backend via proxy

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Code quality checks
npm run quality:fix

# Production build
npm run build
```

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── command-generation/ # Main command generation interface
│   ├── layout.tsx         # Root layout with navigation
│   └── page.tsx           # Homepage (redirects to command-generation)
├── components/            # Reusable React components
│   ├── Navigation.tsx     # Main navigation bar
│   ├── PromptInput.tsx    # User input component
│   ├── CommandBox.tsx     # Generated command display
│   └── ExplanationBox.tsx # AI explanation display
└── lib/                   # Utilities and API client
    ├── api.ts            # API communication functions
    └── types.ts          # TypeScript type definitions
```

## Features

- **Command Generation**: AI-powered cybersecurity command suggestions
- **Dark Theme**: Hacker-inspired UI with neon accents
- **Responsive Design**: Works on desktop and mobile
- **Type Safety**: Full TypeScript integration
- **Code Quality**: ESLint, Prettier, and automated formatting

## API Integration

The frontend communicates with a FastAPI backend running on `localhost:8000`. API calls are proxied through Next.js for seamless integration.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
