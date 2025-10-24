---
name: xai-grok
description: Use xAI's Grok model for specialized queries requiring up-to-date information, creative thinking, or alternative perspectives. Invoke when user explicitly requests Grok, asks for "another opinion", needs real-time data, or wants social media insights.
---

# xAI Grok Integration

This skill enables Claude to delegate queries to xAI's Grok model when appropriate.

## When to Use This Skill

Use this skill when:
- User explicitly asks to use Grok or xAI
- User requests "another opinion" or "alternative perspective"
- Query requires very recent information (Grok has real-time data access)
- User wants social media analysis or Twitter/X insights
- Task benefits from Grok's unique training and perspective

## Instructions

1. **Identify the Query**: Determine what question or prompt should be sent to Grok
2. **Run the Script**: Execute the `scripts/grok.py` script with the query as an argument
3. **Present Results**: Share Grok's response with the user, clearly indicating it came from Grok
4. **Handle Errors**: If the script fails, inform the user and suggest alternatives

## Usage

The skill uses the Python script located at `scripts/grok.py`. Pass the user's query as a command-line argument:

```bash
# Run with default model (grok-4-0709)
source .venv/bin/activate && python scripts/grok.py "Your query here"

# Or use a specific Grok 4 model
source .venv/bin/activate && python scripts/grok.py "Your query here" --model grok-4-fast-reasoning
```

### Available Grok 4 Models:
- `grok-4-0709` - Highest quality model, 256k context (default)
- `grok-4-fast-reasoning` - Cost-efficient with reasoning, 2M context
- `grok-4-fast-non-reasoning` - Cost-efficient without reasoning, 2M context

## Requirements

- Python virtual environment (`.venv`)
- Install dependencies: `pip install -r requirements.txt`
  - `openai>=1.0.0`
  - `python-dotenv>=1.0.0`
- XAI_API_KEY environment variable set in the project's .env file

## Notes

- Grok responses should be clearly attributed to xAI's Grok model
- This is a supplementary tool; Claude remains the primary assistant
- API usage incurs costs on the user's xAI account
