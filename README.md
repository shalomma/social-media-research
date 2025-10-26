# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python-based social media research toolkit for discovering and tracking Israeli tech nano-influencers (<10K followers) on Twitter/X. The project integrates with xAI's Grok API for real-time Twitter search, RapidAPI for Twitter data access, and maintains a SQLite database for organized influencer management.

**Primary Purpose**: Strategic engagement tracking of nano-influencers in the Israeli tech ecosystem.

**Current Database**: 78 active influencers + 15 excluded profiles tracked in `influencers.db`

## Development Environment

**Package Management**: This project uses `uv` for Python dependency management.
- Install dependencies: `uv sync`
- Run Python scripts: `uv run python script.py`
- Python version: 3.13+

**Required Environment Variables** (`.env`):
- `XAI_API_KEY` - xAI Grok API key for Twitter search
- `RAPIDAPI_KEY` - RapidAPI key for Twitter API access

## Claude Code Skills

This repository includes three custom Claude Code skills in `.claude/skills/`:

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

**Script location**: `.claude/skills/x-api/src/client.py`

**Commands**:
- `userinfo <screenname>` - Get user info
- `timeline <screenname>` - Get user's tweets
- `search <query> [--type TYPE]` - Search tweets
- `replies <screenname>` - Get user replies

### 3. influencer-db skill
SQLite database management for Israeli tech nano-influencers with direct SQL query access:
- Execute any SQL query (SELECT, INSERT, UPDATE, DELETE)
- Schema inspection
- JSON output for easy integration
- Tracks active and excluded influencers in single database

**Invocation**: Use the `Skill` tool with command `"influencer-db"`

**Script location**: `.claude/skills/influencer-db/src/client.py`

**Commands**:
- `query "<SQL>"` - Execute SQL query, returns JSON
- `schema [table]` - View database schema

**Database location**: `influencers.db` (version controlled in git)

## Claude Code Agents

### 1. israeli-tech-influencer-finder
**Location**: `.claude/agents/israeli-tech-influencer-finder.md`

Specialized agent for discovering and tracking Israeli tech nano-influencers on Twitter/X.

**When to use**: Invoke when user wants to find Israeli tech influencers, expand network in Israeli startup scene, or engage with Hebrew-speaking tech professionals.

**Primary workflow**:
1. Uses `xai-grok` skill for direct Twitter/X searches (primary method)
2. Searches with Hebrew keywords: "טק", "היי-טק", "סטארטאפ", "יזם", "פיתוח"
3. Validates profiles: individual personas only, <10K followers, recent activity, Hebrew content
4. Stores discovered influencers in `influencers.db` SQLite database

**Key criteria**:
- INDIVIDUAL PERSONAS ONLY (not organizations/companies/media outlets)
- Follower count under 10,000
- Recent activity (within 7-14 days)
- Hebrew language content
- Tech/startup focus

### 2. x-list-manager
**Location**: `.claude/agents/x-list-manager.md`

Browser automation agent for adding Twitter/X users to X lists using Chrome DevTools MCP server.

**When to use**: Invoke when user wants to add influencers to an X/Twitter list for organized tracking.

**Primary workflow**:
1. Ensures user is logged into X/Twitter (manual login required)
2. Navigates to user profiles
3. Accesses list management interface via profile menu
4. Adds users to specified lists
5. Verifies successful additions
6. Supports batch operations with progress tracking

**Key features**:
- Single and batch user additions
- Error handling for suspended/deleted accounts
- Progress tracking and summary reports
- Retry logic for transient failures

### 3. influencer-data-refresher
**Location**: `.claude/agents/influencer-data-refresher.md`

Data synchronization agent for maintaining accuracy of the influencer database.

**When to use**: Invoke when you need to validate and update influencer data with current Twitter information.

**Primary workflow**:
1. Reads influencer entries from database
2. Fetches fresh data from Twitter API using `x-api` skill
3. Updates or validates stored information
4. Marks processed entries with timestamps
5. Handles suspended accounts and errors gracefully

**Key features**:
- Systematic batch processing
- Progress tracking with checkpoints
- Data validation and integrity checks
- Comprehensive reporting

## Repository Structure

```
.
├── .claude/
│   ├── agents/
│   │   ├── israeli-tech-influencer-finder.md   # Influencer discovery agent
│   │   ├── x-list-manager.md                   # X list management agent
│   │   └── influencer-data-refresher.md        # Data validation agent
│   ├── skills/
│   │   ├── influencer-db/
│   │   │   ├── SKILL.md
│   │   │   ├── requirements.txt
│   │   │   └── src/
│   │   │       ├── client.py                   # SQLite CLI
│   │   │       └── schema.sql                  # Database schema
│   │   ├── x-api/
│   │   │   ├── SKILL.md
│   │   │   ├── requirements.txt
│   │   │   └── src/
│   │   │       ├── client.py                   # Twitter API client
│   │   │       └── models.py                   # Data models
│   │   └── xai-grok/
│   │       ├── SKILL.md
│   │       ├── requirements.txt
│   │       └── src/
│   │           └── grok.py                     # Grok API client
│   └── settings.local.json
├── influencers.db                               # SQLite database (78 active + 15 excluded)
├── pyproject.toml                               # Python project config
└── uv.lock                                      # Dependency lock file
```

## Key Dependencies

- `xai-sdk` (1.3.1) - xAI Grok API integration
- `typer` (0.20.0) - CLI framework for both skills
- `python-dotenv` - Environment variable management
- `openai` - OpenAI API client

## Working with the Skills

All skills are implemented as Python scripts using Typer for CLI functionality. They can be invoked:

1. **Through Claude Code**: Use the `Skill` tool with commands:
   - `"xai-grok"` - For Grok AI queries
   - `"x-api"` - For Twitter API access
   - `"influencer-db"` - For database operations

2. **Directly from CLI**:
   - `uv run python .claude/skills/xai-grok/src/grok.py "query"`
   - `uv run python .claude/skills/x-api/src/client.py userinfo <screenname>`
   - `uv run python .claude/skills/influencer-db/src/client.py query "SELECT * FROM influencers"`

## Israeli Tech Ecosystem Context

When working with influencer data, be aware of:

- **Unit 8200 Influence**: ~80% of Israeli cybersecurity founders come from IDF intelligence units
- **Bilingual Culture**: Most tech professionals use both Hebrew and English
- **Tight-Knit Networks**: Strong personal connections from military service, Hebrew U, Technion
- **Global Orientation**: Strong ties to Silicon Valley, NYC, London tech scenes
- **Key Events**: Reversim Summit, DLD Tel Aviv, CyberTech
- **Major Companies**: Wix, Monday.com, Check Point, Waze alumni networks

## Research Workflow

### Discovery & Tracking
1. Invoke `israeli-tech-influencer-finder` agent for discovery
2. Agent uses `xai-grok` skill for real-time Twitter searches
3. Agent validates profiles against criteria
4. Agent stores discoveries in `influencers.db` using `influencer-db` skill
5. User reviews database contents using SQL queries

### Data Maintenance
1. Invoke `influencer-data-refresher` agent to update profile data
2. Agent fetches current Twitter data using `x-api` skill
3. Agent updates database with fresh information
4. Agent tracks excluded/inactive accounts

### List Management
1. Query database for influencers to add to X lists
2. Invoke `x-list-manager` agent with usernames
3. Agent adds users to specified X lists via browser automation
4. Track list memberships in database notes

## Important Notes

- The `.env` file contains API keys and is gitignored
- **Database versioning**: `influencers.db` is tracked in git for version history and collaboration
- All Twitter API access goes through either Grok (via xai-grok skill) or RapidAPI (via x-api skill)
- Focus on nano-influencers: follower counts must be verified to be under 10,000
- Individual personas only - organizations and media outlets are excluded from tracking
- Database schema uses single table with `excluded` flag (0=active, 1=excluded)
- Currently tracking: 78 active influencers + 15 excluded profiles