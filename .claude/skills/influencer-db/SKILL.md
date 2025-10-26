---
name: influencer-db
description: Simple SQLite database for Israeli Tech Nano-Influencers with direct SQL query access. Execute any SQL query or inspect schema. Flexible and agent-friendly.
---

# Israeli Tech Nano-Influencers Database

A simple SQLite database with direct SQL query access for managing Israeli tech nano-influencer data. No abstractions - just raw SQL power.

## Features

- **Direct SQL Access**: Execute any SQL query (SELECT, INSERT, UPDATE, DELETE)
- **Safe Mode Protection**: Blocks destructive operations by default (DROP, TRUNCATE, DELETE without WHERE)
- **Schema Inspection**: View database schema and table structures
- **JSON Output**: All results returned as JSON for easy parsing
- **Auto-initialization**: Database created automatically on first use
- **Flexible**: Agents can craft any query they need

## Database Schema

### Tables

**`influencers`** - Single table for all influencers (active and excluded)

**Profile & Identity:**
- `twitter_handle` (TEXT PRIMARY KEY) - Twitter/X username
- `name` (TEXT NOT NULL) - Full name
- `role` (TEXT) - Professional role/title
- `focus` (TEXT) - Areas of expertise or interest
- `background` (TEXT) - Professional background
- `profile_url` (TEXT) - Link to Twitter/X profile

**Engagement & Activity:**
- `recent_activity` (TEXT) - Description of recent posts/activity
- `engagement_potential` (TEXT) - Assessment of engagement value (HIGH/MEDIUM/LOW)
- `last_tweet_date` (TEXT) - Date of most recent tweet
- `last_reply_date` (TEXT) - Date of most recent reply

**Location & Language:**
- `location` (TEXT) - Geographic location
- `language` (TEXT) - Languages used in content
- `hebrew_writer` (BOOLEAN) - Whether they write in Hebrew (0/1)

**X API Metrics (matching UserInfoResponse model):**
- `followers` (INTEGER) - Number of followers
- `following` (INTEGER) - Number of accounts they follow
- `statuses_count` (INTEGER) - Total number of tweets/statuses
- `media_count` (INTEGER) - Total media items posted

**Discovery & Tracking:**
- `discovery_path` (TEXT) - How the influencer was discovered (web search query, website URL, referral path, etc.)
- `added_date` (TEXT NOT NULL) - Date added to database (ISO 8601 format)
- `last_verified_date` (TEXT) - Date profile was last verified (ISO 8601 format)

**Exclusion Management:**
- `excluded` (BOOLEAN DEFAULT 0) - Whether excluded from active list (0=active, 1=excluded)
- `excluded_date` (TEXT) - Date of exclusion (ISO 8601 format, nullable)
- `exclusion_reason` (TEXT) - Reason for exclusion (nullable)

**Metadata:**
- `notes` (TEXT) - Additional notes or observations
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP) - Record creation timestamp
- `updated_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP) - Last update timestamp (auto-updated)

**Indexes:**
- `idx_influencers_location` - Fast queries by location
- `idx_influencers_hebrew_writer` - Fast queries by language
- `idx_influencers_followers` - Fast queries by follower count
- `idx_influencers_excluded` - Fast queries for active vs excluded

## Safe Mode Protection

**Safe mode is ENABLED by default** to prevent accidental data loss.

**Blocked operations:**
- `DROP TABLE`, `DROP INDEX`, `DROP VIEW`, `DROP TRIGGER`
- `TRUNCATE TABLE`
- `DELETE FROM table` (without WHERE clause)
- `ALTER TABLE ... DROP`

**Allowed operations:**
- `SELECT` (all queries)
- `INSERT` (all inserts)
- `UPDATE` (with or without WHERE)
- `DELETE FROM table WHERE ...` (with WHERE clause)
- `ALTER TABLE ... ADD` (adding columns)

**To disable safe mode:**

```bash
# Option 1: Use --unsafe flag for a single query
python3 client.py query "DROP TABLE old_table" --unsafe

# Option 2: Set environment variable to disable globally
export DB_SAFE_MODE=false
python3 client.py query "DROP TABLE old_table"
```

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
python3 client.py query "INSERT INTO influencers (twitter_handle, name, location, followers, hebrew_writer, added_date, last_verified_date) VALUES ('test_user', 'Test User', 'Tel Aviv', 1500, 1, '2025-10-26', '2025-10-26')"

# Add with more fields including discovery path
python3 client.py query "INSERT INTO influencers (twitter_handle, name, role, focus, location, language, followers, following, statuses_count, media_count, hebrew_writer, engagement_potential, discovery_path, added_date) VALUES ('example', 'Example User', 'Developer', 'AI/ML', 'Israel', 'Hebrew, English', 2000, 500, 1500, 300, 1, 'HIGH', 'web search: Israeli AI developers', '2025-10-26')"
```

#### UPDATE Queries

```bash
# Update follower count
python3 client.py query "UPDATE influencers SET followers = 2000 WHERE twitter_handle = 'test_user'"

# Update multiple X API metrics
python3 client.py query "UPDATE influencers SET followers = 2500, following = 600, statuses_count = 2000, media_count = 400 WHERE twitter_handle = 'test_user'"
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
2. **Safe mode is ON**: Destructive operations are blocked by default - use `--unsafe` flag if needed
3. **Use LIMIT**: Always limit results during exploration
4. **Test SELECTs first**: Before INSERT/UPDATE/DELETE, test with SELECT
5. **Use transactions**: For multiple operations, wrap in transaction (BEGIN/COMMIT)
6. **Check constraints**: twitter_handle is PRIMARY KEY - handle conflicts gracefully
7. **Use indexes**: location, followers, hebrew_writer, and excluded are indexed for fast queries
8. **Track discovery**: Always populate `discovery_path` when adding new influencers to track sourcing
9. **X API fields**: Use exact naming from X API model (followers, following, statuses_count, media_count)
10. **Git safety net**: Database is version controlled - you can always revert with `git checkout influencers.db`
