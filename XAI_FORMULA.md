# Hermes xAI (Grok) Integration Formula

## What is xAI (Grok)?

xAI is Elon Musk's AI company that developed the Grok series of large language models. Grok models are known for:

- **Real-time knowledge**: Access to X (Twitter) data
- **Rebellious personality**: Witty and less filtered responses
- **Strong reasoning**: Excellent at math, coding, and logical tasks
- **Open-source availability**: Several variants available for local deployment

## Current xAI Models Available

| Model | Type | Use Case |
|-------|------|----------|
| **Grok-2** | 270B parameters | General purpose, reasoning, coding |
| **Grok-2 Beta** | 270B | Latest with vision capabilities |
| **Grok-1** | 314B | Original model |
| **Grok-2 Mini** | Smaller | Faster inference, lower cost |

## Hermes Integration Formula

```
Task → XAI_API_KEY → Grok Model → Result
```

### The Core Formula

```python
Input (Question/Task) 
  → Context (Memory + Skills) 
  → XAI_API_KEY (Grok Authentication) 
  → Execution (Grok API Call) 
  → Output (Grok Response)
```

## Quick Setup Formula

### Step 1: Add API Key to Doppler

```bash
doppler secrets set --project hermes --config dev -- XAI_API_KEY='your-api-key'
```

### Step 2: Use with Hermes

```bash
# Run commands with Grok available
doppler run --config dev --project hermes -- python your-script.py
```

### Step 3: Configure in Code

```python
import os

# Access Grok API key from environment
xai_key = os.getenv('XAI_API_KEY')

if not xai_key:
    raise ValueError("XAI_API_KEY not found in environment")

# Use with xAI SDK or direct API calls
from xai import XAI

client = XAI(api_key=xai_key)
response = client.chat.completions.create(
    model="grok-2",
    messages=[{"role": "user", "content": "Hello, Grok!"}]
)
```

## Usage Patterns Formula

### 1. Direct API Access Pattern

```python
import requests

def ask_grok(question: str, model: str = "grok-2") -> str:
    """Ask Grok a question using direct API call."""
    
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7,
        "max_tokens": 4096
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

# Usage
answer = ask_grok("What's the latest on SpaceX Starship?")
```

### 2. Reasoning & Math Pattern

```python
def grok_math_reasoning(problem: str) -> str:
    """Use Grok for complex math and reasoning problems."""
    
    prompt = f"""
    Solve this step-by-step:
    {problem}
    
    Show all your reasoning work clearly.
    """
    
    return ask_grok(prompt, model="grok-2-beta")
```

### 3. Coding Assistant Pattern

```python
def grok_code_review(code: str, language: str = "python") -> str:
    """Use Grok for code review and suggestions."""
    
    prompt = f"""
    Review this {language} code for:
    1. Bugs and errors
    2. Performance issues
    3. Security vulnerabilities
    4. Best practices
    5. Readability improvements
    
    Code:
    {code}
    
    Provide specific suggestions with code examples.
    """
    
    return ask_grok(prompt, model="grok-2")
```

### 4. Real-time Information Pattern

```python
def grok_realtime_query(topic: str) -> str:
    """Leverage Grok's access to X (Twitter) data."""
    
    prompt = f"""
    What's the latest information about {topic}?
    Include recent developments and trending discussions.
    """
    
    return ask_grok(prompt, model="grok-2-beta")
```

## Hermes Skill Formula

Create a reusable skill for xAI integration:

```yaml
name: grok-integration
category: ai-models
description: Use xAI Grok models for various tasks

steps:
  1. Verify XAI_API_KEY is loaded from Doppler
  2. Select appropriate Grok model based on task complexity
  3. Format prompt with clear instructions
  4. Make API call with proper error handling
  5. Process and return results

pitfalls:
  - Rate limiting: Grok has request limits, implement backoff
  - Context window: Respect model's token limits
  - Cost tracking: Monitor API usage for billing

verification:
  - Test with simple query first
  - Check response format
  - Verify error handling works
```

## Model Selection Formula

| Task Type | Recommended Model | Reason |
|-----------|-------------------|--------|
| General Chat | `grok-2` | Balanced performance |
| Complex Reasoning | `grok-2-beta` | Enhanced capabilities |
| Math/Science | `grok-2` | Strong reasoning |
| Coding | `grok-2` | Good code understanding |
| Real-time Info | `grok-2-beta` | X data access |
| Fast Response | `grok-2-mini` | Lower latency |
| Vision Tasks | `grok-2-beta` | Multi-modal support |

## Error Handling Formula

```python
from requests import RequestException, Timeout

def safe_grok_call(question: str, retries: int = 3) -> str:
    """Safe Grok call with retry logic and error handling."""
    
    for attempt in range(retries):
        try:
            response = ask_grok(question)
            return response
            
        except Timeout:
            if attempt == retries - 1:
                raise Exception("Grok API timeout after retries")
            time.sleep(2 ** attempt)  # Exponential backoff
            
        except RequestException as e:
            if attempt == retries - 1:
                raise Exception(f"Grok API error: {e}")
            time.sleep(2 ** attempt)
            
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")
```

## Cost Optimization Formula

```python
def optimize_grok_cost(task: str) -> str:
    """Choose the right model for the task to optimize cost."""
    
    # Simple queries → mini model
    if len(task) < 100 and "quick" in task.lower():
        return "grok-2-mini"
    
    # Complex reasoning → full model
    if "math" in task.lower() or "reasoning" in task.lower():
        return "grok-2-beta"
    
    # Default to balanced model
    return "grok-2"
```

## Integration with Other Tools

### Combined with Firecrawl

```python
def grok_web_research(query: str) -> str:
    """Combine Firecrawl with Grok for deep web research."""
    
    # 1. Crawl relevant pages
    crawled_data = firecrawl_crawl(query)
    
    # 2. Summarize with Grok
    prompt = f"""
    Based on this crawled data, summarize the key findings:
    
    {crawled_data}
    
    Provide a comprehensive summary with sources.
    """
    
    return ask_grok(prompt)
```

### Combined with ElevenLabs

```python
def grok_voice_response(question: str) -> str:
    """Get Grok response and convert to speech."""
    
    # 1. Get text response from Grok
    text_response = ask_grok(question)
    
    # 2. Convert to speech
    audio = elevenlabs_speech(text_response)
    
    # 3. Return audio
    return audio
```

## Debugging Formula

### Check API Key

```bash
# Verify XAI_API_KEY is set in Doppler
doppler secrets get XAI_API_KEY --project hermes --config dev

# Or check in current environment
doppler run --config dev --project hermes -- env | grep XAI
```

### Test Connection

```python
def test_xai_connection():
    """Test xAI API connection."""
    
    try:
        response = ask_grok("Say 'hello' in 5 words or less")
        print(f"✓ Connection successful: {response}")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False
```

## Best Practices Formula

1. **Key Security**: Never commit XAI_API_KEY to version control
2. **Error Handling**: Always implement retry logic and timeouts
3. **Rate Limiting**: Implement exponential backoff for rate limits
4. **Token Monitoring**: Track token usage to avoid unexpected costs
5. **Prompt Engineering**: Use clear, specific prompts for best results
6. **Model Selection**: Choose the right model for each task
7. **Caching**: Cache repeated queries to reduce API calls

## Cost Estimation Formula

```python
def estimate_grok_cost(tokens: int, model: str = "grok-2") -> float:
    """Estimate cost for given token count."""
    
    # Pricing per 1M tokens (approximate)
    pricing = {
        "grok-2": 2.50,
        "grok-2-beta": 5.00,
        "grok-2-mini": 0.50
    }
    
    tokens_millions = tokens / 1_000_000
    return tokens_millions * pricing.get(model, 2.50)

# Example
cost = estimate_grok_cost(10000, "grok-2")
print(f"Cost for 10k tokens: ${cost:.4f}")
```

## Troubleshooting Formula

| Issue | Solution |
|-------|----------|
| **Authentication failed** | Verify XAI_API_KEY in Doppler is correct |
| **Rate limit exceeded** | Implement exponential backoff, use mini model |
| **Timeout errors** | Increase timeout, check network connection |
| **Invalid model** | Use one of: grok-2, grok-2-beta, grok-2-mini |
| **Response truncated** | Check token limits, use smaller prompts |
| **High costs** | Use mini model, implement caching, track usage |

## Quick Reference

### Available Models
- `grok-2` - Standard model
- `grok-2-beta` - Enhanced with vision
- `grok-2-mini` - Fast and cheap

### Common Parameters
```python
{
    "model": "grok-2",
    "temperature": 0.7,
    "max_tokens": 4096,
    "top_p": 1.0,
    "frequency_penalty": 0.0
}
```

### API Endpoint
```
POST https://api.x.ai/v1/chat/completions
```

### Environment Variable
```bash
XAI_API_KEY=xai-...
```

## Next Steps Formula

```
1. ✓ Add XAI_API_KEY to Doppler
2. Test basic query
3. Create custom skill for your use case
4. Implement error handling
5. Monitor usage and costs
6. Optimize based on results
```

---

For more information:
- xAI API Documentation: https://docs.x.ai/
- Grok Models: https://x.ai/blog/grok-2
- Hermes Doppler Setup: See SETUP_GUIDE.md
