#!/usr/bin/env python3
"""
xAI Grok API integration script for Claude Code skills.
Usage: python grok.py "Your query here" [--model MODEL_NAME]

Available Grok 4 Models:
  - grok-4-0709 (alias: grok-4) - Highest quality model, 256k context [DEFAULT]
  - grok-4-fast-reasoning - Cost-efficient reasoning, 2M context
  - grok-4-fast-non-reasoning - Cost-efficient non-reasoning, 2M context
"""

import sys
import dotenv
import argparse
from openai import OpenAI


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Query xAI Grok 4 model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Available Grok 4 Models:
                grok-4-0709               Highest quality (256k context) [DEFAULT]
                grok-4-fast-reasoning     Cost-efficient reasoning (2M context)
                grok-4-fast-non-reasoning Cost-efficient non-reasoning (2M context)
        """
    )
    parser.add_argument('query', type=str, help='The query to send to Grok')
    parser.add_argument('--model', type=str, default='grok-4-0709',
                        help='Grok model to use (default: grok-4-0709)')
    parser.add_argument('--temperature', type=float, default=0.7,
                        help='Temperature for response generation (default: 0.7)')

    args = parser.parse_args()

    # Load environment variables
    dotenv.load_dotenv()

    # Get API key
    api_key = dotenv.get_key(dotenv.find_dotenv(), "XAI_API_KEY")
    if not api_key:
        print("Error: XAI_API_KEY not found in environment variables.", file=sys.stderr)
        print("Please set XAI_API_KEY in your .env file.", file=sys.stderr)
        sys.exit(1)

    try:
        # Initialize OpenAI client with xAI endpoint
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1",
        )

        # Create completion using responses API
        completion = client.responses.create(
            model=args.model,
            input=args.query,
            temperature=args.temperature
        )

        # Output the response (responses API returns output array with message content)
        print(completion.output[0].content[0].text)

    except Exception as e:
        print(f"Error querying Grok: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
