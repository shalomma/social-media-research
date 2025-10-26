from typing import Optional, Any
from pydantic import BaseModel


class UserInfoResponse(BaseModel):
    """Response model for user info with calculated fields."""
    status: str
    profile: str
    blue_verified: bool
    verification_type: Optional[str] = None
    affiliates: Any  # Can be list or dict depending on API response
    business_account: Any  # Can be list or dict depending on API response
    desc: str
    name: str
    website: Optional[str] = None
    protected: Optional[bool] = None
    location: Optional[str] = None
    following: int
    followers: int
    statuses_count: int
    media_count: int
    created_at: str
    last_tweet_date: Optional[str] = None
    last_reply_date: Optional[str] = None
    is_hebrew_writer: bool = False


class SearchTweet(BaseModel):
    """Individual tweet in search results (excludes id and media)."""
    screen_name: str
    bookmarks: int
    favorites: int
    created_at: str
    text: str
    lang: str
    quotes: int
    replies: int
    retweets: int


class SearchResponse(BaseModel):
    """Response model for tweet search results."""
    timeline: list[SearchTweet]
