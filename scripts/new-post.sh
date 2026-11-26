#!/usr/bin/env bash
set -euo pipefail

echo ""
read -rp "Post title: " TITLE
read -rp "Category (AI/Development/Knowledge/Project): " CATEGORY

# Slug: trim, lowercase, collapse whitespace runs into "_"
SLUG=$(printf '%s' "$TITLE" \
  | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[[:space:]]+/_/g')

if [ -z "$SLUG" ]; then
  echo "Title is empty." >&2
  exit 1
fi

FULL_PATH="content/posts/${SLUG}/index.md"

if [ -e "$FULL_PATH" ]; then
  echo "Already exists: ${FULL_PATH}" >&2
  exit 1
fi

# ISO 8601 with local offset, e.g. 2026-11-26T16:52:10+09:00 (works with BSD and GNU date)
NOW=$(date +%Y-%m-%dT%H:%M:%S%z | sed -E 's/([0-9]{2})$/:\1/')

if [ -n "$CATEGORY" ]; then
  CATEGORIES="[\"${CATEGORY}\"]"
else
  CATEGORIES="[]"
fi

echo ""
echo "Creating ${FULL_PATH}"

mkdir -p "$(dirname "$FULL_PATH")"

cat > "$FULL_PATH" << EOF
---
title: "${TITLE}"
description: ""
summary: ""
date: ${NOW}
lastmod: ${NOW}
draft: true
weight: 50
categories: ${CATEGORIES}
tags: []
contributors: []
pinned: false
homepage: false
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

EOF

echo ""
echo "✓ Created: ${FULL_PATH}"
echo ""
echo "Please edit the file to add your content and update the front matter."
