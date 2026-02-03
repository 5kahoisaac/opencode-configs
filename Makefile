# Makefile for building OpenCode configuration with .env variables

# Define the JSONC files to process
JSONC_FILES := oh-my-opencode.jsonc opencode.jsonc supermemory.jsonc
DIRECTORIES := agents commands skills

# Main targets
.PHONY: all build clean help

all: build

build:
	@echo "🔨 Building OpenCode configuration..."
	@echo ""
	
	# Create and clean output directory
	@mkdir -p ./dist
	@rm -rf ./dist/*
	@echo "✓ Created and cleaned ./dist directory"
	
	# Load environment variables and process config files
	@echo "📋 Loading environment variables from .env..."
	@( \
		set -a; \
		. .env; \
		for file in $(JSONC_FILES); do \
			if [ -f "$$file" ]; then \
				echo "⚙️ Processing $$file..."; \
				envsubst < "$$file" > "./dist/$$file"; \
				echo "✅ $$file processed"; \
			fi; \
		done \
	)
	
	# Copy directories
	@for dir in $(DIRECTORIES); do \
		if [ -d "$$dir" ]; then \
			echo "📁 Copying $$dir..."; \
			cp -r "$$dir" "./dist/"; \
			echo "✅ $$dir copied"; \
		fi; \
		done
	@echo ""
	@echo "🎉 Build complete! OpenCode configuration saved to ./dist"
	@echo ""
	@echo "📁 Output summary:"
	@ls -la ./dist/

clean:
	@rm -rf ./dist
	@echo "🗑️ Cleaned ./dist directory"

help:
	@echo "📖 Available Makefile targets:"
	@echo ""
	@echo "  make all     - Build OpenCode config with .env (default)"
	@echo "  make build   - Build OpenCode configuration with .env variables"
	@echo "  make clean   - Remove ./dist directory"
	@echo "  make help    - Show this help message"
	@echo ""
	@echo "📝 This Makefile:"
	@echo "  1. Loads environment variables from .env"
	@echo "  2. Substitutes \$$VAR_NAME placeholders in JSONC files"
	@echo "  3. Outputs processed files to ./dist directory"
	@echo "  4. Copies agents, commands, and skills to ./dist"
