-- Israeli Tech Nano-Influencers Database Schema
-- Created: October 26, 2025
-- Updated: October 26, 2025 - Simplified to single table with twitter_handle as primary key

-- Single table for all influencers (active and excluded)
CREATE TABLE IF NOT EXISTS influencers (
    twitter_handle TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    role TEXT,
    focus TEXT,
    background TEXT,
    recent_activity TEXT,
    engagement_potential TEXT,
    profile_url TEXT,
    location TEXT,
    language TEXT,
    follower_count INTEGER,
    last_tweet_date TEXT,  -- Stored as ISO 8601 string or original Twitter format
    last_reply_date TEXT,  -- Stored as ISO 8601 string or original Twitter format
    hebrew_writer BOOLEAN DEFAULT 0,
    excluded BOOLEAN DEFAULT 0,  -- 0 = active, 1 = excluded
    excluded_date TEXT,  -- ISO 8601 format (nullable, only for excluded influencers)
    exclusion_reason TEXT,  -- Nullable, only for excluded influencers
    added_date TEXT NOT NULL,  -- ISO 8601 format
    last_verified_date TEXT,  -- ISO 8601 format
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_influencers_location ON influencers(location);
CREATE INDEX IF NOT EXISTS idx_influencers_hebrew_writer ON influencers(hebrew_writer);
CREATE INDEX IF NOT EXISTS idx_influencers_follower_count ON influencers(follower_count);
CREATE INDEX IF NOT EXISTS idx_influencers_excluded ON influencers(excluded);

-- Trigger to update updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_influencers_timestamp
AFTER UPDATE ON influencers
FOR EACH ROW
BEGIN
    UPDATE influencers SET updated_at = CURRENT_TIMESTAMP WHERE twitter_handle = NEW.twitter_handle;
END;
