---
name: x-api
description: Unified Twitter/X API client for retrieving user info, timelines, tweets, and replies via RapidAPI. Supports user lookup, timeline retrieval, tweet search, and reply fetching with a clean Typer-based CLI and agent-friendly Python interface.
---

# X (Twitter) API Skill via RapidAPI

A unified Twitter/X API client providing access to multiple endpoints through RapidAPI. Built with Typer for a clean CLI experience and designed to be agent-friendly for programmatic usage.

## CLI Usage

The unified client (`.claude/skills/x-api/scripts/client.py`) provides four subcommands with beautiful, rich-formatted output.

### 1. Get User Information

Retrieve detailed user information by screen name and rest_id.

```bash
python3 client.py user <screenname>

# Example:
python3 client.py user elonmusk
```

### 2. Get User Timeline

Retrieve a user's timeline (tweets) by screen name. Returns a structured response with user information and the date of the most recent tweet.

```bash
python3 client.py timeline <screenname>

# Example:
python3 client.py timeline elonmusk
```

**Response Format:**

The timeline command returns a `UserTimelineResponse` Pydantic model with the following structure:

```json
{
  "status": "active",
  "profile": "username",
  "rest_id": "123456789",
  "blue_verified": true,
  "verification_type": null,
  "affiliates": [],
  "business_account": [],
  "avatar": "https://...",
  "header_image": "https://...",
  "desc": "User bio description",
  "name": "Display Name",
  "website": "example.com",
  "protected": null,
  "location": "Location",
  "following": 100,
  "followers": 1000,
  "statuses_count": 5000,
  "media_count": 50,
  "created_at": "Mon Jan 01 00:00:00 +0000 2020",
  "pinned_tweet_ids_str": [],
  "id": "123456789",
  "last_tweet_date": "Thu Oct 23 16:30:00 +0000 2025",
  "last_reply_date": "Fri Oct 24 09:55:51 +0000 2025",
  "is_hebrew_writer": false
}
```

**Calculated Fields:**

- `last_tweet_date`: The `created_at` timestamp of the user's most recent original tweet (where `tweet_id == conversation_id`), or `null` if no tweets are available.

- `last_reply_date`: The `created_at` timestamp of the user's most recent reply (where `tweet_id != conversation_id`), or `null` if no replies are available.

- `is_hebrew_writer`: Boolean flag indicating whether the user has posted any content in Hebrew (`lang == "he"`) in their timeline.

### 3. Get User's Replies

Retrieve replies to a specific tweet by tweet ID.

```bash
python3 client.py replies <screenname>

# Example:
python3 client.py replies elonmusk
```

### 4. Search Tweets

Search for tweets matching a query with optional search type filtering.

```bash
python3 client.py search <query> [--type Top|Latest|Media|People|Lists]

# Basic Examples:
python3 client.py search "artificial intelligence" --type Latest
python3 client.py search SpaceX
python3 client.py search "developers" --type People
python3 client.py search "tech lists" --type Lists
```

#### Advanced Search Operators

The search endpoint supports Twitter's advanced search syntax for precise filtering:

**User Filters:**
```bash
# Posts from a specific user
python3 client.py search "from:elonmusk Tesla"

# Posts directed to a user
python3 client.py search "to:NASA space"
```

**Date Filters:**
```bash
# Posts since a specific date
python3 client.py search "AI since:2025-01-01"

# Posts within a date range
python3 client.py search "climate change since:2025-01-01 until:2025-01-31"

# Using Unix timestamps for precise timing
python3 client.py search "breaking news since_time:1704067200"
```

**Content Type Filters:**
```bash
# Posts with images only
python3 client.py search "sunset filter:images"

# Posts with videos
python3 client.py search "tutorial filter:videos"

# Posts with links
python3 client.py search "article filter:links"

# Reply posts only
python3 client.py search "question filter:replies"
```

**Language Filter:**
```bash
# Posts in specific language (ISO 639-1 codes)
python3 client.py search "technology lang:he"
```

**Exclusion Operator:**
```bash
# Exclude specific terms (use minus operator)
python3 client.py search "from:NASA -Mars"
python3 client.py search "Python -snake"
```

**Combined Queries:**
```bash
# Complex multi-filter search
python3 client.py search "from:elonmusk since:2025-01-01 until:2025-01-07 Tesla -filter:replies"

# Search for content with media from specific user in date range
python3 client.py search "from:NASA filter:images since:2025-01-01"
```

## Common Use Cases

- **Research**: Retrieve and analyze user timelines, search for specific topics
- **Monitoring**: Track mentions, hashtags, or specific users
- **Data Collection**: Gather tweets, replies, and user information for analysis
- **Validation**: Verify Twitter usernames and IDs
- **Engagement Analysis**: Analyze replies and interactions on specific tweets

## Error Handling

Common error scenarios:
- **401 Unauthorized**: Invalid or missing API key - verify `RAPIDAPI_KEY` is set
- **429 Too Many Requests**: Rate limit exceeded - implement delays between requests
- **404 Not Found**: User/tweet not found - verify IDs/usernames are correct
- **500 Server Error**: RapidAPI service issue - retry with exponential backoff

The `TwitterAPIClient` automatically handles these errors and provides clear error messages.
