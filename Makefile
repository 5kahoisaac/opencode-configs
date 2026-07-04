# Makefile for OpenCode configuration

FILES := AGENTS.md oh-my-openagent.json opencode.json tui.json
DIRECTORIES := agents commands

.PHONY: sync help check

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
	@if [ -d ./agents ]; then \
		rm -rf ~/.config/opencode/agents/*; \
		cp -r ./agents/* ~/.config/opencode/agents/ 2>/dev/null || true; \
	fi
	@if [ -d ./commands ]; then \
		rm -rf ~/.config/opencode/commands/*; \
		cp -r ./commands/* ~/.config/opencode/commands/ 2>/dev/null || true; \
	fi
	@echo "🎉 Sync complete!"

check:
	@python3 scripts/check-config.py

help:
	@echo "  make sync    - Sync OpenCode configuration"
	@echo "  make help    - Show this message"
	@echo "  make check   - Validate config cross-references and drift"
