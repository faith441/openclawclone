---
name: git-helper
description: Help with Git commands and workflows. Use when user needs Git assistance - commits, branches, merges, rebases, or resolving conflicts.
---

# Git Helper

## Overview

Assists with Git commands, workflows, and troubleshooting common Git issues.

## When to Use

- User needs help with Git commands
- User is stuck with a merge conflict
- User wants to undo something in Git
- User needs branching strategy advice

## Common Workflows

### Start New Feature
```bash
git checkout main
git pull origin main
git checkout -b feature/my-feature
# ... make changes ...
git add .
git commit -m "Add my feature"
git push -u origin feature/my-feature
```

### Update Feature Branch
```bash
git checkout main
git pull origin main
git checkout feature/my-feature
git rebase main
# or: git merge main
```

### Squash Commits Before PR
```bash
git rebase -i HEAD~3  # Squash last 3 commits
# Change 'pick' to 'squash' for commits to combine
```

## Undo Operations

| What to Undo | Command |
|--------------|---------|
| Unstage file | `git reset HEAD <file>` |
| Discard local changes | `git checkout -- <file>` |
| Undo last commit (keep changes) | `git reset --soft HEAD~1` |
| Undo last commit (discard changes) | `git reset --hard HEAD~1` |
| Revert pushed commit | `git revert <commit>` |
| Undo merge | `git reset --hard ORIG_HEAD` |

## Merge Conflicts

### Resolution Steps
```bash
# 1. See conflicting files
git status

# 2. Open file and look for conflict markers
<<<<<<< HEAD
your changes
=======
their changes
>>>>>>> branch-name

# 3. Edit to keep desired code, remove markers

# 4. Mark as resolved
git add <file>

# 5. Complete merge
git commit
```

## Useful Commands

### View History
```bash
git log --oneline -10           # Last 10 commits
git log --graph --oneline       # Visual branch history
git log -p <file>               # History of a file
git blame <file>                # Who changed each line
```

### Stash Changes
```bash
git stash                       # Save changes
git stash list                  # List stashes
git stash pop                   # Restore and remove
git stash apply                 # Restore and keep
```

### Compare
```bash
git diff                        # Unstaged changes
git diff --staged               # Staged changes
git diff main..feature          # Between branches
```

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/description` | `feature/user-auth` |
| Bugfix | `fix/description` | `fix/login-error` |
| Hotfix | `hotfix/description` | `hotfix/security-patch` |
| Release | `release/version` | `release/1.2.0` |
