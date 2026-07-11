#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# --- CONFIGURATION ---
BRANCH="main" # Change this to your default branch if it's 'master' or something else
REMOTE="origin"
# ---------------------

echo "========================================"
echo "🚀 Starting Git Push & Shutdown Sequence"
echo "========================================"

# 1. Check if we are inside a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "❌ Error: This directory is not a Git repository."
    exit 1
fi

# 2. Stage all changes
echo "📦 Staging changes..."
git add .

# 3. Commit changes
# Uses a default timestamp message if no argument is passed to the script
COMMIT_MSG="${1:-"Auto-commit before shutdown on $(date +'%Y-%m-%d %H:%M:%S')"}"
echo "📝 Committing with message: '$COMMIT_MSG'"
git commit -m "$COMMIT_MSG" || echo "ℹ️ Nothing new to commit."

# 4. Push to remote
echo "📤 Pushing to $REMOTE/$BRANCH..."
if git push $REMOTE $BRANCH; then
    echo "✅ Git push successful!"
else
    echo "❌ Git push failed! Aborting shutdown to prevent data loss."
    exit 1
fi

# 5. Shutdown the system
# echo "🛑 Shutting down the system in 10 seconds..."
# echo "⏳ Press Ctrl+C now to cancel the shutdown."
# sleep 10

# echo "🔌 Shutting down now. Goodbye!"
# sudo shutdown -h now
