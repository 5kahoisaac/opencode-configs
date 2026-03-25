# Makefile for OpenCode configuration

FILES := AGENTS.md opencode-historian.json oh-my-opencode.json opencode.json tui.json
DIRECTORIES := agents commands
SKILLS_CSV := skills.csv

.PHONY: sync sync-skills help

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
	@$(MAKE) sync-skills
	@echo "🎉 Sync complete!"

sync-skills:
	@echo "🔧 Syncing skills to global scope..."
	@npx skills ls -g --json 2>/dev/null > /tmp/installed_skills.json; \
	installed_names=$$(cat /tmp/installed_skills.json | grep -o '"name": *"[^"]*"' | cut -d'"' -f4 | sort -u); \
	csv_skills=$$(tail -n +2 $(SKILLS_CSV) | cut -d',' -f2 | sort -u); \
	echo "📋 Installed: $$(echo $$installed_names | wc -w | tr -d ' ') skills"; \
	echo "📋 CSV: $$(echo $$csv_skills | wc -w | tr -d ' ') skills"; \
	echo ""; \
	echo "🗑️  Removing obsolete skills..."; \
	for skill in $$installed_names; do \
		if ! echo "$$csv_skills" | grep -qw "$$skill"; then \
			echo "   ✗ Removing: $$skill"; \
			npx skills remove --skill "$$skill" -g -y 2>/dev/null || true; \
		fi; \
	done; \
	echo ""; \
	echo "📦 Processing CSV skills..."; \
	for skill in $$csv_skills; do \
		if echo "$$installed_names" | grep -qw "$$skill"; then \
			echo "   ✓ Already installed: $$skill"; \
		else \
			repo=$$(grep ",$$skill," $(SKILLS_CSV) | head -1 | cut -d',' -f1); \
			agents=$$(grep ",$$skill," $(SKILLS_CSV) | head -1 | cut -d',' -f3); \
			if [ -n "$$repo" ]; then \
				echo "   → Installing: $$skill"; \
				npx skills add "$$repo" --skill "$$skill" -g -a "$$agents" -y; \
			fi; \
		fi; \
	done; \
	echo ""; \
	echo "⬆️  Updating all skills..."; \
	npx skills update -g 2>/dev/null || true; \
	echo ""; \
	echo "✅ Skills sync complete"; \
	rm -f /tmp/installed_skills.json

help:
	@echo "  make sync          - Sync configuration and skills"
	@echo "  make sync-skills   - Sync skills from CSV"
	@echo "  make help          - Show this message"
