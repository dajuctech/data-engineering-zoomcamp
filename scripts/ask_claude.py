#!/usr/bin/env python3
"""
Simple CLI tool to ask Claude questions from terminal
Usage: python ask_claude.py "Your question here"

Setup:
1. Install: pip install anthropic
2. Set API key: export ANTHROPIC_API_KEY="your-key-here"
3. Run: python ask_claude.py "What is dbt?"
"""

import os
import sys
from anthropic import Anthropic

def ask_claude(question, model="claude-3-5-sonnet-20241022"):
    """Ask Claude a question and get a response"""

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set!")
        print("\nTo fix:")
        print('  export ANTHROPIC_API_KEY="sk-ant-api03-YOUR-KEY-HERE"')
        print("\nGet your key at: https://console.anthropic.com/settings/keys")
        sys.exit(1)

    # Initialize client
    try:
        client = Anthropic(api_key=api_key)
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        sys.exit(1)

    # Create message
    try:
        message = client.messages.create(
            model=model,
            max_tokens=2048,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"❌ Error calling API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ask_claude.py 'Your question'")
        print("\nExamples:")
        print("  python ask_claude.py 'Explain dbt in simple terms'")
        print("  python ask_claude.py 'What is the difference between partitioning and clustering?'")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    print(f"\n🤔 Question: {question}\n")
    print("💭 Thinking...\n")

    response = ask_claude(question)
    print(f"💬 Claude:\n{response}\n")
