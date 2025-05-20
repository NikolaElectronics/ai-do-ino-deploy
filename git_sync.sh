#!/bin/bash

echo "🔍 Checking for changes..."

# Stagiem toate fișierele modificate
git add .

# Setăm un mesaj implicit de commit (sau folosești $1 pentru unul personalizat)
commit_msg=${1:-"Sync changes"}
git commit -m "$commit_msg"

# Tragem modificările de pe GitHub și rezolvăm cu rebase
git pull origin main --rebase

# Împingem la GitHub
git push origin main

echo "✅ Repo updated with message: $commit_msg"
