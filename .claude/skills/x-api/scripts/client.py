#!/usr/bin/env python3
"""
Twitter API client for accessing multiple RapidAPI endpoints.
Supports user info, timeline, search, and replies functionality.
"""

import os
import json
import typer
import requests
from dotenv import load_dotenv

load_dotenv()


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

    def get_user_by_screenname(self, screenname: str) -> dict:
        """
        Retrieve Twitter user information by screen name and rest_id.

        Args:
            screenname: Twitter username (without @)

        Returns:
            dict: User data from the API

        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        params = {
            "screenname": screenname,
        }

        return self._make_request("screenname.php", params)

    def get_user_timeline(self, screenname: str) -> dict:
        """
        Retrieve a user's timeline (tweets) by screen name.

        Args:
            screenname: Twitter username (without @)

        Returns:
            dict: Timeline data from the API

        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        params = {
            "screenname": screenname
        }

        return self._make_request("timeline.php", params)

    def get_user_replies(self, screenname: str) -> dict:
        """
        Retrieve user replies.

        Args:
            screenname: The ID of the tweet to get replies for

        Returns:
            dict: Replies data from the API

        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        params = {
            "screenname": screenname
        }

        return self._make_request("replies.php", params)

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
def user(
    screenname: str = typer.Argument(..., help="Twitter username (without @)"),
):
    """Get user information by screenname"""
    try:
        client = TwitterAPIClient()
        result = client.get_user_by_screenname(screenname)
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


@app.command()
def timeline(
    screenname: str = typer.Argument(..., help="Twitter username (without @)")
):
    """Get user's timeline (tweets)"""
    try:
        client = TwitterAPIClient()
        result = client.get_user_timeline(screenname)
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


@app.command()
def replies(
    screenname: str = typer.Argument(..., help="username to get replies for")
):
    """Get replies to a specific tweet"""
    try:
        client = TwitterAPIClient()
        result = client.get_user_replies(screenname)
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
