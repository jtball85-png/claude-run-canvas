---
name: sync-tools
description: Pull the latest agents/skills/commands from library/ in the Claude-Projects-Templates repo into this project, without overwriting anything customized without asking first.
---

# Sync Tools — Pull Latest from library/

Execute these steps in order. Do not skip the confirmation step, even if every component looks new.

---

## 1. Fetch the library

Clone the templates repo into a temp folder, shallow:

```bash
git clone --depth 1 https://github.com/jtball85-png/Claude-Projects-Templates.git .sync-tools-tmp
```

If the clone fails (auth, network, repo not found), stop and show the user the exact error. Do not proceed to later steps.

---

## 2. List what's available

List every component under `.sync-tools-tmp/library/agents/`, `.sync-tools-tmp/library/skills/`, and `.sync-tools-tmp/library/commands/`.

- `commands/` — one component per `.md` file.
- `agents/` and `skills/` — one component per subfolder (may contain several files, e.g. `dev-team/` holds four agent files).

For each component, compare it against this project's `.claude/agents/`, `.claude/skills/`, `.claude/commands/`:

- **New** — nothing by that name exists locally yet.
- **Identical** — exists locally and matches exactly.
- **Changed** — exists locally but differs (the library version moved on, or this project's copy was customized — either is possible, don't assume which).

---

## 3. Show the user and ask

Present a short table: component, type, status. Leave "identical" ones out of the question entirely — nothing to decide there.

For each **new** component, ask whether to install it.

For each **changed** component, ask this way — never assume the library version should win:

"`[component]` differs from your local copy — pull the library version and overwrite yours, keep your local version as-is, or see the diff first?"

---

## 4. Apply

For everything approved, copy it from `.sync-tools-tmp/library/...` into this project's matching `.claude/...` folder, preserving structure (e.g. `library/agents/dev-team/*.md` → `.claude/agents/*.md`).

---

## 5. Clean up

Delete `.sync-tools-tmp` — always, whether earlier steps succeeded, failed, or were partially skipped. Nothing from the clone should remain in the project.

---

## 6. Report

Tell the user, in a few short lines: what was added, what was updated, what was left alone, and confirm nothing else in the project was touched.
