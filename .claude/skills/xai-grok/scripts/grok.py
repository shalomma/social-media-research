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
import argparse
from dotenv import load_dotenv

try:
    from xai_sdk import Client
    from xai_sdk.chat import user
    from xai_sdk.tools import web_search, x_search, code_execution
except ImportError:
    print("Error: xai-sdk package not found.", file=sys.stderr)
    print("Please install it with: pip install xai-sdk>=1.3.1", file=sys.stderr)
    sys.exit(1)


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Query xAI Grok 4 model with agentic tool calling',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Available Grok 4 Models:
                grok-4                    Highest quality (256k context) [DEFAULT]
                grok-4-fast-reasoning     Cost-efficient reasoning (2M context)
                grok-4-fast-non-reasoning Cost-efficient non-reasoning (2M context)
            
            Tools (X search and web search enabled by default):
                --disable-x-search        Disable X (Twitter) search
                --disable-web-search      Disable web search
                --enable-code-execution   Enable Python code execution (opt-in)
                --disable-all-tools       Disable all tools (basic chat mode)
            
            Examples:
                # Search X/Twitter for Israeli tech influencers (default: streaming with X + web search)
                python grok.py "Find recent tweets from Israeli tech nano-influencers"
            
                # Use all tools including code execution
                python grok.py "Analyze tech trends" --enable-code-execution
            
                # Basic chat without tools
                python grok.py "What is AI?" --disable-all-tools
        """
    )
    parser.add_argument('query', type=str, help='The query to send to Grok')
    parser.add_argument('--model', type=str, default='grok-4',
                        help='Grok model to use (default: grok-4)')
    parser.add_argument('--temperature', type=float, default=0.7,
                        help='Temperature for response generation (default: 0.7)')
    parser.add_argument('--disable-x-search', action='store_true',
                        help='Disable X (Twitter) search (enabled by default)')
    parser.add_argument('--disable-web-search', action='store_true',
                        help='Disable web search (enabled by default)')
    parser.add_argument('--enable-code-execution', action='store_true',
                        help='Enable Python code execution (disabled by default)')
    parser.add_argument('--disable-all-tools', action='store_true',
                        help='Disable all tools (basic chat mode)')
    parser.add_argument('--show-citations', action='store_true', default=True,
                        help='Show citations in output (default: enabled)')
    parser.add_argument('--show-usage', action='store_true',
                        help='Show detailed token usage and tool call statistics')
    parser.add_argument('--show-tool-calls', action='store_true',
                        help='Show all tool calls made during the request')

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("XAI_API_KEY")

    if not api_key:
        print("Error: XAI_API_KEY not found in environment variables.", file=sys.stderr)
        print("Please set XAI_API_KEY in your .env file.", file=sys.stderr)
        sys.exit(1)

    try:
        # Initialize xAI client
        client = Client(api_key=api_key)

        # Configure tools based on arguments (streaming mode always used per xAI recommendations)
        # X search and web search are enabled by default, code execution is opt-in
        tools = []
        if not args.disable_all_tools:
            if not args.disable_web_search:
                tools.append(web_search())
            if not args.disable_x_search:
                tools.append(x_search())
            if args.enable_code_execution:
                tools.append(code_execution())

        # Create chat with configured tools
        chat = client.chat.create(
            model=args.model,
            tools=tools if tools else None,
        )

        # Append user query
        chat.append(user(args.query))

        # Process response with streaming (strongly recommended by xAI for agentic workflows)
        if not tools:
            # Basic chat mode without tools (synchronous)
            response = chat.sample()
            print(response.content)
        else:
            # Streaming mode with real-time tool call visibility (recommended for agentic workflows)
            is_thinking = True
            for response, chunk in chat.stream():
                # Show tool calls as they happen
                if args.show_tool_calls:
                    for tool_call in chunk.tool_calls:
                        print(f"\n[Tool Call] {tool_call.function.name}: {tool_call.function.arguments}",
                              file=sys.stderr)

                # Show thinking progress
                if response.usage.reasoning_tokens and is_thinking:
                    print(f"\r[Thinking... {response.usage.reasoning_tokens} tokens]",
                          end="", flush=True, file=sys.stderr)

                # Print the final response content
                if chunk.content and is_thinking:
                    print("\n", file=sys.stderr)  # Clear the thinking line
                    is_thinking = False

                if chunk.content and not is_thinking:
                    print(chunk.content, end="", flush=True)

            # Print newline after streaming
            print()

            # Show citations
            if args.show_citations and response.citations:
                print("\n\n=== Citations ===")
                for citation in response.citations:
                    print(f"  - {citation}")

            # Show usage statistics
            if args.show_usage:
                print("\n\n=== Usage Statistics ===")
                print(f"Completion tokens: {response.usage.completion_tokens}")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Reasoning tokens: {response.usage.reasoning_tokens}")
                print(f"Total tokens: {response.usage.total_tokens}")
                if response.server_side_tool_usage:
                    print(f"\nTool usage: {response.server_side_tool_usage}")
                    print(f"\nTool calls summary:")
                    for tool_call in response.tool_calls:
                        print(f"  {tool_call.function.name}: {tool_call.function.arguments}")

    except Exception as e:
        print(f"Error querying Grok: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()