#!/usr/bin/env python3
"""
Interactive Claude chat with streaming responses
Usage: python claude_chat.py

Features:
- Maintains conversation context
- Streaming responses (see text as it's generated)
- Type 'quit' or 'exit' to end
"""

import os
import sys
from anthropic import Anthropic

def chat():
    """Start an interactive chat session with Claude"""

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

    print("🤖 Claude Terminal Chat (Sonnet 3.5)")
    print("=" * 50)
    print("Type your questions below")
    print("Commands: 'quit' or 'exit' to end, 'clear' to reset\n")

    conversation = []

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋\n")
                break

            if user_input.lower() == 'clear':
                conversation = []
                print("\n✨ Conversation cleared!\n")
                continue

            if not user_input:
                continue

            # Add to conversation
            conversation.append({"role": "user", "content": user_input})

            print("\nClaude: ", end="", flush=True)

            # Stream response
            response_text = ""
            try:
                with client.messages.stream(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4096,
                    messages=conversation
                ) as stream:
                    for text in stream.text_stream:
                        print(text, end="", flush=True)
                        response_text += text
            except Exception as e:
                print(f"\n❌ Error: {e}")
                conversation.pop()  # Remove last message
                continue

            print("\n")

            # Add assistant response to conversation
            conversation.append({"role": "assistant", "content": response_text})

        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'quit' to exit or continue chatting.\n")
            continue

if __name__ == "__main__":
    chat()
