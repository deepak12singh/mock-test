#!/bin/bash

# File list to delete
FILES=(
  "Exam Prep Site Report.pdf"
  "README.md"
  "db - Copy.sqlite3"
  "db.sqlite3"
  "env.txt"
  "my_schema.pdf"
)

# Loop through files and delete if they exist
for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "Deleting: $file"
    rm "$file"
  else
    echo "Not found (skip): $file"
  fi
done

echo "✅ Done!"
