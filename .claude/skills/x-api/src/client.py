#!/usr/bin/env python3
"""
Twitter API client for accessing twitterapi.io endpoints.
Supports user info and advanced search functionality.
"""

import os
import requests
from dotenv import load_dotenv

from models import UserInfoResponse, SearchResponse, SearchTweet

load_dotenv()


class TwitterAPIClient:
    """Client for interacting with Twitter API via twitterapi.io."""

    BASE_URL = "https://api.twitterapi.io"

    def __init__(self, api_key: str = None):
        """
        Initialize the Twitter API client.

        Args:
            api_key: API key for twitterapi.io. If not provided, reads from XAPI_IO_API_KEY env var.

        Raises:
            ValueError: If api_key is not provided and XAPI_IO_API_KEY is not set.
        """
        self.api_key = api_key or os.environ.get("XAPI_IO_API_KEY")

        if not self.api_key:
            raise ValueError("XAPI_IO_API_KEY environment variable is not set or api_key not provided")

    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        """
        Make a request to the Twitter API.

        Args:
            endpoint: API endpoint (e.g., 'twitter/user/info')
            params: Query parameters (optional)

        Returns:
            dict: JSON response from the API

        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"

        headers = {
            "X-API-Key": self.api_key
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        # Debug: print response text if JSON parsing fails
        try:
            return response.json()
        except Exception:
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            raise

    def get_user_info(self, screenname: str) -> UserInfoResponse:
        """
        Retrieve user information by screen name.

        Args:
            screenname: Twitter username (without @)

        Returns:
            UserInfoResponse: User info (calculated fields require separate search call)

        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        params = {
            "username": screenname
        }

        response = self._make_request("twitter/user/info", params)

        # Extract user data from the 'data' wrapper
        user_data = response["data"]

        # Note: The new API doesn't return timeline data in user info endpoint
        # Calculated fields (last_tweet_date, last_reply_date, is_hebrew_writer)
        # would require a separate search call using search_tweets(f"from:{screenname}")

        # Create and return Pydantic model
        # Map new API field names to our model field names
        return UserInfoResponse(
            status="active" if not user_data.get("unavailable") else "unavailable",
            profile=user_data.get("profilePicture", ""),
            blue_verified=user_data.get("isBlueVerified", False),
            verification_type=user_data.get("verifiedType"),
            affiliates=user_data.get("affiliatesHighlightedLabel", {}),
            business_account={},  # Not provided in new API
            desc=user_data.get("description", ""),
            name=user_data.get("name", ""),
            website=user_data.get("profile_bio", {}).get("entities", {}).get("url", {}).get("urls", [{}])[0].get("expanded_url") if user_data.get("profile_bio") else None,
            protected=user_data.get("possiblySensitive"),
            location=user_data.get("location"),
            following=user_data.get("following", 0),
            followers=user_data.get("followers", 0),
            statuses_count=user_data.get("statusesCount", 0),
            media_count=user_data.get("mediaCount", 0),
            created_at=user_data.get("createdAt", ""),
            last_tweet_date=None,  # Requires separate search call
            last_reply_date=None,  # Requires separate search call
            is_hebrew_writer=False  # Requires separate search call
        )

    def search_tweets(self, query: str, search_type: str = "Top") -> SearchResponse:
        """
        Search for tweets matching a query.

        Args:
            query: Search query string
            search_type: Type of search ("Top", "Latest", "Media", "People", or "Lists")

        Returns:
            SearchResponse: Filtered search results

        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        params = {
            "query": query,
            "type": search_type
        }

        response = self._make_request("twitter/tweet/advanced_search", params)

        # Extract tweets array
        tweets_data = response.get("tweets", [])
        filtered_tweets = []

        for tweet in tweets_data:
            # Extract author username
            author = tweet.get("author", {})
            screen_name = author.get("userName", "")

            filtered_tweets.append(SearchTweet(
                screen_name=screen_name,
                bookmarks=tweet.get("bookmarkCount", 0),
                favorites=tweet.get("likeCount", 0),
                created_at=tweet.get("createdAt", ""),
                text=tweet.get("text", ""),
                lang=tweet.get("lang", ""),
                quotes=tweet.get("quoteCount", 0),
                replies=tweet.get("replyCount", 0),
                retweets=tweet.get("retweetCount", 0)
            ))

        return SearchResponse(timeline=filtered_tweets)
