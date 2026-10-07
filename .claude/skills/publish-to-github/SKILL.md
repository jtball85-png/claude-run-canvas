---
name: publish-to-github
description: Create a GitHub repo for the current local project and connect/push it — the automated equivalent of GitHub Desktop's "Publish repository" button. Use after /new-project sets up a brand-new project, or any time an existing local git repo has no GitHub remote yet.
---

# Publish to GitHub

Turns a local-only git repo into one backed up on GitHub, in one step. Uses the `gh` CLI, not raw git — plain git has no concept of creating a repo on GitHub.com, that's a GitHub API action.

## 1. Check prerequisites

```bash
gh --version
```

If not found, check the default Windows install location before giving up:

```bash
"/c/Program Files/GitHub CLI/gh.exe" --version
```

If genuinely not installed: **stop**. Tell the user `gh` needs to be installed first (`winget install --id GitHub.cli`) — do not install it yourself without asking, since that's a system-level change on whatever machine this is running on.

Then check authentication:

```bash
gh auth status
```

If not logged in: **stop**. Tell the user to run `gh auth login --web` themselves (or offer to run it and relay the device code, the way it was done the first time) — don't proceed without an authenticated account.

## 2. Check the local repo is ready

```bash
git rev-parse --is-inside-work-tree
git log -1 --oneline
```

If this isn't a git repo yet, or has no commits yet: **stop**. Nothing to publish — `git init` and at least one commit need to happen first (normally already done by `/new-project`).

## 3. Check it isn't already connected

```bash
git remote -v
```

If a remote already exists: **stop**. Tell the user this project is already connected (show them the remote URL) — don't overwrite an existing connection.

## 4. Confirm name and visibility

Never create the repo silently. Ask the user:

- **Repo name** — default to the current folder name, let them override
- **Public or private** — default to private unless they say otherwise

Wait for confirmation before proceeding.

## 5. Create, connect, and push — in one step

```bash
gh repo create <name> --private --source=. --remote=origin --push
```

(Use `--public` instead of `--private` if that's what was confirmed.) This single command creates the GitHub repo, sets it as `origin`, and pushes the current branch — equivalent to Desktop's "Publish repository" button.

## 6. Report

Tell the user the repo is live, and give them the URL (`gh repo view --web` prints it, or read it from the command output above). From here, this project behaves like any other repo with a remote — `/start-of-day` and `/end-of-day` will pull/push against it normally.
