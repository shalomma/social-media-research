#!/usr/bin/env python3
"""
Simple CLI for Israeli Tech Nano-Influencers SQLite Database.
Provides direct SQL query access and schema inspection.
"""

import json
import os
import re
import sqlite3
from pathlib import Path
from typing import Optional

import typer

# Create Typer app
app = typer.Typer(help="Israeli Tech Nano-Influencers Database - Simple SQL Interface")

# Safety mode - set to False to allow destructive operations
SAFE_MODE = os.environ.get("DB_SAFE_MODE", "true").lower() == "true"

# Database path relative to project root
# From: .claude/skills/influencer-db/src/client.py
# Up to: project root (5 levels up)
DB_PATH = Path(__file__).parent.parent.parent.parent.parent / "influencers.db"


def get_connection() -> sqlite3.Connection:
    """Get database connection."""
    db_path = Path(DB_PATH)

    # Initialize database if it doesn't exist
    if not db_path.exists():
        initialize_database(db_path)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database(db_path: Path):
    """Initialize database with schema."""
    schema_path = Path(__file__).parent / "schema.sql"

    with sqlite3.connect(db_path) as conn:
        with open(schema_path, "r") as f:
            conn.executescript(f.read())
        conn.commit()


def validate_sql_safety(sql: str) -> tuple[bool, str]:
    """
    Validate SQL query for safety in safe mode.
    Returns (is_safe, error_message).

    Blocks:
    - DROP (TABLE, INDEX, VIEW, TRIGGER)
    - TRUNCATE
    - DELETE without WHERE clause
    - ALTER TABLE DROP

    Allows:
    - SELECT
    - INSERT
    - UPDATE (with or without WHERE)
    - DELETE with WHERE clause
    - ALTER TABLE ADD
    """
    if not SAFE_MODE:
        return True, ""

    # Normalize SQL for analysis (remove extra whitespace, make uppercase)
    normalized = re.sub(r'\s+', ' ', sql.strip().upper())

    # Block DROP commands
    if re.match(r'^DROP\s+(TABLE|INDEX|VIEW|TRIGGER)', normalized):
        return False, "DROP commands are blocked in safe mode. Set DB_SAFE_MODE=false to allow."

    # Block TRUNCATE
    if normalized.startswith('TRUNCATE'):
        return False, "TRUNCATE commands are blocked in safe mode. Set DB_SAFE_MODE=false to allow."

    # Block DELETE without WHERE clause
    if re.match(r'^DELETE\s+FROM\s+\w+\s*$', normalized) or \
       re.match(r'^DELETE\s+FROM\s+\w+\s*;', normalized):
        return False, "DELETE without WHERE clause is blocked in safe mode. Add a WHERE clause or set DB_SAFE_MODE=false."

    # Block ALTER TABLE DROP
    if re.match(r'^ALTER\s+TABLE.*DROP', normalized):
        return False, "ALTER TABLE DROP is blocked in safe mode. Set DB_SAFE_MODE=false to allow."

    return True, ""


@app.command()
def query(
    sql: str = typer.Argument(..., help="SQL query to execute"),
    params: Optional[str] = typer.Option(None, "--params", "-p", help="JSON array of query parameters"),
    unsafe: bool = typer.Option(False, "--unsafe", help="Disable safe mode for this query"),
):
    """
    Execute a SQL query and return results as JSON.

    Safe mode is ENABLED by default, blocking: DROP, TRUNCATE, DELETE without WHERE.
    To disable: use --unsafe flag or set DB_SAFE_MODE=false environment variable.

    Examples:

    \b
    # SELECT queries
    python3 client.py query "SELECT * FROM influencers LIMIT 5"
    python3 client.py query "SELECT * FROM influencers WHERE location LIKE '%Tel Aviv%'"
    python3 client.py query "SELECT * FROM influencers WHERE follower_count > 1000"

    \b
    # With parameters (for safety)
    python3 client.py query "SELECT * FROM influencers WHERE twitter_handle = ?" --params '["example_user"]'

    \b
    # INSERT
    python3 client.py query "INSERT INTO influencers (twitter_handle, name, location) VALUES ('test', 'Test User', 'Tel Aviv')"

    \b
    # UPDATE
    python3 client.py query "UPDATE influencers SET follower_count = 2000 WHERE twitter_handle = 'test'"

    \b
    # DELETE
    python3 client.py query "DELETE FROM influencers WHERE twitter_handle = 'test'"

    \b
    # Aggregations
    python3 client.py query "SELECT COUNT(*) as total FROM influencers"
    python3 client.py query "SELECT location, COUNT(*) as count FROM influencers GROUP BY location"
    """
    try:
        # Validate SQL safety in safe mode (unless --unsafe flag is used)
        if not unsafe:
            is_safe, error_msg = validate_sql_safety(sql)
            if not is_safe:
                typer.secho(f"⚠️  {error_msg}", fg=typer.colors.RED, err=True)
                raise typer.Exit(1)
        elif SAFE_MODE:
            typer.secho("⚠️  Running in unsafe mode for this query...", fg=typer.colors.YELLOW)

        # Parse parameters if provided
        query_params = []
        if params:
            query_params = json.loads(params)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, query_params)

            # Check if this is a SELECT query (returns rows)
            if sql.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                results = [dict(row) for row in rows]
                typer.echo(json.dumps(results, indent=2, default=str))
            else:
                # For INSERT, UPDATE, DELETE
                conn.commit()
                typer.echo(json.dumps({
                    "success": True,
                    "rowcount": cursor.rowcount,
                    "lastrowid": cursor.lastrowid
                }, indent=2))

    except sqlite3.Error as e:
        typer.secho(f"Database error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
    except json.JSONDecodeError as e:
        typer.secho(f"Invalid JSON in params: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@app.command()
def schema(
    table: Optional[str] = typer.Argument(None, help="Specific table name (influencers)"),
):
    """
    Show database schema information.

    Examples:

    \b
    # Show all tables and their schemas
    python3 client.py schema

    \b
    # Show schema for specific table
    python3 client.py schema influencers
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            if table:
                # Show schema for specific table
                cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,))
                result = cursor.fetchone()

                if result:
                    typer.echo(f"\n{table} schema:\n")
                    typer.echo(result['sql'])
                    typer.echo()

                    # Show indexes for this table
                    cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name=?", (table,))
                    indexes = cursor.fetchall()
                    if indexes:
                        typer.echo(f"\nIndexes:")
                        for idx in indexes:
                            if idx['sql']:  # Skip auto-created indexes
                                typer.echo(idx['sql'])
                else:
                    typer.secho(f"Table '{table}' not found", fg=typer.colors.YELLOW)
                    raise typer.Exit(1)
            else:
                # Show all tables and their schemas
                cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name")
                tables = cursor.fetchall()

                schema_info = {
                    "tables": {}
                }

                for tbl in tables:
                    table_name = tbl['name']

                    # Get column info
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()

                    schema_info["tables"][table_name] = {
                        "columns": [dict(col) for col in columns],
                        "create_statement": tbl['sql']
                    }

                    # Get indexes
                    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name=?", (table_name,))
                    indexes = cursor.fetchall()
                    if indexes:
                        schema_info["tables"][table_name]["indexes"] = [idx['sql'] for idx in indexes if idx['sql']]

                typer.echo(json.dumps(schema_info, indent=2))

    except sqlite3.Error as e:
        typer.secho(f"Database error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
