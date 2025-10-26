-- Israeli Tech Nano-Influencers Database Schema
-- Created: October 26, 2025

-- Table for active nano-influencers
CREATE TABLE IF NOT EXISTS influencers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    twitter_handle TEXT UNIQUE NOT NULL,
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
    added_date TEXT NOT NULL,  -- ISO 8601 format
    last_verified_date TEXT,  -- ISO 8601 format
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for excluded/inactive influencers
CREATE TABLE IF NOT EXISTS excluded_influencers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    twitter_handle TEXT UNIQUE NOT NULL,
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
    last_tweet_date TEXT,
    last_reply_date TEXT,
    hebrew_writer BOOLEAN DEFAULT 0,
    added_date TEXT NOT NULL,
    last_verified_date TEXT,
    excluded_date TEXT NOT NULL,  -- ISO 8601 format
    exclusion_reason TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_influencers_handle ON influencers(twitter_handle);
CREATE INDEX IF NOT EXISTS idx_influencers_location ON influencers(location);
CREATE INDEX IF NOT EXISTS idx_influencers_hebrew_writer ON influencers(hebrew_writer);
CREATE INDEX IF NOT EXISTS idx_influencers_follower_count ON influencers(follower_count);
CREATE INDEX IF NOT EXISTS idx_excluded_handle ON excluded_influencers(twitter_handle);

-- Trigger to update updated_at timestamp on influencers
CREATE TRIGGER IF NOT EXISTS update_influencers_timestamp
AFTER UPDATE ON influencers
FOR EACH ROW
BEGIN
    UPDATE influencers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger to update updated_at timestamp on excluded_influencers
CREATE TRIGGER IF NOT EXISTS update_excluded_timestamp
AFTER UPDATE ON excluded_influencers
FOR EACH ROW
BEGIN
    UPDATE excluded_influencers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
