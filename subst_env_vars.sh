#!/bin/bash
# Script to replace $ENV_KEY patterns with values from .env file

# Process each .env line
while IFS= read -r line || [ -n "$line" ]; do
    # Trim whitespace
    trimmed=$(echo "$line" | xargs)
    
    # Skip empty lines and comments
    if [ -z "$trimmed" ] || [[ "$trimmed" == \#* ]]; then
        continue
    fi
    
    # Split by first "=" to get key and value
    key="${line%%=*}"
    value="${line#*=}"
    
    # Trim key and value
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)
    
    # Create pattern to search for in files
    pattern="\$$key"
    
    # Check if pattern exists in any of the target files
    found=false
    for file in "$@"; do
        if [ -f "$file" ] && grep -q "$pattern" "$file"; then
            found=true
            break
        fi
    done
    
    # Only process if pattern was found in at least one file
    if [ "$found" = true ]; then
        for file in "$@"; do
            if [ -f "$file" ] && grep -q "$pattern" "$file"; then
                echo "⚙️ Replacing $pattern in $file..."
                sed -i '' "s|$pattern|$value|g" "$file"
            fi
        done
    else
        echo "⚠️ No matches found for $pattern in the config files. Please verify this key exists in your configuration files."
    fi
done < .env

echo "✅ Environment variables substituted"
