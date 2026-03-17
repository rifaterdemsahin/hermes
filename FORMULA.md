# Hermes Formula Document

## What is the Hermes Formula?

The Hermes Formula is a structured approach to getting the most out of the Hermes AI agent. It breaks down the workflow into repeatable patterns that maximize productivity.

## The Core Formula

```
Input (Task) → Context (Memory + Skills) → Execution (Tools) → Output (Result + Delivery)
```

### 1. Input: Define the Task

Every interaction starts with a clear task. Hermes works best when you:

- State what you want, not how to do it
- Provide relevant context (file paths, URLs, constraints)
- Specify the desired output format

**Formula:** `TASK = What + Where + How (output format)`

**Example:** "Create a Python script in /projects/api that fetches weather data and saves it as JSON."

### 2. Context: Leverage Memory & Skills

Hermes brings persistent context to every task:

- **Memory** — Your preferences, environment details, past corrections
- **Skills** — Reusable workflows for common tasks
- **Session History** — Searchable archive of past conversations

**Formula:** `CONTEXT = Memory + Skills + Session History`

**Tip:** Tell Hermes things once. It remembers your name, coding style, preferred tools, and project conventions.

### 3. Execution: Chain Tools Together

Hermes orchestrates multiple tools to complete tasks:

| Tool Category | Examples |
|---|---|
| Terminal | Shell commands, builds, installs, git |
| File Operations | Read, write, search, patch files |
| Web | Search, extract content from URLs |
| Browser | Navigate, click, fill forms, screenshot |
| Code Execution | Run Python scripts with tool access |
| Delegation | Spawn sub-agents for parallel work |
| Scheduling | Cron jobs for recurring tasks |

**Formula:** `EXECUTION = Tool₁ → Tool₂ → ... → Toolₙ`

Hermes automatically chains tools, handles errors, and retries when needed.

### 4. Output: Deliver Results

Results can be delivered to multiple platforms:

- **Terminal** — Direct response in CLI
- **Telegram** — Message to your Telegram chat
- **Discord** — Post to a Discord channel
- **Signal** — Send via Signal messenger
- **Files** — Save to disk (documents, code, images)

**Formula:** `OUTPUT = Result × Delivery Channel`

## The Productivity Formula

```
Productivity = (Tasks Completed × Quality) / Time Spent
```

With Hermes:

- **Tasks Completed** ↑ — Autonomous execution handles multiple steps
- **Quality** ↑ — Skills encode best practices, memory prevents repeated mistakes
- **Time Spent** ↓ — No context switching, parallel delegation, automation

## The Automation Formula

For recurring work, convert manual tasks into scheduled jobs:

```
Manual Task → Hermes Skill → Cron Job → Automated Delivery
```

**Steps:**
1. Do the task manually with Hermes once
2. Save the approach as a skill
3. Schedule it as a cron job
4. Receive results on your preferred platform

## The Delegation Formula

For complex tasks, split work across sub-agents:

```
Complex Task → Subtask₁ + Subtask₂ + Subtask₃ → Merge Results
```

**Rules:**
- Each subtask should be independent (no dependencies between them)
- Provide full context to each sub-agent (they have no shared memory)
- Maximum 3 parallel sub-agents per delegation

## The Memory Formula

Build Hermes' knowledge over time:

```
Correction → Memory Entry → Better Future Responses
```

**What to teach Hermes:**
- Your name, role, timezone
- Coding style preferences (tabs vs spaces, naming conventions)
- Project-specific conventions
- Tool preferences (yarn vs npm, vim vs nano)
- Communication style preferences

## The Skill Formula

Convert solved problems into reusable skills:

```
Problem Solved → Skill Created → Instant Recall Next Time
```

**Good skills include:**
- Trigger conditions (when to use this skill)
- Numbered steps with exact commands
- Pitfalls section (common errors and fixes)
- Verification steps (how to confirm success)

## Quick Reference

| Formula | Pattern |
|---|---|
| Core | Task → Context → Execution → Output |
| Productivity | (Tasks × Quality) / Time |
| Automation | Manual → Skill → Cron → Delivery |
| Delegation | Complex → Subtasks → Merge |
| Memory | Correction → Memory → Better Output |
| Skill | Problem → Skill → Instant Recall |

## Sending a Telegram Message

To send a test message via Telegram from Hermes:

1. Ensure Telegram is configured in `~/.hermes/config.yaml`
2. Use a cron job with `deliver: telegram` for one-time or recurring messages
3. Or interact with Hermes directly from your Telegram bot

**Example cron job for a test message:**
```
Schedule: once (1m delay)
Deliver: telegram
Prompt: "Hello from Hermes! This is a test message."
```

This is how the test message for this document was sent — via a scheduled one-time delivery to Telegram.
