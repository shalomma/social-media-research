---
name: xai-grok
description: Use xAI's Grok model with agentic tool calling for X (Twitter) search, web search, code execution, and real-time data access. Invoke when user needs Twitter/X insights, current events, alternative perspectives, or complex multi-step research.
---

# xAI Grok Integration with Agentic Tool Calling

This skill enables Claude to delegate queries to xAI's Grok model with powerful agentic capabilities including real-time X (Twitter) search, web browsing, and code execution.

## When to Use This Skill

Use this skill when:
- User explicitly asks to use Grok or xAI
- User needs **real-time X (Twitter) search** - finding tweets, users, trends
- User requests "another opinion" or "alternative perspective"
- Query requires very recent information or current events
- User wants social media analysis or Twitter/X insights
- Task benefits from Grok's unique training and perspective
- Complex research requiring multiple tools (web search + code + Twitter)

## Core Capabilities

### 1. X (Twitter) Search
- **Semantic and keyword search** across X posts, users, and threads
- **User search** by name or handle
- **Thread fetching** for full conversation context
- **Real-time data** from the X platform

### 2. Web Search
- Real-time search across the internet
- Browse web pages and extract content

### 3. Code Execution
- Write and execute Python code
- Data analysis and complex computations
- Generate visualizations and process data

### 4. Agentic Orchestration
- **Server-side tool calling** - Grok autonomously decides which tools to use
- **Multi-step reasoning** - Combines multiple tools to answer complex queries
- **Streaming mode** - Real-time progress and observability (always used per xAI recommendation)
- **Citations** - Full traceability of information sources

## Usage

The skill uses the Python script located at `.claude/skills/xai-grok/scripts/grok.py`:

### Basic Usage (X Search + Web Search enabled by default)

```bash
source .venv/bin/activate && python .claude/skills/xai-grok/scripts/grok.py "Find recent tweets from Israeli tech nano-influencers"
```

### With All Tools Including Code Execution

```bash
source .venv/bin/activate && python .claude/skills/xai-grok/scripts/grok.py "Analyze tech trends with charts" --enable-code-execution
```

### Twitter/X Search Examples

```bash
# Find specific users
python .claude/skills/xai-grok/scripts/grok.py "Who are the top Israeli tech influencers on X?"

# Search for recent tweets
python .claude/skills/xai-grok/scripts/grok.py "Latest tweets about Israeli startups"

# Analyze trends
python .claude/skills/xai-grok/scripts/grok.py "What are Israeli tech companies tweeting about today?"
```

### Disable Specific Tools

```bash
# Only X search, no web search
python .claude/skills/xai-grok/scripts/grok.py "Find tweets" --disable-web-search

# Only web search, no X search
python .claude/skills/xai-grok/scripts/grok.py "Latest news" --disable-x-search

# No tools (basic chat)
python .claude/skills/xai-grok/scripts/grok.py "Explain AI" --disable-all-tools
```

### Available Options

```bash
--model grok-4                   # Model selection (default: grok-4)
--disable-x-search               # Disable X (Twitter) search (enabled by default)
--disable-web-search             # Disable web search (enabled by default)
--enable-code-execution          # Enable Python code execution (opt-in)
--disable-all-tools              # Disable all tools (basic chat mode)
--show-citations                 # Show source URLs (default: enabled)
--show-usage                     # Show token usage statistics
--show-tool-calls                # Show real-time tool calls
--temperature                    # Temperature for response generation (default: 0.7)
```

### Available Grok 4 Models

- `grok-4` - Highest quality model, 256k context [DEFAULT]
- `grok-4-fast-reasoning` - Cost-efficient with reasoning, 2M context
- `grok-4-fast-non-reasoning` - Cost-efficient without reasoning, 2M context

## Requirements

- Python virtual environment (`.venv`)
- `xai-sdk==1.3.1`
- `python-dotenv==1.1.1`
- XAI_API_KEY environment variable in project's .env file

## How It Works

When you invoke this skill with tools enabled, Grok uses **agentic tool calling**:

1. **Analyzes your query** to understand what information is needed
2. **Autonomously selects tools** - decides whether to search X, browse web, execute code, or combine multiple approaches
3. **Executes tools server-side** - no need for you to handle tool responses
4. **Iterates and refines** - uses tool results to make better decisions
5. **Returns comprehensive answer** with citations and sources

This means a single query like "What are Israeli tech companies tweeting about and how does it compare to global trends?" can automatically:
- Search X for Israeli tech company tweets
- Search the web for global tech trends
- Execute Python code to analyze patterns
- Synthesize everything into a comprehensive answer

## Output

The script provides:
- **Streaming responses** with real-time progress
- **Citations** - URLs of all sources Grok used
- **Tool call visibility** - See which tools Grok invoked (optional)
- **Token usage** - Detailed cost tracking (optional)

## Notes

- Grok responses are clearly indicated in output
- X search provides **real-time data** from the Twitter/X platform
- Citations show full traceability of information sources
- This is a supplementary tool; Claude remains the primary assistant
- API usage incurs costs on the user's xAI account
- **Streaming mode is always used** for agentic workflows (per xAI strong recommendation)
- Image/video understanding is **not supported** in this implementation
