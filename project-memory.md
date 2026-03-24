# Project Memory
Last updated: 2026-03-24

This file captures decisions, reasoning, and session context that
project-context.md doesn't hold. It is Claude's memory between sessions.

---

## Key decisions (permanent record)

---

## Sessions

## Session — 2026-03-24

**Focus:** Upgrade project to new session management system — add .claude/commands/ folder with /start-of-day, /end-of-day, /new-project skills; create project-memory.md.

**Decisions made:**
- Adopted .claude/commands/ as the location for custom slash commands — this is the Claude Code convention for project-scoped skills.
- project-memory.md replaces the old captains-log.md pattern — session context now lives here, not in a separate log file.
- No captains-log.md existed in this project, so no archive migration was needed.

**Files changed this session:**
 .claude/commands/end-of-day.md   | new file
 .claude/commands/new-project.md  | new file
 .claude/commands/start-of-day.md | new file
 project-memory.md                | new file

