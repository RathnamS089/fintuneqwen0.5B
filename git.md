# Comprehensive Guide to Git Branching & Virtual Environments

When working on a project, especially one involving heavy machine learning or Python packages, managing how your code is tracked is crucial. This guide explains Git branching concepts, how to isolate your development, and how to avoid tracking heavy local files like virtual environments (`venv`).

---

## 1. What is Branching?

Think of your Git repository as a tree. The **`main`** (or `master`) branch is the trunk of the tree—it holds your stable, production-ready code. 

A **branch** is a separate timeline that splits off from the trunk. It allows you to experiment, fix bugs, or modify configurations (like a `.yaml` file) in total isolation. 

```text
                  (Your new feature or experiments)
                  O---O---O  [modified-yaml]
                 /
---O---O---O----O------------O  [main]
```

### Why Use Branches?
* **Safety:** You can rewrite or break code on your branch without affecting the stable `main` code.
* **Independence:** Independent branches can live on GitHub forever without ever being merged into `main`.
* **Clean History:** It keeps your individual feature updates grouped together.

---

## 2. Essential Git Branching Commands

Here is the exact workflow to create, track, and push a standalone branch safely.

### Step 1: Create and Switch to a New Branch
Instead of working on `main`, split off into a custom workspace.

```bash
# The modern way (Git 2.23+)
git switch -c modified-yaml

# The traditional way (works on all Git versions)
git checkout -b modified-yaml
```
*The `-c` or `-b` flag stands for "create". This command creates the branch locally and immediately moves you into it.*

### Step 2: Check Your Current Status
Always check what files Git is seeing before you save anything.
```bash
git status
```

### Step 3: Stage Your Specific Files
Only stage the exact source or configuration files you modified. Avoid staging temporary folders or massive package directories.
```bash
git add training/soup.yaml
```

### Step 4: Commit Your Changes
Save a snapshot of your staged files to your branch's local timeline.
```bash
git commit -m "chore: update training configurations in soup.yaml"
```

### Step 5: Push as a Standalone Remote Branch
Upload your local branch to GitHub so it exists safely on the cloud, completely detached from `main`.
```bash
git push -u origin modified-yaml
```
* `-u` (upstream) links your local branch to GitHub, so in the future, you only need to type `git push`.
* As long as you do not open or merge a **Pull Request** on GitHub, this branch will remain permanently isolated from `main`.

---

## 3. Managing Local Artifacts & Virtual Environments

When you initialize a Python virtual environment (like `venv` or `venv312`) inside your project directory, it downloads thousands of third-party libraries (e.g., PyTorch, Hugging Face `trl`, `numpy`).

### The Danger: Exceeding GitHub's Limits
GitHub enforces a strict **100 MB file size limit**. Heavy compiled binaries inside machine learning packages (such as PyTorch's `libtorch_cpu.dylib`, which can exceed 360 MB) will cause GitHub to reject your entire push with a `pre-receive hook declined (GH001)` error.

### The Solution: The `.gitignore` File
A `.gitignore` file is a plain text file placed at the root of your project. It tells Git exactly which files or folders to completely blind itself to.

If you don't have one, create it and specify your environment directory:

```bash
# Create a .gitignore file and ignore the venv312 folder
echo "venv312/" > .gitignore
```

### Cleaning Up If Git Already Tracked Large Files
If you accidentally staged or committed your virtual environment, Git remembers it in your history even if you edit your `.gitignore` later. You must explicitly scrub it from Git's memory:

```bash
# 1. Remove the folder from Git's tracking area (keeps the actual files safe on your Mac)
git rm -r --cached venv312/

# 2. Reset your branch timeline back to the remote baseline to clear bad history
git reset origin/main

# 3. Re-verify that only your code and .gitignore are visible
git status

# 4. Save your clean environment-free changes
git add .gitignore training/soup.yaml
git commit -m "chore: clear heavy dependencies and add gitignore"

# 5. Force-push to overwrite the rejected remote attempt with your clean history
git push origin modified-yaml --force
```

---

## 4. Summary Cheat Sheet

| Command | What it does |
| :--- | :--- |
| `git branch` | Lists all your local branches. |
| `git switch -c <name>` | Creates a new branch and switches to it. |
| `git status` | Shows modified, staged, and untracked files. |
| `git rm -r --cached <dir>/` | Stops tracking a folder without deleting local files. |
| `git reset origin/main` | Points your local history back to main while preserving your code changes. |
| `git push -u origin <name>` | Pushes a brand new standalone branch up to GitHub. |
| `git push origin <name> --force` | Overwrites remote branch history (useful after scrubbing large files). |
