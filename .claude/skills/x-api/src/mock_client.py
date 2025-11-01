#!/usr/bin/env python3
"""
Mock Twitter API client for testing when api.twitterapi.io is blocked.
Simulates responses with realistic Israeli tech influencer data.
"""

import json
from models import UserInfoResponse, SearchResponse, SearchTweet


class MockTwitterAPIClient:
    """Mock client for testing when real API is blocked."""

    def __init__(self, api_key: str = None):
        """Initialize mock client (api_key ignored)."""
        pass

    def get_user_info(self, screenname: str) -> UserInfoResponse:
        """
        Return mock user info for testing.

        Args:
            screenname: Twitter username (without @)

        Returns:
            UserInfoResponse: Mock user info
        """
        # Mock data for common Israeli tech personas
        mock_users = {
            "yuraguller": UserInfoResponse(
                status="active",
                profile="https://pbs.twimg.com/profile_images/mock/yura.jpg",
                blue_verified=False,
                verification_type=None,
                affiliates={},
                business_account={},
                desc="Israeli tech entrepreneur | Building startups in Tel Aviv 🚀",
                name="Yura Guller",
                website="https://example.com",
                protected=False,
                location="Tel Aviv, Israel",
                following=450,
                followers=1250,
                statuses_count=2840,
                media_count=156,
                created_at="2018-03-15T10:22:00.000Z",
                last_tweet_date="2025-10-28T14:30:00.000Z",
                last_reply_date="2025-10-28T18:45:00.000Z",
                is_hebrew_writer=True
            ),
            "default": UserInfoResponse(
                status="active",
                profile="https://pbs.twimg.com/profile_images/mock/default.jpg",
                blue_verified=False,
                verification_type=None,
                affiliates={},
                business_account={},
                desc=f"Mock user profile for @{screenname}",
                name=screenname.title(),
                website=None,
                protected=False,
                location="Israel",
                following=200,
                followers=850,
                statuses_count=1200,
                media_count=50,
                created_at="2020-01-01T00:00:00.000Z",
                last_tweet_date="2025-10-25T12:00:00.000Z",
                last_reply_date="2025-10-25T15:00:00.000Z",
                is_hebrew_writer=True
            )
        }

        return mock_users.get(screenname.lower(), mock_users["default"])

    def search_tweets(self, query: str, search_type: str = "Top") -> SearchResponse:
        """
        Return mock search results for testing.

        Args:
            query: Search query string
            search_type: Type of search ("Top", "Latest", etc.)

        Returns:
            SearchResponse: Mock search results
        """
        # Generate mock Israeli tech tweets based on query
        mock_tweets = []

        # Hebrew tech content
        if "lang:he" in query or any(hebrew in query for hebrew in ["סטארטאפ", "טכנולוגיה"]):
            mock_tweets = [
                SearchTweet(
                    screen_name="israeli_techie",
                    bookmarks=12,
                    favorites=45,
                    created_at="2025-10-28T10:30:00.000Z",
                    text="הסטארטאפ החדש שלנו בתל אביב מגייס! מחפשים מפתחים מוכשרים 🚀",
                    lang="he",
                    quotes=3,
                    replies=8,
                    retweets=15
                ),
                SearchTweet(
                    screen_name="tlv_founder",
                    bookmarks=8,
                    favorites=32,
                    created_at="2025-10-28T09:15:00.000Z",
                    text="טכנולוגיה ישראלית משנה את העולם! גאה להיות חלק מהמהפכה",
                    lang="he",
                    quotes=2,
                    replies=5,
                    retweets=10
                )
            ]
        # English Israeli tech content
        elif "israeli" in query.lower() or "startup" in query.lower():
            mock_tweets = [
                SearchTweet(
                    screen_name="startupTLV",
                    bookmarks=25,
                    favorites=120,
                    created_at="2025-10-28T14:20:00.000Z",
                    text="Israeli startup scene is on fire! 🔥 Just closed our seed round",
                    lang="en",
                    quotes=8,
                    replies=15,
                    retweets=35
                ),
                SearchTweet(
                    screen_name="tech_aviv",
                    bookmarks=18,
                    favorites=89,
                    created_at="2025-10-28T12:45:00.000Z",
                    text="Building in Tel Aviv, scaling globally. This is the future of tech.",
                    lang="en",
                    quotes=5,
                    replies=12,
                    retweets=28
                ),
                SearchTweet(
                    screen_name="israeli_dev",
                    bookmarks=10,
                    favorites=56,
                    created_at="2025-10-28T11:30:00.000Z",
                    text="Excited to announce our new AI product launching next month! #IsraeliTech",
                    lang="en",
                    quotes=3,
                    replies=9,
                    retweets=18
                )
            ]
        else:
            # Generic tech tweets
            mock_tweets = [
                SearchTweet(
                    screen_name="tech_enthusiast",
                    bookmarks=5,
                    favorites=25,
                    created_at="2025-10-28T16:00:00.000Z",
                    text=f"Interesting discussion about {query}",
                    lang="en",
                    quotes=1,
                    replies=4,
                    retweets=8
                )
            ]

        return SearchResponse(timeline=mock_tweets)
