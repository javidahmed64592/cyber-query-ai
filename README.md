[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=ffd343)](https://docs.python.org/3.13/)
[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Ollama](https://img.shields.io/badge/Ollama-AI%20Models-FF6B6B?style=flat-square&logo=ollama&logoColor=white)](https://ollama.ai/)
[![Kali Linux](https://img.shields.io/badge/Kali%20Linux-Optimized-557C94?style=flat-square&logo=kalilinux&logoColor=white)](https://www.kali.org/)
[![CI](https://img.shields.io/github/actions/workflow/status/javidahmed64592/cyber-query-ai/ci.yml?branch=main&style=flat-square&label=CI&logo=github)](https://github.com/javidahmed64592/cyber-query-ai/actions/workflows/ci.yml)
[![Build](https://img.shields.io/github/actions/workflow/status/javidahmed64592/cyber-query-ai/build.yml?branch=main&style=flat-square&label=Build&logo=github)](https://github.com/javidahmed64592/cyber-query-ai/actions/workflows/build.yml)
[![License](https://img.shields.io/github/license/javidahmed64592/cyber-query-ai?style=flat-square)](https://github.com/javidahmed64592/cyber-query-ai/blob/main/LICENSE)

<!-- omit from toc -->
# CyberQueryAI

**Your AI-powered cybersecurity assistant for ethical hacking, penetration testing, and security research.**

CyberQueryAI transforms natural language into precise cybersecurity commands, scripts, and insights using advanced AI language models.
Designed specifically for cybersecurity professionals, ethical hackers, and security researchers, this tool dramatically increases productivity while fostering learning and growth within the cybersecurity community.

**Important: Ollama must be running locally on your system for this application to function.**

<!-- omit from toc -->
## Screenshots

**See CyberQueryAI in action!** These screenshots showcase the intuitive interface and powerful capabilities that make cybersecurity tasks faster and more accessible. Experience natural language command generation, comprehensive tool explanations, and seamless workflow integration - all designed to accelerate your security research and testing.

**AI Assistant Page:**
![AI Assistant Page - Shows the main interface for converting natural language to a variety of cybersecurity tasks](https://github.com/javidahmed64592/cyber-query-ai/blob/main/docs/screenshots/assistant.png "AI Assistant Page")

**Code Generation Page:**
![Code Generation Interface - Shows an interface for converting natural language to cybersecurity commands and scripts](https://github.com/javidahmed64592/cyber-query-ai/blob/main/docs/screenshots/code_generation.png "Code Generation Interface")

**About Page:**
![About Page - Displays comprehensive information about CyberQueryAI features and usage](https://github.com/javidahmed64592/cyber-query-ai/blob/main/docs/screenshots/about.png "About Page")

<!-- omit from toc -->
## Table of Contents
- [Why CyberQueryAI?](#why-cyberqueryai)
- [Key Features](#key-features)
  - [**AI Assistant (Conversational Interface)**](#ai-assistant-conversational-interface)
  - [**Intelligent Code Generation**](#intelligent-code-generation)
  - [**Code Analysis \& Explanation**](#code-analysis--explanation)
  - [**Exploit Research \& Discovery**](#exploit-research--discovery)
  - [**Security \& Sanitization**](#security--sanitization)
- [Web Application Pages](#web-application-pages)
  - [**AI Assistant** (`/`)](#ai-assistant-)
  - [**Code Generation** (`/code-generation`)](#code-generation-code-generation)
  - [**Code Explanation** (`/code-explanation`)](#code-explanation-code-explanation)
  - [**Exploit Search** (`/exploit-search`)](#exploit-search-exploit-search)
  - [**About** (`/about`)](#about-about)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Option 1: Using Pre-built Release (Recommended)](#option-1-using-pre-built-release-recommended)
    - [Option 2: From Source](#option-2-from-source)
  - [Configuration](#configuration)
- [Technology Stack](#technology-stack)
  - [Backend (Python)](#backend-python)
  - [Frontend (TypeScript/React)](#frontend-typescriptreact)
  - [Development \& Operations](#development--operations)
- [Documentation](#documentation)
- [Security Policy \& Ethics](#security-policy--ethics)
  - [Core Principles](#core-principles)
  - [Prohibited Uses](#prohibited-uses)
- [License](#license)

## Why CyberQueryAI?

Traditional cybersecurity work often involves memorizing complex command syntax, researching tool parameters, and manually crafting scripts for specific scenarios. CyberQueryAI eliminates these productivity bottlenecks by providing:

- **Instant Code Generation**: Convert natural language descriptions into precise CLI commands or multi-language scripts (Python, Bash, PowerShell, etc.) for tools like nmap, metasploit, john, hydra, and more
- **Educational Value**: Learn how security tools work through detailed explanations and examples
- **Vulnerability Research**: Discover known exploits and attack vectors relevant to specific targets
- **Time Savings**: Reduce command lookup time from minutes to seconds
- **Knowledge Transfer**: Bridge the gap between experienced professionals and newcomers to cybersecurity

Whether you're conducting authorized penetration tests, participating in CTF competitions, or learning cybersecurity fundamentals, CyberQueryAI accelerates your workflow while maintaining ethical standards.

## Key Features

### **AI Assistant (Conversational Interface)**
- **Primary interaction method** for natural, context-aware assistance
- Full conversation history maintained across your session
- Ask questions, request commands/scripts, and get explanations in one place
- Perfect for learning workflows and iterative problem-solving
- Code block rendering with syntax highlighting and copy functionality

### **Intelligent Code Generation**
- Natural language to code translation (CLI commands or scripts in Python, Bash, PowerShell, JavaScript, etc.)
- Context-aware parameter suggestions optimized for Kali Linux environments
- Support for network scanning, vulnerability assessment, password cracking, and more
- Tailored for cybersecurity use cases including exploit development, data parsing, and tool automation
- Complete with explanations to help you understand and modify the code
- Rate-limited API (5 requests/minute) to ensure responsible usage

### **Code Analysis & Explanation**
- Detailed breakdowns of complex commands and scripts with their parameters
- Security risk assessment and potential impact analysis
- Educational explanations to build your cybersecurity knowledge

### **Exploit Research & Discovery**
- Find known vulnerabilities and CVEs for specific targets
- Suggest attack vectors based on service descriptions
- Link to relevant exploit databases and proof-of-concept code
- Severity ratings and impact assessments

### **Security & Sanitization**
- All inputs and outputs are sanitized using `bleach` to prevent injection attacks
- Rate limiting prevents abuse and ensures fair usage
- CORS protection and secure API design
- Clear ethical guidelines and usage policies

## Web Application Pages

CyberQueryAI's intuitive web interface provides specialized tools for different cybersecurity workflows:

### **AI Assistant** (`/`)
The **primary interface** for interacting with CyberQueryAI - a conversational AI assistant with full chat history:

- **Conversational Experience**: Natural back-and-forth dialogue with context awareness
- **Universal Capability**: Can handle all types of requests (commands, scripts, explanations, exploit research)
- **Learning-Friendly**: Perfect for asking follow-up questions and iterative problem-solving
- **Code Rendering**: Beautiful syntax-highlighted code blocks with copy functionality
- **Example**: "How do I scan a network with nmap?" → Detailed explanation + follow-up questions like "Can you show me the stealth scan version?"

**Tip**: Start here for most tasks - the AI Assistant provides the most natural and flexible interaction model.

### **Code Generation** (`/code-generation`)
Focused interface for converting natural language into executable security code. The AI automatically infers whether to generate a command or a script:

- **Command Example**: "Scan a network for open ports" → `nmap -sS -O 192.168.1.0/24`
- **Script Example**: "Create a port scanner in Python" → Complete Python script with threading and error handling
- Supports multiple programming languages: Python, Bash, PowerShell, JavaScript, and more
- Includes explanations to help you understand the generated code

### **Code Explanation** (`/code-explanation`)
Understand complex security commands and scripts through detailed analysis. The AI automatically detects the code type:

- Parameter-by-parameter breakdowns for commands
- Line-by-line code analysis for scripts
- Security implications and risks
- Alternative approaches and variations
- Optimization suggestions and best practices
- **Command Example**: `nmap -sS -O 192.168.1.0/24` → Detailed explanation of SYN scan, OS detection, and target specification
- **Script Example**: Analyze a privilege escalation script to understand its methodology

### **Exploit Search** (`/exploit-search`)
Research known vulnerabilities and attack vectors:
- CVE lookups and exploit databases
- Attack vector suggestions for specific targets
- Severity assessments and impact analysis
- Links to proof-of-concept code and patches
- **Example**: "WordPress 5.4.2 with outdated plugins" → List of relevant CVEs and exploit techniques

### **About** (`/about`)
Comprehensive information about the application, including:
- Detailed feature explanations
- Security policies and ethical guidelines
- Usage best practices and safety reminders
- Technical implementation details

## Getting Started

### Prerequisites

1. **Ollama**: Download and install from [ollama.ai](https://ollama.ai/)
2. **Python 3.13+**: Required for the backend application
3. **AI Model**: Pull a compatible model using Ollama (e.g., `ollama pull mistral`)

**Note:** You can configure the LLMs used in the application by editing the `config.json` file.

### Installation

#### Option 1: Using Pre-built Release (Recommended)
1. Download the latest release from [GitHub Releases](https://github.com/javidahmed64592/cyber-query-ai/releases)
2. Extract the archive
3. Run the installer:
   - **Linux/macOS**: `./install_cyber_query_ai.sh`
   - **Windows**: `install_cyber_query_ai.bat`

#### Option 2: From Source
```bash
# Clone the repository
git clone https://github.com/javidahmed64592/cyber-query-ai.git
cd cyber-query-ai

# Install using uv (recommended)
uv sync --extra dev

# Or using pip
pip install -e .

# Build and run the frontend (optional for development)
cd cyber-query-ai-frontend
npm install
npm run dev
```

### Configuration

1. **Start Ollama**: Ensure Ollama is running locally:
   ```bash
   ollama serve
   ```

2. **Configure the model**: Edit `config.json` to specify your preferred AI model:
   ```json
   {
     "model": "mistral",
     "embedding_model": "bge-m3",
     "host": "localhost",
     "port": 8000
   }
   ```

   **Note:** This `config.json` file is the single source of truth for all configuration settings, including server host/port and AI model selection.

3. **Launch the application**:
   ```bash
   cyber-query-ai
   ```

4. **Access the web interface**: Open your browser to `http://localhost:8000`

## Technology Stack

### Backend (Python)
- **FastAPI**: High-performance async web framework with automatic API documentation
- **LangChain**: LLM integration and prompt management
- **Ollama**: Local AI model hosting and inference
- **Pydantic**: Data validation and serialization
- **SlowAPI**: Rate limiting for responsible usage
- **Bleach**: Input/output sanitization for security

### Frontend (TypeScript/React)
- **Next.js 16**: Modern React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling framework
- **Framer Motion**: Smooth animations and transitions
- **DOMPurify**: Client-side sanitization

### Development & Operations
- **pytest**: Comprehensive backend testing
- **Jest**: Frontend unit testing
- **Ruff**: Python code formatting and linting
- **ESLint/Prettier**: JavaScript/TypeScript code quality
- **GitHub Actions**: Automated CI/CD pipeline
- **uv**: Fast Python package management

## Documentation

Detailed documentation is available in the `docs/` directory:

- **[API.md](docs/API.md)**: Complete API endpoint documentation with examples
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: Technical architecture and component overview
- **[SMG.md](docs/SMG.md)**: Software maintenance guide for developers
- **[WORKFLOWS.md](docs/WORKFLOWS.md)**: CI/CD pipeline and development workflows

Additional resources:
- **[Security Policy](SECURITY.md)**: Vulnerability reporting and security guidelines
- **[Release Notes](release/readme.txt)**: Deployment and installation instructions

## Security Policy & Ethics

CyberQueryAI is designed exclusively for **ethical cybersecurity research**, **authorized penetration testing**, and **educational purposes**.

### Core Principles
- **Authorization Required**: Only use on systems you own or have explicit written permission to test
- **Educational Focus**: Designed to accelerate learning and skill development
- **Responsible Disclosure**: Follow proper vulnerability reporting procedures
- **Community Growth**: Foster knowledge sharing and collaboration

### Prohibited Uses
- Unauthorized access to computer systems
- Real-world exploitation or malicious activities
- Violation of computer crime laws or regulations
- Any activity that could cause harm to individuals or organizations

**By using CyberQueryAI, you agree to use it responsibly and ethically. Users are solely responsible for their actions and compliance with applicable laws.**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Ready to supercharge your cybersecurity workflow?** Install CyberQueryAI today and join the growing community of security professionals using AI to enhance their capabilities while maintaining the highest ethical standards.
