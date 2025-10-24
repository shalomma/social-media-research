# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python-based social media research toolkit for discovering and tracking Israeli tech nano-influencers (<10K followers) on Twitter/X. The project integrates with xAI's Grok API for real-time Twitter search and RapidAPI for Twitter data access.

**Primary Purpose**: Strategic engagement tracking of nano-influencers in the Israeli tech ecosystem.

## Development Environment

**Package Management**: This project uses `uv` for Python dependency management.
- Install dependencies: `uv sync`
- Run Python scripts: `uv run python script.py`
- Python version: 3.13+

**Required Environment Variables** (`.env`):
- `XAI_API_KEY` - xAI Grok API key for Twitter search
- `RAPIDAPI_KEY` - RapidAPI key for Twitter API access

## Claude Code Skills

This repository includes two custom Claude Code skills in `.claude/skills/`:

### 1. xai-grok skill
Provides access to xAI's Grok-4 model with agentic tool calling capabilities:
- Real-time X (Twitter) search
- Web search and page browsing
- Optional Python code execution
- Streaming mode with tool call visibility

**Invocation**: Use the `Skill` tool with command `"xai-grok"`

**Script location**: `.claude/skills/xai-grok/scripts/grok.py`

**Key features**:
- Default model: `grok-4` (256k context)
- Alternative models: `grok-4-fast-reasoning`, `grok-4-fast-non-reasoning`
- X and web search enabled by default
- Code execution opt-in via `--enable-code-execution`

### 2. x-api skill
Python-based Twitter API client using RapidAPI endpoints via Typer CLI:
- User information retrieval by screenname
- User timeline (tweets) fetching
- Tweet search with filters (Top, Latest, Media, People, Lists)
- Reply retrieval

**Invocation**: Use the `Skill` tool with command `"x-api"`

**Script location**: `.claude/skills/x-api/scripts/client.py`

**Commands**:
- `user <screenname>` - Get user info
- `timeline <screenname>` - Get user's tweets
- `search <query> [--type TYPE]` - Search tweets
- `replies <screenname>` - Get user replies

## Claude Code Agents

### israeli-tech-influencer-finder
**Location**: `.claude/agents/israeli-tech-influencer-finder.md`

Specialized agent for discovering and tracking Israeli tech nano-influencers on Twitter/X.

**When to use**: Invoke when user wants to find Israeli tech influencers, expand network in Israeli startup scene, or engage with Hebrew-speaking tech professionals.

**Primary workflow**:
1. Uses `xai-grok` skill for direct Twitter/X searches (primary method)
2. Searches with Hebrew keywords: "טק", "היי-טק", "סטארטאפ", "יזם", "פיתוח"
3. Validates profiles: individual personas only, <10K followers, recent activity, Hebrew content
4. Maintains two markdown files:
   - `israeli-tech-nano-influencers.md` - Main influencer profiles
   - `israeli-tech-influencers-metadata.md` - Search history and analytics

**Key criteria**:
- INDIVIDUAL PERSONAS ONLY (not organizations/companies/media outlets)
- Follower count under 10,000
- Recent activity (within 7-14 days)
- Hebrew language content
- Tech/startup focus

## Repository Structure

```
.
├── .claude/
│   ├── agents/
│   │   └── israeli-tech-influencer-finder.md
│   ├── skills/
│   │   ├── x-api/
│   │   │   ├── SKILL.md
│   │   │   └── scripts/
│   │   │       └── client.py
│   │   └── xai-grok/
│   │       ├── SKILL.md
│   │       └── scripts/
│   │           └── grok.py
│   └── settings.local.json
├── israeli-tech-nano-influencers.md         # Main influencer database
├── israeli-tech-influencers-metadata.md     # Research metadata & analytics
├── pyproject.toml                            # Python project config
└── uv.lock                                   # Dependency lock file
```

## Key Dependencies

- `xai-sdk` (1.3.1) - xAI Grok API integration
- `typer` (0.20.0) - CLI framework for both skills
- `python-dotenv` - Environment variable management
- `openai` - OpenAI API client

## Working with the Skills

Both skills are implemented as Python scripts using Typer for CLI functionality. They can be invoked:

1. **Through Claude Code**: Use the `Skill` tool with commands `"xai-grok"` or `"x-api"`
2. **Directly from CLI**:
   - `uv run python .claude/skills/xai-grok/scripts/grok.py "query"`
   - `uv run python .claude/skills/x-api/scripts/client.py user screenname`

## Israeli Tech Ecosystem Context

When working with influencer data, be aware of:

- **Unit 8200 Influence**: ~80% of Israeli cybersecurity founders come from IDF intelligence units
- **Bilingual Culture**: Most tech professionals use both Hebrew and English
- **Tight-Knit Networks**: Strong personal connections from military service, Hebrew U, Technion
- **Global Orientation**: Strong ties to Silicon Valley, NYC, London tech scenes
- **Key Events**: Reversim Summit, DLD Tel Aviv, CyberTech
- **Major Companies**: Wix, Monday.com, Check Point, Waze alumni networks

## Research Workflow

1. Invoke `israeli-tech-influencer-finder` agent for discovery
2. Agent uses `xai-grok` skill for real-time Twitter searches
3. Agent validates profiles against criteria
4. Agent updates both markdown files with findings
5. User reviews and uses data for strategic engagement

## Important Notes

- The `.env` file contains API keys and is gitignored
- Research output files (markdown) are tracked in git
- All Twitter API access goes through either Grok (via xai-grok skill) or RapidAPI (via x-api skill)
- Focus on nano-influencers: follower counts must be verified to be under 10,000
- Individual personas only - organizations and media outlets are excluded from tracking