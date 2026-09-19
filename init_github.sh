#!/bin/bash

# Script to initialize and setup GitHub repository for Intelligent Observability & Event Watchdog Project
# Usage: ./init_github.sh <your_github_username> <your_repo_name>

set -e

echo "🚀 Setting up GitHub Repository for Intelligent Observability & Event Watchdog Project"
echo "=============================================="
echo ""

# Check if arguments provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./init_github.sh <github_username> <repository_name>"
    echo "Example: ./init_github.sh olu project3-observability"
    exit 1
fi

USERNAME=$1
REPO_NAME=$2
REMOTE_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"

echo "📦 Repository: ${USERNAME}/${REPO_NAME}"
echo "Remote URL: ${REMOTE_URL}"
echo ""

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "📂 Initializing Git repository..."
    git init
    
    # Add .gitignore if it exists
    if [ -f ".gitignore" ]; then
        git add .gitignore
    fi
else
    echo "✅ Git repository already initialized"
fi

# Configure git user (if not configured)
if ! git config user.email &>/dev/null; then
    read -p "Enter your GitHub email: " GIT_EMAIL
    read -p "Enter your name for commits: " GIT_NAME
    git config user.email "$GIT_EMAIL"
    git config user.name "$GIT_NAME"
fi

# Create initial commit with all project files
echo "📝 Creating initial commit..."
git add .
git commit -m "Initial commit: Project - Intelligent Observability & Event Watchdog

- FastAPI-based observability service
- SQLite database for logs and metrics
- Anomaly detection and alerting system
- Streamlit dashboard
- Prompts audit log included"

# Add remote repository
if [ -z "$(git remote -v)" ]; then
    git remote add origin "$REMOTE_URL"
    echo "✅ Remote repository added: $REMOTE_URL"
else
    echo "ℹ️  Remote repository already configured"
fi

echo ""
echo "📊 Current status:"
git status

echo ""
echo "🚀 Ready to push to GitHub!"
echo "Run: git push origin main"
echo ""
echo "💡 Pro Tips:"
echo "- Run 'git pull' before each Copilot session to get latest changes"
echo "- Keep your prompts.md file updated after every Copilot interaction"
echo "- Commit frequently with meaningful messages"
