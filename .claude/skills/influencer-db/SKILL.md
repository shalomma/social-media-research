---
name: influencer-db
description: Simple SQLite database for Israeli Tech Nano-Influencers with direct SQL query access. Execute any SQL query or inspect schema. Flexible and agent-friendly.
---

# Israeli Tech Nano-Influencers Database

A simple SQLite database with direct SQL query access for managing Israeli tech nano-influencer data. No abstractions - just raw SQL power.

## Features

- **Direct SQL Access**: Execute any SQL query (SELECT, INSERT, UPDATE, DELETE)
- **Schema Inspection**: View database schema and table structures
- **JSON Output**: All results returned as JSON for easy parsing
- **Auto-initialization**: Database created automatically on first use
- **Flexible**: Agents can craft any query they need

## Setup

```bash
cd .claude/skills/influencer-db
pip install -r requirements.txt
```

## Database Schema

### Tables

**`influencers`** - Active nano-influencers
- `id` (INTEGER PRIMARY KEY)
- `twitter_handle` (TEXT UNIQUE NOT NULL)
- `name` (TEXT NOT NULL)
- `role` (TEXT)
- `focus` (TEXT)
- `background` (TEXT)
- `recent_activity` (TEXT)
- `engagement_potential` (TEXT)
- `profile_url` (TEXT)
- `location` (TEXT)
- `language` (TEXT)
- `follower_count` (INTEGER)
- `last_tweet_date` (TEXT)
- `last_reply_date` (TEXT)
- `hebrew_writer` (BOOLEAN)
- `added_date` (TEXT NOT NULL)
- `last_verified_date` (TEXT)
- `notes` (TEXT)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

**`excluded_influencers`** - Excluded/inactive influencers
- All fields from `influencers` table
- `excluded_date` (TEXT NOT NULL)
- `exclusion_reason` (TEXT NOT NULL)

## CLI Commands

### 1. query - Execute SQL

Execute any SQL query and get JSON results.

```bash
cd .claude/skills/influencer-db/src
python3 client.py query "<SQL>"
```

#### SELECT Queries

```bash
# Get all influencers
python3 client.py query "SELECT * FROM influencers"

# Get specific influencer
python3 client.py query "SELECT * FROM influencers WHERE twitter_handle = 'oriSomething'"
```

#### INSERT Queries

```bash
# Add new influencer
python3 client.py query "INSERT INTO influencers (twitter_handle, name, location, follower_count, hebrew_writer, added_date, last_verified_date) VALUES ('test_user', 'Test User', 'Tel Aviv', 1500, 1, '2025-10-26', '2025-10-26')"

# Add with more fields
python3 client.py query "INSERT INTO influencers (twitter_handle, name, role, focus, location, language, follower_count, hebrew_writer, engagement_potential, added_date) VALUES ('example', 'Example User', 'Developer', 'AI/ML', 'Israel', 'Hebrew, English', 2000, 1, 'HIGH', '2025-10-26')"
```

#### UPDATE Queries

```bash
# Update follower count
python3 client.py query "UPDATE influencers SET follower_count = 2000 WHERE twitter_handle = 'test_user'"
```

### 2. schema - View Schema

View database schema and structure.

```bash
# Show all tables and schemas
python3 client.py schema

# Show specific table schema
python3 client.py schema influencers
```

## Usage Examples

## Database Location

```
/influencers.db
```

**The database file IS version controlled in git.** Unlike typical databases, this SQLite file is treated as a data file (similar to the markdown files it replaces). This provides:
- Version history of influencer data
- Easy collaboration and cloning
- Automatic backup through git
- Change tracking over time

Since it's a small, curated dataset (not a high-frequency transactional database), this approach works well.

## Architecture

```
.claude/skills/influencer-db/
├── SKILL.md              # This documentation
├── requirements.txt      # Python dependencies (just typer)
└── src/
    ├── client.py        # Simple CLI (query + schema)
    └── schema.sql       # Database schema

influencers.db           # SQLite database (version controlled in git)
```

## Tips for Agents

1. **Start with schema**: Run `python3 client.py schema` to understand the structure
2. **Use LIMIT**: Always limit results during exploration
3. **Test SELECTs first**: Before INSERT/UPDATE/DELETE, test with SELECT
4. **Use transactions**: For multiple operations, wrap in transaction (BEGIN/COMMIT)
5. **Check constraints**: twitter_handle is UNIQUE - handle conflicts
6. **Use indexes**: location and follower_count are indexed for fast queries
