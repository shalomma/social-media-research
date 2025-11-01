import json
import typer
import requests

from client import TwitterAPIClient


# Create Typer app
app = typer.Typer(help="Twitter API client for twitterapi.io endpoints")


@app.command()
def userinfo(
    screenname: str = typer.Argument(..., help="Twitter username (without @)")
):
    """Get user information"""
    try:
        client = TwitterAPIClient()
        result = client.get_user_info(screenname)
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


if __name__ == "__main__":
    app()
