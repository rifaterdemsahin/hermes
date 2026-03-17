# Hermes Project Setup Guide

This document provides step-by-step instructions for setting up the Hermes project after cloning.

## Prerequisites

1. **Doppler CLI installed**
   ```bash
   # macOS
   brew install doppler

   # Ubuntu/Debian
   curl -L https://packagecloud.io/install/repositories/dopplerhq/doppler/script.deb.sh | sudo bash
   sudo apt-get install doppler

   # or via pip
   pip install doppler-cli
   ```

2. **Doppler account**
   - Sign up at https://dashboard.doppler.com
   - Get your API token from Settings → API Tokens

3. **Doppler CLI authentication**
   ```bash
   doppler login
   ```
   - Follow the interactive prompts to authenticate
   - You can also use environment variables:
     ```bash
     export DOPPLER_TOKEN=<your-token>
     ```

## Step 1: Clone the Project

```bash
git clone <repository-url>
cd hermes
```

## Step 2: Load Doppler Configuration

The Hermes project uses Doppler for secrets management. Here are the available environments:

### Available Environments
- `dev` - Development environment
- `dev_personal` - Personal development environment  
- `stg` - Staging environment
- `prd` - Production environment

### Load Secrets for Dev Environment (Recommended)

```bash
# Load all secrets for the dev environment
doppler run --config dev --project hermes -- <your-command>

# Example: Run the main application
doppler run --config dev --project hermes -- python app.py

# Example: Run tests
doppler run --config dev --project hermes -- pytest

# Example: Start a development server
doppler run --config dev --project hermes -- npm start
```

### Download Secrets to File (for manual inspection or CI/CD)

```bash
# Download secrets to a local file
doppler secrets download --config dev --project hermes --format env --no-file > .env.local

# Download as JSON (encrypted)
doppler secrets download --config dev --project hermes --format json
```

## Step 3: Verify Secrets Are Loaded

```bash
# Run a command with all secrets available
doppler run --config dev --project hermes -- env | grep -E '(GEMINI|OPENROUTER|ANTHROPIC|API)'

# Expected output includes:
# - GEMINI_API_KEY
# - OPENROUTER_API_KEY
# - ANTHROPIC_API_KEY
# - And any other configured secrets
```

## Step 4: Using Secrets in Your Code

### Environment Variables

Doppler injects secrets as environment variables automatically when using `doppler run`:

```python
import os

# Access secrets directly from environment
gemini_key = os.getenv('GEMINI_API_KEY')
openrouter_key = os.getenv('OPENROUTER_API_KEY')
anthropic_key = os.getenv('ANTHROPIC_API_KEY')

# Use in your application
```

### Node.js/TypeScript

```javascript
const geminiKey = process.env.GEMINI_API_KEY;
const openrouterKey = process.env.OPENROUTER_API_KEY;
const anthropicKey = process.env.ANTHROPIC_API_KEY;
```

### Shell Scripts

```bash
#!/bin/bash
# Run your script with Doppler secrets
doppler run --config dev --project hermes -- ./your-script.sh
```

## Common Doppler Commands Reference

### Manage Secrets

```bash
# Get specific secret
doppler secrets get API_KEY --project hermes --config dev

# Set a new secret
doppler secrets set API_KEY="new-value" --project hermes --config dev

# Delete a secret
doppler secrets delete API_KEY --project hermes --config dev

# List all secrets
doppler secrets ls --project hermes --config dev
```

### Project Management

```bash
# List available configs
doppler configs --project hermes

# Get project info
doppler projects get hermes

# Open Doppler dashboard
doppler open --project hermes --config dev
```

### Run Commands with Secrets

```bash
# Run any command with secrets injected
doppler run --config dev --project hermes -- <your-command>

# Run interactive shell with secrets
doppler run --config dev --project hermes -- bash

# Run with debug output
doppler run --config dev --project hermes --debug -- <command>
```

## AI API Keys Available

The following AI API keys are configured in the `dev` environment:

| Secret Name | Provider | Description |
|-------------|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini | Google's AI model API |
| `OPENROUTER_API_KEY` | OpenRouter | Unified API for multiple models |
| `ANTHROPIC_API_KEY` | Anthropic | Claude API access |

### Usage Examples

#### Gemini
```python
from google import genai

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
response = client.models.generate_content(
    model='gemini-1.5-flash',
    contents='Hello, world!'
)
```

#### OpenRouter
```python
import requests

response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {os.getenv("OPENROUTER_API_KEY")}',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'mistralai/mistral-7b-instruct',
        'messages': [{'role': 'user', 'content': 'Hello'}]
    }
)
```

#### Anthropic
```python
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Environment-Specific Notes

### Development (`dev`)
- Intended for local development
- Uses development credentials
- Lower rate limits, more permissive settings

### Staging (`stg`)
- Pre-production environment
- Mirrors production more closely
- Use for final testing before deployment

### Production (`prd`)
- Live production environment
- Use with caution
- Proper access controls required

## Troubleshooting

### Common Issues

1. **Authentication Error**
   ```
   Error: authentication failed
   ```
   Solution: Run `doppler login` again or check `DOPPLER_TOKEN` environment variable

2. **Secret Not Found**
   ```
   Error: secret not found
   ```
   Solution: Verify the secret name and environment config

3. **Permission Denied**
   ```
   Error: insufficient permissions
   ```
   Solution: Check your Doppler token has access to the project

### Debug Mode

Enable debug output for troubleshooting:
```bash
doppler run --debug --config dev --project hermes -- <command>
```

### Offline Mode

If you need to work without internet access:
```bash
# Download secrets once while online
doppler secrets download --config dev --project hermes --format env --no-file > secrets.env

# Use offline mode for subsequent runs
doppler run --offline --config dev --project hermes -- <command>
```

## Security Best Practices

1. **Never commit secrets to version control**
   - Add `.env` files to `.gitignore`
   - Never push `doppler.env` or `doppler.json` files

2. **Use appropriate environments**
   - Never use production secrets in development
   - Rotate API keys regularly

3. **Limit access**
   - Only share secrets with authorized team members
   - Use different tokens for different environments

4. **Audit usage**
   - Regularly check `doppler activity` for access logs
   - Monitor API key usage in provider dashboards

## Quick Reference Card

```bash
# Login
doppler login

# Load and run command
doppler run --config dev --project hermes -- npm run dev

# Get all secrets as environment variables
doppler secrets download --config dev --project hermes --format env

# Add new secret
doppler secrets set NEW_SECRET=value --config dev --project hermes

# View secrets list
doppler secrets ls --config dev --project hermes

# Open dashboard
doppler open --config dev --project hermes

# Check activity
doppler activity --project hermes
```

---

For more information, visit the official Doppler documentation:
https://docs.doppler.com/

Or open the Doppler dashboard:
https://dashboard.doppler.com/workplace/5ccb59c6d72db414f3e7/projects/hermes
