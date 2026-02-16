#!/bin/bash
#
# Setup script for Claude API terminal access
# Usage: bash setup_claude_api.sh
#

set -e

echo "🤖 Claude API Terminal Setup"
echo "=============================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Install it first: sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed!"
    echo "Install it: sudo apt-get install python3-pip"
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Install Anthropic SDK
echo ""
echo "📦 Installing Anthropic Python SDK..."
pip3 install anthropic --quiet

echo "✅ Anthropic SDK installed"

# Install jq for JSON parsing
echo ""
echo "📦 Installing jq (for JSON parsing)..."
if ! command -v jq &> /dev/null; then
    sudo apt-get update -qq
    sudo apt-get install -y jq -qq
    echo "✅ jq installed"
else
    echo "✅ jq already installed"
fi

# Make scripts executable
echo ""
echo "🔧 Making scripts executable..."
chmod +x scripts/ask_claude.py
chmod +x scripts/claude_chat.py
echo "✅ Scripts are now executable"

# Create bash function
echo ""
echo "🔧 Setting up bash function..."

BASH_FUNCTION='
# Claude API quick query function
ask() {
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "❌ Error: ANTHROPIC_API_KEY not set!"
        echo "Set it with: export ANTHROPIC_API_KEY=\"your-key-here\""
        return 1
    fi

    local question="$*"
    curl -s https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data "{
        \"model\": \"claude-3-5-sonnet-20241022\",
        \"max_tokens\": 2048,
        \"messages\": [{\"role\": \"user\", \"content\": \"$question\"}]
      }" | jq -r ".content[0].text"
}
'

# Add to bashrc if not already there
if ! grep -q "Claude API quick query function" ~/.bashrc; then
    echo "$BASH_FUNCTION" >> ~/.bashrc
    echo "✅ Bash function 'ask()' added to ~/.bashrc"
else
    echo "✅ Bash function 'ask()' already in ~/.bashrc"
fi

# Check for API key
echo ""
echo "🔑 Checking for API key..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY is not set"
    echo ""
    echo "To set your API key:"
    echo "  1. Go to: https://console.anthropic.com/settings/keys"
    echo "  2. Create a new API key"
    echo "  3. Run this command:"
    echo "     export ANTHROPIC_API_KEY=\"sk-ant-api03-YOUR-KEY-HERE\""
    echo ""
    echo "To make it permanent, add to ~/.bashrc:"
    echo "     echo 'export ANTHROPIC_API_KEY=\"sk-ant-api03-YOUR-KEY-HERE\"' >> ~/.bashrc"
else
    echo "✅ ANTHROPIC_API_KEY is set (${ANTHROPIC_API_KEY:0:20}...)"
fi

echo ""
echo "=============================="
echo "✅ Setup Complete!"
echo "=============================="
echo ""
echo "Available commands:"
echo "  1. Quick questions:  ask 'What is dbt?'"
echo "  2. Python CLI:       python3 scripts/ask_claude.py 'Your question'"
echo "  3. Interactive chat: python3 scripts/claude_chat.py"
echo "  4. curl (manual):    See claude-terminal-setup.md"
echo ""
echo "To activate bash function in current session:"
echo "  source ~/.bashrc"
echo ""
echo "Documentation: claude-terminal-setup.md"
echo ""
