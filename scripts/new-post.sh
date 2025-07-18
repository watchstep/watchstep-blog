set -euo pipefail

echo ""
read -rp "Post title: " TITLE
read -rp "Category (AI/Development/Knowledge/Project): " CATEGORY

# Extract year and month
YEAR=$(date +%Y)
MONTH=$(date +%m)

# Create slug for folder name (same logic as batch script)
SLUG="$TITLE"

# Remove leading and trailing spaces
SLUG=$(echo "$SLUG" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

# Convert to lowercase (simple and reliable)
SLUG=$(echo "$SLUG" | tr '[:upper:]' '[:lower:]')

# Convert consecutive spaces to single underscore
SLUG=$(echo "$SLUG" | sed 's/[[:space:]]\+/_/g')

# Create folder path
DIR="blog/${YEAR}/${MONTH}/${SLUG}"
PATH_MD="${DIR}/index.md"
FULL_PATH="content/${PATH_MD}"

echo ""
echo "Creating ${FULL_PATH}"

# Create directory
mkdir -p "$(dirname "${FULL_PATH}")"

# Create file directly (same as batch script)
cat > "${FULL_PATH}" << EOF
---
title: "${TITLE}"
description: ""
summary: ""
date: $(date -Iseconds)+09:00
lastmod: $(date -Iseconds)+09:00
draft: true
weight: 50
categories: []
tags: []
contributors: []
pinned: false
homepage: false
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  robots: "" # custom robot tags (optional)
---

EOF

echo ""
echo "✓ Created: ${FULL_PATH}"
echo ""
echo "Please edit the file to add your content and update the front matter."
echo "Note: Title in the file is set to: ${TITLE}"
