# Makefile for building OpenCode configuration with .env variables

# Define the files to process
FILES := AGENTS.md oh-my-opencode-slim.jsonc opencode.jsonc
DIRECTORIES := agents commands skills

# Main targets
.PHONY: build clean migrate help

build: clean
	@echo "🔨 Building OpenCode configuration..."
	@echo ""
	
	# Create and clean output directory
	@mkdir -p ./dist
	@echo "✓ Created ./dist directory"
	
	# Copy JSONC files to dist directory first
	@for file in $(FILES); do \
		if [ -f "$$file" ]; then \
			echo "📋 Copying $$file to dist..."; \
			cp "$$file" "./dist/"; \
		fi; \
		done
	
	# Load environment variables and process config files in dist
	@echo "🔄 Substituting environment variables..."
	@./subst_env_vars.sh ./dist/*.jsonc
	
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

migrate: build
	@echo "🚀 Migrating OpenCode configuration..."
	@echo ""
	
	# Ensure target directories exist
	@mkdir -p ~/.config/opencode
	@mkdir -p ~/.agents/skills
	@mkdir -p ~/.config/opencode/agents
	@mkdir -p ~/.config/opencode/commands
	@mkdir -p ~/.config/opencode/skills
	@mkdir -p ~/.config/opencode/oh-my-opencode-slim
	@echo "✓ Created target directories"
	@echo ""
	
	# Migrate individual files (not folders) from ./dist to ~/.config/opencode/
	@echo "📋 Migrating configuration files..."
	@for file in $(FILES); do \
		if [ -f "./dist/$$file" ]; then \
			echo "  → Moving $$file"; \
			cp -f "./dist/$$file" ~/.config/opencode/; \
		fi; \
		done
	@echo "✓ Configuration files migrated"
	@echo ""


	# Migrate oh-my-opencode-slim folder
	@echo "📁 Migrating oh-my-opencode-slim folder..."
	@rm -rf ~/.config/opencode/oh-my-opencode-slim/*
	@cp -r ./dist/oh-my-opencode-slim/* ~/.config/opencode/oh-my-opencode-slim/ 2>/dev/null || true
	@echo "✓ oh-my-opencode-slim folder migrated"
	@echo ""
	
	# Migrate agents folder
	@echo "📁 Migrating agents folder..."
	@rm -rf ~/.config/opencode/agents/*
	@cp -r ./dist/agents/* ~/.config/opencode/agents/ 2>/dev/null || true
	@echo "✓ agents folder migrated"
	@echo ""
	
	# Migrate commands folder
	@echo "📁 Migrating commands folder..."
	@rm -rf ~/.config/opencode/commands/*
	@cp -r ./dist/commands/* ~/.config/opencode/commands/ 2>/dev/null || true
	@echo "✓ commands folder migrated"
	@echo ""
	
	# Migrate skills folder to ~/.agents/skills/
	@echo "📁 Migrating skills folder to ~/.agents/skills/..."
	@rm -rf ~/.agents/skills/*
	@cp -r ./dist/skills/* ~/.agents/skills/ 2>/dev/null || true
	@echo "✓ skills copied to ~/.agents/skills/"
	
	# Clear and symlink skills from ~/.agents/skills/ to ~/.config/opencode/skills/
	@echo "🔗 Creating symlinks in ~/.config/opencode/skills/..."
	@rm -rf ~/.config/opencode/skills/*
	@for skill_dir in ~/.agents/skills/*/; do \
		skill_name=$$(basename "$$skill_dir"); \
		if [ "$$skill_name" != "*" ]; then \
			echo "  → Linking $$skill_name"; \
			ln -sf ../../../.agents/skills/$$skill_name ~/.config/opencode/skills/$$skill_name; \
		fi; \
		done
	@echo "✓ skills symlinks created"
	@echo ""
	
	@echo "🎉 Migration complete!"

help:
	@echo "📖 Available Makefile targets:"
	@echo ""
	@echo "  make build   - Build OpenCode configuration with .env variables"
	@echo "  make clean   - Remove ./dist directory"
	@echo "  make migrate - Migrate build output to global OpenCode config locations"
	@echo "  make help    - Show this help message"
	@echo ""
	@echo "📝 This Makefile:"
	@echo "  1. Loads environment variables from .env"
	@echo "  2. Substitutes $$VAR_NAME placeholders in JSONC files (only .env variables)"
	@echo "  3. Outputs processed files to ./dist directory"
	@echo "  4. Copies agents, commands, and skills to ./dist"
	@echo "  5. Migrates dist content to ~/.config/opencode/ and ~/.agents/skills/"
