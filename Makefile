# Makefile for OpenCode configuration

FILES := AGENTS.md oh-my-openagent.json opencode.json tui.json
DIRECTORIES := agents commands

.PHONY: sync help

sync:
	@echo "🚀 Syncing OpenCode configuration..."
	@mkdir -p ~/.config/opencode
	@mkdir -p ~/.config/opencode/agents
	@mkdir -p ~/.config/opencode/commands
	@echo "✓ Created target directories"
	@for file in $(FILES); do \
		if [ -f "$$file" ]; then \
			cp -f "$$file" ~/.config/opencode/; \
		fi; \
	done
	@rm -rf ~/.config/opencode/agents/*
	@cp -r ./agents/* ~/.config/opencode/agents/ 2>/dev/null || true
	@rm -rf ~/.config/opencode/commands/*
	@cp -r ./commands/* ~/.config/opencode/commands/ 2>/dev/null || true
	@echo "🎉 Sync complete!"

help:
	@echo "  make sync    - Sync OpenCode configuration"
	@echo "  make help    - Show this message"
