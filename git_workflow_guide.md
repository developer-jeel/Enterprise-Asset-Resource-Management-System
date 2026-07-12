# Git & GitHub Collaborative Workflow Guide (Django)

This guide outlines a clean, conflict-free Git workflow for a 2-person Django project. It is designed to keep **Bhavya** and **Jeel** synchronized without getting stuck in merge conflicts, especially during a fast-paced hackathon.

---

## 1. Why Did Conflicts and Crashes Happen?

Before fixing the workflow, it is important to understand the three main issues that were causing your project to break:

1. **Missing `.gitignore` (Tracking Cache & Database):**
   - Git was tracking python cache files (`__pycache__/`, `*.pyc`) and the SQLite database (`db.sqlite3`). 
   - Since these files change every time you run your server or make database queries, Git flags them as conflicts constantly.
   - *Status: Fixed! We added a `.gitignore` and removed these files from Git tracking.*

2. **Django Circular Imports:**
   - Both developers were using wildcard imports like `from employee.models import *` inside `admin/models.py`, while `employee/models.py` imported from `admin.models`.
   - This creates a circular dependency loop, causing Python to crash on startup.
   - *Status: Fixed! We resolved this by removing wildcard imports and using Django's lazy string relationship reference.*

3. **Merging Branches Directly:**
   - Merging `Jeel` directly into `bhavya-chaudhary` (or vice-versa) bypasses the central integration branch (`main`), leading to messy histories.

---

## 2. The Recommended Branching Strategy

For a 2-person team, the **Short-Lived Developer Branch + Shared `main` Branch** workflow is the best balance of safety and speed.

```mermaid
graph TD
    subgraph GitHub Remote (origin)
        main_remote[main branch - Shared Integration]
        bhavya_remote[bhavya-chaudhary branch]
        jeel_remote[Jeel branch]
    end

    subgraph Bhavya Local
        bhavya_local[bhavya-chaudhary local]
    end

    subgraph Jeel Local
        jeel_local[Jeel local]
    end

    bhavya_local -->|1. Push changes| bhavya_remote
    bhavya_remote -->|2. Pull Request| main_remote
    jeel_local -->|1. Push changes| jeel_remote
    jeel_remote -->|2. Pull Request| main_remote

    main_remote -->|3. Sync main back| bhavya_local
    main_remote -->|3. Sync main back| jeel_local
```

### Key Concepts:
* **`main` is the Source of Truth:** The `main` branch always holds the latest, fully working, and integrated code. Neither developer commits directly to `main`.
* **Developer Branches:** 
  * Bhavya works on the `bhavya-chaudhary` branch.
  * Jeel works on the `Jeel` branch.
* **Synchronization Point:** You both push your work to your own branches, open a Pull Request (PR) to `main`, merge it, and then pull the updated `main` branch back into your local workspace.

---

## 3. Git Commands Cheat Sheet

| Command | What it does | When to use it |
| :--- | :--- | :--- |
| `git fetch origin` | Downloads information about changes from the remote repo (does not change your files). | To see if your teammate has pushed anything new. |
| `git pull origin main` | Downloads changes from remote `main` and merges them into your current local branch. | At the start of the day or after your teammate's PR is merged. |
| `git push origin <branch>` | Uploads your local commits to GitHub. | When you finish a task and want to open a PR or share your work. |
| `git checkout <branch>` | Switches your active branch. | When switching between your dev branch and `main`. |
| `git status` | Shows which files are modified, staged, or untracked. | Frequently! To know what state your repository is in. |
| `git add <files>` | Stages files for commit. | When you are ready to save a group of changes. |
| `git commit -m "msg"` | Saves a snapshot of staged changes. | When you complete a logical unit of work (e.g. "Add login form"). |

---

## 4. Daily Step-by-Step Workflow

Follow these steps daily to keep both workspaces perfectly synchronized.

### Step 1: Starting Your Work (Syncing up)
Before writing any code, pull the latest changes from the shared `main` branch:
1. Open your terminal in VS Code.
2. Checkout your local branch:
   ```bash
   git checkout bhavya-chaudhary   # (Jeel runs: git checkout Jeel)
   ```
3. Fetch all remote changes and pull the latest `main`:
   ```bash
   git fetch origin
   git pull origin main
   ```
   *Note: If there are changes on `main`, they will merge smoothly into your local branch.*

### Step 2: Write Code and Commit Locally
Work on your assigned feature. Commit frequently so your changes are small and easy to merge.
1. Stage your modified files:
   ```bash
   git add enterprise/dept_head/models.py
   ```
2. Commit with a clear message:
   ```bash
   git commit -m "Implement DepartmentHead model user relation"
   ```

### Step 3: Pushing and Syncing with GitHub
When you finish a task and want to share it with your teammate:
1. Push your branch to GitHub:
   ```bash
   git push origin bhavya-chaudhary   # (Jeel runs: git push origin Jeel)
   ```
2. Go to your GitHub repository URL.
3. Open a **Pull Request (PR)** from `bhavya-chaudhary` into `main`.
4. Review the changes and click **Merge Pull Request**. (If conflicts occur on GitHub, see Section 6).

### Step 4: The Other Developer Pulls the New Code
Once Bhavya's PR is merged into `main`, **Jeel** needs to get those changes:
1. Jeel switches to his local branch (if not already there):
   ```bash
   git checkout Jeel
   ```
2. Jeel pulls the latest `main`:
   ```bash
   git pull origin main
   ```
   *Now Jeel has Bhavya's changes instantly in his VS Code!*

---

## 5. How to Prevent Merge Conflicts

Conflicts happen when both of you edit the **same lines of the same file** at the same time. Prevent this using these best practices:

### A. Divide and Conquer (Assign Specific Files/Apps)
* Django is modular. Divide your work by app!
  * **Bhavya** works on `dept_head` and `employee` folders.
  * **Jeel** works on `admin` and `manager` folders.
* Try not to edit files in the other person's folders unless you communicate first.

### B. Django Circular Import Prevention
Instead of importing models from other apps directly (which causes circular imports and merge conflicts):
* **Do NOT use star imports:** Avoid `from app.models import *` between apps.
* **Use Lazy/String References for Relations:**
  If a model in `dept_head` needs a foreign key to the `user` model in `admin`, define it as a string instead of importing:
  ```python
  # enterprise/dept_head/models.py
  # No need to import admin.models!
  class DepartmentHead(models.Model):
      user = models.OneToOneField('custom_admin.user', on_delete=models.CASCADE)
  ```
  *(Django will automatically look up the `user` model in the `custom_admin` app at runtime, completely avoiding import loops!)*

### C. Commit and Pull Frequently
* Do not wait until the end of the hackathon to push your code.
* Push small changes (e.g. one view, one model, one template) and merge them.
* Pull from `main` every time a PR is merged.

---

## 6. How to Resolve Conflicts (If They Occur)

If both of you edit the same file, Git will show a conflict during a `pull` or `merge`. Here is how to fix it:

### Step 1: Identify the Conflicts
Git will block the merge and modify the conflicted files. VS Code will highlight them in red. Open the conflicted file and look for the conflict markers:

```python
<<<<<<< HEAD
# This is YOUR local change (Bhavya's code)
user = models.OneToOneField('custom_admin.user', on_delete=models.CASCADE)
=======
# This is the INCOMING change (Jeel's code)
user = models.ForeignKey('admin.user', on_delete=models.SET_NULL, null=True)
>>>>>>> origin/main
```

### Step 2: Choose the Correct Code in VS Code
VS Code provides interactive buttons above the markers:
* **Accept Current Change:** Keeps your code and deletes your teammate's.
* **Accept Incoming Change:** Keeps your teammate's code and deletes yours.
* **Accept Both Changes:** Keeps both blocks of code.
* **Manually Edit:** Simply delete the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) and edit the code yourself to merge them cleanly.

### Step 3: Complete the Merge
Once you have cleaned up the file and saved it:
1. Run `git status` to see the conflicted files.
2. Stage the resolved files:
   ```bash
   git add <path-to-resolved-file>
   ```
3. Commit to finalize the merge:
   ```bash
   git commit -m "Merge main and resolve conflicts"
   ```
4. Push the resolved code back:
   ```bash
   git push origin <your-branch-name>
   ```

---

> [!TIP]
> **Communication is key:** If you see a merge conflict, do not guess! Ask your teammate: *"Hey, I see we both edited settings.py. Which packages or settings did you add so we can keep both?"* A 1-minute quick call resolves conflicts faster than any Git command.
