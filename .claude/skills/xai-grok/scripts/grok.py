#!/usr/bin/env python3
"""
xAI Grok API integration script with agentic tool calling for Claude Code skills.
Usage: python grok.py "Your query here" [OPTIONS]

Available Grok 4 Models:
  - grok-4 (alias for grok-4-0709) - Highest quality model, 256k context [DEFAULT]
  - grok-4-fast-reasoning - Cost-efficient reasoning, 2M context
  - grok-4-fast-non-reasoning - Cost-efficient non-reasoning, 2M context

Features:
  - Agentic tool calling with real-time X (Twitter) search
  - Web search and page browsing
  - Code execution for calculations and analysis
  - Streaming mode with real-time progress (strongly recommended by xAI)
"""

import os
import sys
import typer
from dotenv import load_dotenv
from typing_extensions import Annotated

from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.tools import web_search, x_search, code_execution

# Initialize Typer app
app = typer.Typer(
    help="xAI Grok API integration with agentic tool calling for Claude Code skills.",
    epilog="""
        Available Grok 4 Models:
          grok-4                    Highest quality (256k context) [DEFAULT]
          grok-4-fast-reasoning     Cost-efficient reasoning (2M context)
          grok-4-fast-non-reasoning Cost-efficient non-reasoning (2M context)
    
        Examples:
          # Search X/Twitter for Israeli tech influencers (default: streaming with X + web search)
          python grok.py "Find recent tweets from Israeli tech nano-influencers"
    
          # Use all tools including code execution
          python grok.py "Analyze tech trends" --enable-code-execution
    
          # Basic chat without tools
          python grok.py "What is AI?" --disable-all-tools
    """,
    rich_markup_mode="rich"
)


@app.command()
def main(
    query: Annotated[str, typer.Argument(help="The query to send to Grok")],
    model: Annotated[str, typer.Option(
        "--model", "-m",
        help="Grok model to use"
    )] = "grok-4",
    temperature: Annotated[float, typer.Option(
        "--temperature", "-t",
        help="Temperature for response generation"
    )] = 0.3,
    disable_x_search: Annotated[bool, typer.Option(
        "--disable-x-search",
        help="Disable X (Twitter) search (enabled by default)"
    )] = False,
    disable_web_search: Annotated[bool, typer.Option(
        "--disable-web-search",
        help="Disable web search (enabled by default)"
    )] = False,
    enable_code_execution: Annotated[bool, typer.Option(
        "--enable-code-execution",
        help="Enable Python code execution (disabled by default)"
    )] = False,
    disable_all_tools: Annotated[bool, typer.Option(
        "--disable-all-tools",
        help="Disable all tools (basic chat mode)"
    )] = False,
    show_citations: Annotated[bool, typer.Option(
        "--show-citations/--no-show-citations",
        help="Show citations in output"
    )] = True,
    show_usage: Annotated[bool, typer.Option(
        "--show-usage",
        help="Show detailed token usage and tool call statistics"
    )] = False,
    show_tool_calls: Annotated[bool, typer.Option(
        "--show-tool-calls",
        help="Show all tool calls made during the request"
    )] = False,
):
    """
    Query xAI Grok 4 model with agentic tool calling.

    Tools (X search and web search enabled by default):
      - X (Twitter) search for real-time social media data
      - Web search for current information
      - Code execution (opt-in) for calculations and analysis
    """
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("XAI_API_KEY")

    if not api_key:
        typer.echo("Error: XAI_API_KEY not found in environment variables.", err=True)
        typer.echo("Please set XAI_API_KEY in your .env file.", err=True)
        raise typer.Exit(code=1)

    try:
        # Initialize xAI client
        client = Client(api_key=api_key)

        # Configure tools based on arguments (streaming mode always used per xAI recommendations)
        # X search and web search are enabled by default, code execution is opt-in
        tools = []
        if not disable_all_tools:
            if not disable_web_search:
                tools.append(web_search())
            if not disable_x_search:
                tools.append(x_search())
            if enable_code_execution:
                tools.append(code_execution())

        # Create chat with configured tools
        chat = client.chat.create(
            model=model,
            temperature=temperature,
            tools=tools if tools else None,
        )

        # Append user query
        chat.append(user(query))

        # Process response with streaming (strongly recommended by xAI for agentic workflows)
        if not tools:
            # Basic chat mode without tools (synchronous)
            response = chat.sample()
            typer.echo(response.content)
        else:
            # Streaming mode with real-time tool call visibility (recommended for agentic workflows)
            is_thinking = True
            for response, chunk in chat.stream():
                # Show tool calls as they happen
                if show_tool_calls:
                    for tool_call in chunk.tool_calls:
                        typer.echo(f"\n[Tool Call] {tool_call.function.name}: {tool_call.function.arguments}", err=True)

                # Show thinking progress
                if response.usage.reasoning_tokens and is_thinking:
                    typer.echo(f"\r[Thinking... {response.usage.reasoning_tokens} tokens]",
                              nl=False, err=True)

                # Print the final response content
                if chunk.content and is_thinking:
                    typer.echo("\n", nl=False, err=True)  # Clear the thinking line
                    is_thinking = False

                if chunk.content and not is_thinking:
                    typer.echo(chunk.content, nl=False)

            # Print newline after streaming
            typer.echo()

            # Show citations
            if show_citations and response.citations:
                typer.echo("\n\n=== Citations ===")
                for citation in response.citations:
                    typer.echo(f"  - {citation}")

            # Show usage statistics
            if show_usage:
                typer.echo("\n\n=== Usage Statistics ===")
                typer.echo(f"Completion tokens: {response.usage.completion_tokens}")
                typer.echo(f"Prompt tokens: {response.usage.prompt_tokens}")
                typer.echo(f"Reasoning tokens: {response.usage.reasoning_tokens}")
                typer.echo(f"Total tokens: {response.usage.total_tokens}")
                if response.server_side_tool_usage:
                    typer.echo(f"\nTool usage: {response.server_side_tool_usage}")
                    typer.echo(f"\nTool calls summary:")
                    for tool_call in response.tool_calls:
                        typer.echo(f"  {tool_call.function.name}: {tool_call.function.arguments}")

    except Exception as e:
        typer.echo(f"Error querying Grok: {str(e)}", err=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()