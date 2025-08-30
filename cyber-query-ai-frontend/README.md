[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![ESLint](https://img.shields.io/badge/ESLint-9-4B32C3?style=for-the-badge&logo=eslint&logoColor=white)](https://eslint.org/)
[![Prettier](https://img.shields.io/badge/Prettier-3-F7B93E?style=for-the-badge&logo=prettier&logoColor=black)](https://prettier.io/)

[![CI](https://img.shields.io/github/actions/workflow/status/javidahmed64592/cyber-query-ai/ci.yml?branch=main&style=for-the-badge&label=CI&logo=github)](https://github.com/javidahmed64592/cyber-query-ai/actions)
[![License](https://img.shields.io/github/license/javidahmed64592/cyber-query-ai?style=for-the-badge)](https://github.com/javidahmed64592/cyber-query-ai/blob/main/LICENSE)

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
