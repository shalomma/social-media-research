#!/usr/bin/env python3
"""
Twitter API client for accessing multiple RapidAPI endpoints.
Supports user info, timeline, search, and replies functionality.
"""

import os
import json
import typer
import requests
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class UserTimelineResponse(BaseModel):
    """Response model for user timeline with calculated fields."""
    status: str
    profile: str
    blue_verified: bool
    verification_type: Optional[str] = None
    affiliates: list
    business_account: list
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


class TwitterAPIClient:
    """Client for interacting with Twitter API via RapidAPI."""

    BASE_URL = "https://twitter-api45.p.rapidapi.com"

    def __init__(self, api_key: str = None):
        """
        Initialize the Twitter API client.

        Args:
            api_key: RapidAPI key. If not provided, reads from RAPIDAPI_KEY env var.

        Raises:
            ValueError: If api_key is not provided and RAPIDAPI_KEY is not set.
        """
        self.api_key = api_key or os.environ.get("RAPIDAPI_KEY")

        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY environment variable is not set or api_key not provided")

    def _make_request(self, endpoint: str, params: dict) -> dict:
        """
        Make a request to the Twitter API.

        Args:
            endpoint: API endpoint (e.g., 'screenname.php')
            params: Query parameters

        Returns:
            dict: JSON response from the API

        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"

        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "twitter-api45.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json()

    def get_user_timeline(self, screenname: str) -> UserTimelineResponse:
        """
        Retrieve a user's timeline (tweets) by screen name.

        Args:
            screenname: Twitter username (without @)

        Returns:
            UserTimelineResponse: User info with calculated fields

        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        params = {
            "screenname": screenname
        }

        response = self._make_request("timeline.php", params)

        # Extract user data
        user_data = response["user"]

        # Calculate fields from timeline
        last_tweet_date = None
        last_reply_date = None
        is_hebrew_writer = False

        timeline_list = response.get("timeline", [])

        for item in timeline_list:
            tweet_id = item.get("tweet_id")
            conversation_id = item.get("conversation_id")
            created_at = item.get("created_at")
            lang = item.get("lang")

            # Check for Hebrew content
            if lang == "he":
                is_hebrew_writer = True

            # Distinguish between tweets and replies
            if tweet_id == conversation_id:
                # This is an original tweet
                if last_tweet_date is None:
                    last_tweet_date = created_at
            else:
                # This is a reply
                if last_reply_date is None:
                    last_reply_date = created_at

        # Create and return Pydantic model
        # Map API field names to our model field names
        return UserTimelineResponse(
            status=user_data["status"],
            profile=user_data["profile"],
            blue_verified=user_data["blue_verified"],
            verification_type=user_data.get("verification_type"),
            affiliates=user_data["affiliates"],
            business_account=user_data["business_account"],
            desc=user_data["desc"],
            name=user_data["name"],
            website=user_data.get("website"),
            protected=user_data.get("protected"),
            location=user_data.get("location"),
            following=user_data["friends"],
            followers=user_data["sub_count"],
            statuses_count=user_data["statuses_count"],
            media_count=user_data["media_count"],
            created_at=user_data["created_at"],
            last_tweet_date=last_tweet_date,
            last_reply_date=last_reply_date,
            is_hebrew_writer=is_hebrew_writer
        )

    def search_tweets(self, query: str, search_type: str = "Top") -> dict:
        """
        Search for tweets matching a query.

        Args:
            query: Search query string
            search_type: Type of search ("Top", "Latest", "Media", "People", or "Lists")

        Returns:
            dict: Search results from the API

        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        params = {
            "query": query,
            "search_type": search_type
        }

        return self._make_request("search.php", params)


# Create Typer app
app = typer.Typer(help="Twitter API client for RapidAPI endpoints")


@app.command()
def timeline(
    screenname: str = typer.Argument(..., help="Twitter username (without @)")
):
    """Get user's timeline (tweets)"""
    try:
        client = TwitterAPIClient()
        result = client.get_user_timeline(screenname)
        typer.echo(json.dumps(result.model_dump(), indent=2))
    except ValueError as e:
        typer.secho(f"Configuration Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
    except requests.exceptions.HTTPError as e:
        typer.secho(f"API Error: {e}", fg=typer.colors.RED, err=True)
        if e.response is not None:
            typer.secho(f"Response: {e.response.text}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
    except requests.exceptions.RequestException as e:
        typer.secho(f"Request Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    search_type: str = typer.Option(
        "Top",
        "--type",
        help="Search type: Top, Latest, Media, People, or Lists"
    )
):
    """Search for tweets"""
    try:
        client = TwitterAPIClient()
        result = client.search_tweets(query, search_type)
        typer.echo(json.dumps(result, indent=2))
    except ValueError as e:
        typer.secho(f"Configuration Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
    except requests.exceptions.HTTPError as e:
        typer.secho(f"API Error: {e}", fg=typer.colors.RED, err=True)
        if e.response is not None:
            typer.secho(f"Response: {e.response.text}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
    except requests.exceptions.RequestException as e:
        typer.secho(f"Request Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)



if __name__ == "__main__":
    app()
