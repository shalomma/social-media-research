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

# Search by location
python3 client.py query "SELECT * FROM influencers WHERE location LIKE '%Tel Aviv%'"

# Filter by follower count
python3 client.py query "SELECT * FROM influencers WHERE follower_count > 1000"

# Get Hebrew writers
python3 client.py query "SELECT * FROM influencers WHERE hebrew_writer = 1"

# Complex search
python3 client.py query "SELECT * FROM influencers WHERE location LIKE '%Israel%' AND follower_count BETWEEN 500 AND 5000 ORDER BY follower_count DESC"

# Limit results
python3 client.py query "SELECT * FROM influencers LIMIT 10"
```

#### Aggregations & Stats

```bash
# Count total influencers
python3 client.py query "SELECT COUNT(*) as total FROM influencers"

# Count by location
python3 client.py query "SELECT location, COUNT(*) as count FROM influencers WHERE location IS NOT NULL GROUP BY location ORDER BY count DESC"

# Average followers
python3 client.py query "SELECT AVG(follower_count) as avg_followers FROM influencers WHERE follower_count IS NOT NULL"

# Hebrew writers count
python3 client.py query "SELECT COUNT(*) as hebrew_writers FROM influencers WHERE hebrew_writer = 1"

# Top influencers by followers
python3 client.py query "SELECT twitter_handle, name, follower_count FROM influencers ORDER BY follower_count DESC LIMIT 10"
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

# Update verification date
python3 client.py query "UPDATE influencers SET last_verified_date = '2025-10-26T12:00:00' WHERE twitter_handle = 'test_user'"

# Update multiple fields
python3 client.py query "UPDATE influencers SET follower_count = 2500, last_tweet_date = '2025-10-26', last_verified_date = '2025-10-26' WHERE twitter_handle = 'oriSomething'"
```

#### DELETE Queries

```bash
# Delete influencer
python3 client.py query "DELETE FROM influencers WHERE twitter_handle = 'test_user'"

# Delete by criteria
python3 client.py query "DELETE FROM influencers WHERE follower_count < 100"
```

#### Parameterized Queries (Safer)

For user input, use parameterized queries to prevent SQL injection:

```bash
# With parameters
python3 client.py query "SELECT * FROM influencers WHERE twitter_handle = ?" --params '["oriSomething"]'

python3 client.py query "INSERT INTO influencers (twitter_handle, name) VALUES (?, ?)" --params '["user123", "User Name"]'
```

### 2. schema - View Schema

View database schema and structure.

```bash
# Show all tables and schemas
python3 client.py schema

# Show specific table schema
python3 client.py schema influencers
python3 client.py schema excluded_influencers
```

## Usage Examples

### From Agent Code

Agents can easily execute queries and parse JSON output:

```python
import subprocess
import json

def query_db(sql: str) -> list:
    """Execute SQL query and return results."""
    result = subprocess.run(
        ["python3", "client.py", "query", sql],
        capture_output=True,
        text=True,
        cwd=".claude/skills/influencer-db/src"
    )

    if result.returncode == 0:
        return json.loads(result.stdout)
    return []

# Usage
influencers = query_db("SELECT * FROM influencers WHERE location LIKE '%Tel Aviv%'")
stats = query_db("SELECT COUNT(*) as total FROM influencers")
```

### Integration with X API

Fetch user data from X API and insert into database:

```bash
# 1. Get user info from X API
python3 .claude/skills/x-api/src/client.py userinfo oriSomething > user.json

# 2. Parse and insert (example with jq)
# Extract values and construct INSERT query
```

Or programmatically:

```python
import subprocess
import json

# Fetch from X API
result = subprocess.run(
    ["python3", ".claude/skills/x-api/src/client.py", "userinfo", "oriSomething"],
    capture_output=True,
    text=True
)

user_info = json.loads(result.stdout)

# Insert into database
sql = f"""
INSERT INTO influencers (
    twitter_handle, name, location, language,
    follower_count, last_tweet_date, last_reply_date,
    hebrew_writer, added_date, last_verified_date
) VALUES (
    '{user_info['profile']}',
    '{user_info['name']}',
    '{user_info['location']}',
    '{user_info.get('language', '')}',
    {user_info['followers']},
    '{user_info.get('last_tweet_date', '')}',
    '{user_info.get('last_reply_date', '')}',
    {1 if user_info['is_hebrew_writer'] else 0},
    datetime('now'),
    datetime('now')
)
"""

subprocess.run(
    ["python3", "client.py", "query", sql],
    cwd=".claude/skills/influencer-db/src"
)
```

### Exclude Inactive Influencers

Move inactive influencer to excluded list:

```bash
# 1. Get influencer data
python3 client.py query "SELECT * FROM influencers WHERE twitter_handle = 'inactive_user'" > user.json

# 2. Insert into excluded_influencers with exclusion info
python3 client.py query "INSERT INTO excluded_influencers (twitter_handle, name, location, follower_count, hebrew_writer, added_date, excluded_date, exclusion_reason) SELECT twitter_handle, name, location, follower_count, hebrew_writer, added_date, '2025-10-26', 'Inactive: Last tweet before July 2025' FROM influencers WHERE twitter_handle = 'inactive_user'"

# 3. Delete from influencers
python3 client.py query "DELETE FROM influencers WHERE twitter_handle = 'inactive_user'"
```

### Common Patterns

```bash
# List all with specific fields
python3 client.py query "SELECT twitter_handle, name, follower_count, location FROM influencers ORDER BY follower_count DESC"

# Search by multiple criteria
python3 client.py query "SELECT * FROM influencers WHERE (focus LIKE '%AI%' OR focus LIKE '%ML%') AND location LIKE '%Israel%'"

# Recent additions
python3 client.py query "SELECT * FROM influencers ORDER BY added_date DESC LIMIT 10"

# Need verification (older than 30 days)
python3 client.py query "SELECT twitter_handle, name, last_verified_date FROM influencers WHERE last_verified_date < date('now', '-30 days')"

# Export to JSON file
python3 client.py query "SELECT * FROM influencers" > all_influencers.json
```

## Database Location

```
/Users/maayan/Development/social-media-research/influencers.db
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

## Why This Approach?

**Flexibility**: Agents can craft any SQL query needed without being constrained by predefined commands.

**Simplicity**: Just two commands - `query` and `schema`. Everything else is SQL.

**Power**: Full SQL capabilities including joins, aggregations, subqueries, CTEs, etc.

**Transparency**: See exactly what queries are executed. No hidden abstractions.

**Standard**: SQL is universal. Any agent that knows SQL can use this database.

## Tips for Agents

1. **Start with schema**: Run `python3 client.py schema` to understand the structure
2. **Use LIMIT**: Always limit results during exploration
3. **Test SELECTs first**: Before INSERT/UPDATE/DELETE, test with SELECT
4. **Use transactions**: For multiple operations, wrap in transaction (BEGIN/COMMIT)
5. **Check constraints**: twitter_handle is UNIQUE - handle conflicts
6. **Use indexes**: location and follower_count are indexed for fast queries

## SQLite Reference

Common SQL patterns for this database:

```sql
-- Full-text search (case-insensitive)
SELECT * FROM influencers WHERE name LIKE '%search%' OR role LIKE '%search%'

-- Date filtering
SELECT * FROM influencers WHERE last_tweet_date > '2025-07-01'

-- NULL handling
SELECT * FROM influencers WHERE location IS NOT NULL

-- Sorting
SELECT * FROM influencers ORDER BY follower_count DESC, name ASC

-- DISTINCT values
SELECT DISTINCT location FROM influencers WHERE location IS NOT NULL

-- CASE expressions
SELECT
    twitter_handle,
    name,
    CASE
        WHEN follower_count > 5000 THEN 'Large'
        WHEN follower_count > 1000 THEN 'Medium'
        ELSE 'Small'
    END as size_category
FROM influencers
```

## Troubleshooting

**Import errors**: `cd .claude/skills/influencer-db && pip install -r requirements.txt`

**Database locked**: Close any SQLite browser tools or other connections

**SQL syntax errors**: Check SQLite documentation for correct syntax

**Permission errors**: Ensure write access to project directory

## Future Enhancements

- Backup/restore commands
- Export to CSV
- Import from CSV/JSON
- Migration scripts
- Full-text search (FTS5)
