# How to Install Hermes

## Prerequisites

- **Node.js** v18 or later (recommended: latest LTS)
- **npm** or **yarn** package manager
- **Git** installed and configured
- A supported OS: macOS, Linux, or Windows (WSL recommended)

## Installation

### 1. Clone the Repository

```bash
git clone git@github.com:rifaterdemsahin/hermes.git
cd hermes
```

### 2. Install Dependencies

```bash
npm install
```

Or with yarn:

```bash
yarn install
```

### 3. Configure Environment

Copy the example environment file and fill in your settings:

```bash
cp .env.example .env
```

Edit `.env` with your preferred editor and set the required values (API keys, model preferences, etc.).

### 4. Run Hermes

```bash
npm start
```

Or for development mode with hot reload:

```bash
npm run dev
```

## Verify Installation

Run the built-in health check to confirm everything is working:

```bash
npm test
```

You should see all checks pass. If something fails, double-check your `.env` configuration and that all prerequisites are installed.

## Updating

Pull the latest changes and reinstall dependencies:

```bash
git pull origin main
npm install
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `node: command not found` | Install Node.js from [nodejs.org](https://nodejs.org) |
| Dependency errors | Delete `node_modules` and run `npm install` again |
| API key errors | Check your `.env` file for correct keys |
| Permission denied (git) | Ensure your SSH key is added to GitHub |

## What to Do with Hermes

Once installed, Hermes is your AI-powered agent that can:

- **Chat & Answer Questions** — Ask anything and get intelligent, context-aware responses.
- **Execute Terminal Commands** — Hermes can run shell commands, build projects, and manage files on your behalf.
- **Search the Web** — Retrieve up-to-date information from the internet.
- **Read & Write Files** — Create, edit, and analyze files in your workspace.
- **Manage Tasks** — Track to-dos, plan multi-step workflows, and stay organized.
- **Generate Images** — Create visuals from text prompts.
- **Schedule Jobs** — Set up recurring tasks with cron-like scheduling.
- **Use Skills** — Load reusable procedures for common workflows (DevOps, ML, research, etc.).
- **Remember Context** — Hermes has persistent memory across sessions so it learns your preferences over time.
- **Delegate Work** — Spawn sub-agents for parallel or complex tasks.

### Getting Started Tips

1. Start by asking Hermes a simple question to test the connection.
2. Try a file operation: ask it to create or read a file.
3. Explore skills: type "list skills" to see what reusable workflows are available.
4. Set preferences: tell Hermes your name, coding style, or timezone — it will remember.
5. Automate: schedule a recurring task to see cron jobs in action.
