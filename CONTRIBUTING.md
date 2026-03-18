# 🤝 Contributing to CodeMarix

Welcome! This guide is designed for developers new to collaborative development. It explains everything step-by-step.

---

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Understanding the Basics](#understanding-the-basics)
3. [Development Workflow](#development-workflow)
4. [Creating Commits](#creating-commits)
5. [Pull Requests](#pull-requests)
6. [Code Review](#code-review)
7. [Merging](#merging)
8. [Handling Conflicts](#handling-conflicts)
9. [Common Mistakes](#common-mistakes)
10. [Communication](#communication)

---

## Initial Setup

### For the Friend (New Contributor)

#### Step 1: Clone the Repository
```bash
git clone https://github.com/leighkun147/CodeMarix.git
cd CodeMarix
```

#### Step 2: Install Dependencies
```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

#### Step 3: Verify Setup
```bash
# Check git is working
git status

# Should show: On branch main
#             Your branch is up to date with 'origin/main'.
```

---

## Understanding the Basics

### What is Git?
Git is a **version control system** that tracks changes to code. Think of it like:
- **Google Docs track changes**, but for code
- Everyone can work simultaneously
- You can see who changed what, and when
- You can "undo" changes if needed

### Key Concepts

**Repository (Repo):** The entire project folder on GitHub  
**Branch:** A separate "copy" of the code where you make changes  
**Commit:** A snapshot of your changes with a message  
**Pull Request (PR):** A request to merge your changes into the main code  
**Merge:** Combining changes from one branch into another  

### The Main Branch
- `main` is the **official, production-ready code**
- **NEVER work directly on `main`**
- Always create a feature branch for your work

---

## Development Workflow

### Step-by-Step Process

#### 1. **Update Your Local Code**
Before starting ANY work, always pull the latest changes:

```bash
git checkout main
git pull origin main
```

**Why?** Your friend might have pushed changes. You need to stay in sync.

#### 2. **Create a Feature Branch**
Create a branch for your specific task:

```bash
git checkout -b feature/add-user-authentication
```

**Branch naming convention:**
- `feature/description-of-feature` - for new features
- `bugfix/description-of-bug` - for bug fixes
- `docs/description` - for documentation updates
- `refactor/description` - for code refactoring

**Examples:**
```bash
git checkout -b feature/judge-matrix-optimization
git checkout -b bugfix/fix-spelling-in-readme
git checkout -b docs/add-setup-guide
```

#### 3. **Verify You're on the Right Branch**
```bash
git branch

# Output:
#   main
# * feature/add-user-authentication  ← asterisk means you're here
```

#### 4. **Make Your Changes**
Edit files in your code editor. Make changes to:
- `app.py`
- `src/requester.py`
- etc.

#### 5. **Check What Changed**
```bash
git status

# Shows:
# modified:   src/judge_matrix.py
# modified:   app.py
# (files you changed will be listed)
```

---

## Creating Commits

### What is a Commit?
A commit is a **snapshot of your changes** with a message explaining what you did.

Think of it like saving a checkpoint in a video game.

### How to Commit

#### Step 1: Stage Your Changes
Before committing, you must "stage" files:

```bash
# Stage a specific file
git add src/judge_matrix.py

# Stage all changes
git add .
```

**What's the difference?**
- `git add filename` - adds ONE file
- `git add .` - adds ALL changed files

**Check what's staged:**
```bash
git status

# Output:
# Changes to be committed:
#   modified:   src/judge_matrix.py
#   modified:   app.py
```

#### Step 2: Commit with a Message
```bash
git commit -m "Optimize judge matrix algorithm for faster comparisons"
```

**Commit message rules:**
- ✅ **Good:** `"Add authentication to user endpoints"`
- ✅ **Good:** `"Fix typo in README"`
- ❌ **Bad:** `"stuff"`, `"update"`, `"asdf"`
- Use **present tense:** "Add" not "Added"
- Be **specific** about what changed

**Example commits:**
```bash
git commit -m "Add support for 15 programming languages"
git commit -m "Refactor stats_engine for better performance"
git commit -m "Fix bug in model comparison logic"
git commit -m "Update documentation with setup instructions"
```

#### Step 3: Verify Commit
```bash
git log --oneline

# Output:
# a1b2c3d (HEAD -> feature/optimize-judge) Optimize judge matrix algorithm
# e4f5g6h (origin/main, main) Initial commit: CodexMatrix AI benchmarking engine
```

---

## Pushing Your Changes

### Upload to GitHub
Once you've made commits, push them to GitHub:

```bash
git push -u origin feature/optimize-judge
```

**What does this do?**
- Uploads your branch to GitHub
- `-u` sets it to track the remote branch
- Next time, you can just use `git push`

**Verify on GitHub:**
Visit https://github.com/leighkun147/CodeMarix and you should see your branch listed.

---

## Pull Requests

### What is a Pull Request (PR)?
A PR is a **formal request** to merge your changes into the main code. It allows for:
- Code review
- Discussion about changes
- Quality control

### Creating a Pull Request

#### Step 1: Push Your Branch
```bash
git push -u origin feature/optimize-judge
```

#### Step 2: Go to GitHub
1. Visit https://github.com/leighkun147/CodeMarix
2. You should see a notification: **"Your recently pushed branches"**
3. Click **"Compare & pull request"**

#### Step 3: Fill Out the PR Template
```
Title: Add optimization to judge matrix algorithm

Description:
- Improved comparison algorithm efficiency
- Reduced time complexity from O(n²) to O(n log n)
- Added unit tests for verification
- No breaking changes

Related Issue: (if any, e.g., #5)
```

**PR Title rules:**
- ✅ **Good:** `"Add caching to improve API response times"`
- ✅ **Good:** `"Fix bug in language detection"`
- ❌ **Bad:** `"update"`, `"fixes stuff"`

#### Step 4: Click "Create Pull Request"
Once created, notify your collaborator (or wait for them to review).

---

## Code Review

### For the Reviewer (You or Your Friend)

#### Step 1: View the PR
Go to **Pull Requests** tab on GitHub and click on the PR.

#### Step 2: Review the Changes
1. Click **"Files changed"** tab
2. Read through the code
3. Look for:
   - Does it follow project style?
   - Are there obvious bugs?
   - Is it well-documented?
   - Does it break anything?

#### Step 3: Leave Comments
**To comment on a specific line:**
1. Hover over the line number
2. Click the **+** icon
3. Type your comment
4. Click "Comment" or "Start a review"

**Example comments:**
```
"Can you add a docstring explaining this function?"

"This should use the existing helper function in utils.py"

"Great optimization! Did you test this with large datasets?"
```

#### Step 4: Approve or Request Changes
At the bottom:
- ✅ **Approve** - Looks good to merge!
- 💬 **Comment** - Just leaving feedback
- ❌ **Request Changes** - Changes needed before merging

---

### For the Author (Person Who Made the PR)

#### Step 1: Respond to Comments
Reply to reviewer's feedback:
- If you agree: implement the change
- If you disagree: explain why respectfully

#### Step 2: Make Requested Changes
```bash
# You're still on your feature branch
git add .
git commit -m "Address code review feedback"
git push
```

**Important:** The PR automatically updates! No need to create a new one.

#### Step 3: Resolve Comments
Once you've made changes:
1. Reply to the comment: "Fixed! See commit abc123"
2. Click "Resolve conversation"

---

## Merging

### What Happens After Approval?

#### Step 1: PR is Approved
Once the reviewer(s) approve, you'll see: **"This branch has no conflicts with the base branch"**

#### Step 2: Merge the PR
Click the green **"Merge pull request"** button on GitHub.

#### Step 3: Confirm Merge
Click **"Confirm merge"**

#### Step 4: Delete the Feature Branch (Optional but Recommended)
After merging, GitHub offers: **"Delete branch"** - click it to clean up.

#### Step 5: Pull Latest Changes Locally
```bash
git checkout main
git pull origin main
```

Now your local `main` has the merged changes!

---

## Handling Conflicts

### What is a Merge Conflict?
A conflict happens when:
- You and your friend both edited the **same line** of code
- Git doesn't know which version to keep

### Example Conflict
```
<<<<<<< HEAD (your changes)
def calculate_score(models):
    return sum(models) / len(models)
=======
def calculate_score(models):
    return statistics.mean(models)
>>>>>>> feature/refactor-stats
```

### How to Resolve Conflicts

#### Step 1: Identify Conflicts
```bash
git status

# Output:
# both modified:   src/stats_engine.py
```

#### Step 2: Open the File
Look for sections marked with:
```
<<<<<<< HEAD
...your code...
=======
...their code...
>>>>>>> branch-name
```

#### Step 3: Decide Which Version to Keep
- Keep your version? Delete their section.
- Keep their version? Delete your section.
- Combine both? Edit to merge the logic.

**Example resolution:**
```python
# Before (conflicted):
# <<<<<<< HEAD
# return sum(models) / len(models)
# =======
# return statistics.mean(models)
# >>>>>>> feature/refactor-stats

# After (resolved - use the better option):
return statistics.mean(models)  # More robust
```

#### Step 4: Remove Conflict Markers
Delete the `<<<<<<<`, `=======`, and `>>>>>>>` lines.

#### Step 5: Commit the Resolution
```bash
git add src/stats_engine.py
git commit -m "Resolve merge conflict in stats_engine.py"
git push
```

---

## Common Mistakes

### ❌ Mistake 1: Working on `main` Branch
```bash
# WRONG:
git checkout main
git add .
git commit -m "Add new feature"  ← NEVER DO THIS

# RIGHT:
git checkout -b feature/new-feature
git add .
git commit -m "Add new feature"
```

**Fix:** Create a new branch, cherry-pick your commits, and start over.

---

### ❌ Mistake 2: Forgetting to Pull Before Starting
```bash
# WRONG:
git checkout -b feature/new  ← starts from old main

# RIGHT:
git checkout main
git pull origin main  ← get latest
git checkout -b feature/new  ← now starts from latest
```

---

### ❌ Mistake 3: Large, Unclear Commits
```bash
# WRONG:
git add .
git commit -m "stuff"  ← too vague!

# RIGHT:
git add src/judge_matrix.py
git commit -m "Optimize judge matrix comparison algorithm"
git add README.md
git commit -m "Update documentation with new features"
```

**Principle:** Each commit should do ONE logical thing.

---

### ❌ Mistake 4: Force Pushing (`git push -f`)
**NEVER** use `git push -f` unless you're absolutely sure!

```bash
# DANGEROUS - AVOID:
git push -f origin main

# This can overwrite your friend's work!
```

---

### ❌ Mistake 5: Not Communicating
```
# BAD: You work for 5 days in silence, then create a huge PR
# GOOD: Tell your friend what you're working on
# BETTER: Create a PR early and discuss as you go
```

---

## Communication

### How to Communicate with Your Teammate

#### 1. **Slack / Discord / Email**
Before starting work:
- 💬 "Hey, I'm going to work on optimizing the judge matrix"
- 💬 "I see you're working on authentication. Should I wait?"

#### 2. **GitHub Issues** (Optional but Recommended)
Create issues for tasks:
1. Go to **Issues** tab
2. Click **"New issue"**
3. Title: `"Optimize judge matrix performance"`
4. Description: Explain the task
5. Assign to yourself

Then reference it in your PR: `"Closes #5"`

#### 3. **PR Discussions**
Use PR comments for technical discussions:
```
Reviewer: "Why did you choose this algorithm?"
Author: "It has O(n log n) complexity, which is better than O(n²)"
```

#### 4. **Daily Standup** (Optional)
Quick sync every morning:
- ✅ "What did I do yesterday?"
- 🔄 "What am I doing today?"
- 🚧 "Any blockers?"

---

## Quick Reference Cheatsheet

```bash
# Start work
git checkout main
git pull origin main
git checkout -b feature/description

# During work
git status              # See what changed
git add .              # Stage all changes
git commit -m "message"  # Create a commit
git push -u origin feature/description  # Push to GitHub

# After review
git pull origin main    # Get latest main
# (Resolve conflicts if any)
# Then merge on GitHub

# After merging
git checkout main
git pull origin main
# Work on next feature
```

---

## Important Reminders

✅ **DO:**
- Always pull before starting work
- Create descriptive commits
- Communicate with your team
- Request reviews before merging
- Test your code locally first

❌ **DON'T:**
- Push directly to `main`
- Force push (`git push -f`)
- Make huge commits mixing many changes
- Ignore code review comments
- Leave branches hanging for weeks

---

## Need Help?

### Useful Resources
- [GitHub Docs](https://docs.github.com)
- [Git Cheatsheet](https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet)
- Ask your collaborator!

### If You Mess Up
Don't panic! Most mistakes can be fixed. Common scenarios:
- Committed on wrong branch? → Cherry-pick the commit
- Made a bad commit message? → `git commit --amend`
- Deleted a branch by accident? → `git reflog` can recover it

---

## Workflow Summary

```
1. git checkout main && git pull
       ↓
2. git checkout -b feature/your-feature
       ↓
3. Make changes & test locally
       ↓
4. git add . && git commit -m "message"
       ↓
5. git push -u origin feature/your-feature
       ↓
6. Create Pull Request on GitHub
       ↓
7. Your friend reviews & approves
       ↓
8. Merge on GitHub
       ↓
9. git checkout main && git pull
       ↓
10. Repeat (go back to step 2)
```

---

**Happy coding! 🚀**

