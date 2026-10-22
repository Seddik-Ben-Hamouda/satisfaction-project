# Satisfaction Project

Predicting customer satisfaction with Glovo from app-store reviews, plus a questionnaire study on what drives satisfaction with food delivery.

This file explains what the project is and gives every command you need, in order, to get it running on your computer (Windows, PowerShell).

---

## 1. What the project is

There are two parts:

1. **Review analysis.** We collected about 6,600 public Glovo reviews (Oct 2023 to Oct 2026) and study what they say. Each review has a star rating, which we turn into a yes/no label called `high_satisfaction`.
2. **Questionnaire.** The reviews have no ratings per factor (speed, price, support...), so we run our own survey to measure those. The reviews support the story and the comment analysis. The questionnaire feeds the main model.

### Key facts to know

- **Target variable:** `high_satisfaction` = 1 if the review is positive, 0 if not. About 63% of reviews are "high".
- **Ratings are U-shaped:** most reviews are 1 star or 5 stars, very few in between. So the model mostly learns "very unhappy vs happy".
- **Languages are mixed:** French, English, Arabic script, and **Arabizi** (Arabic written with Latin letters and numbers, like `5dhit` or `3lia`). About 3 to 5% of reviews are Arabizi, in both Tunisian and Moroccan dialects.
- **The reviews come from several countries**, not only Tunisia.
- **The newest quarter (2026Q4) is partial** and the first period is cut by our scraping limit, so don't read them as full quarters.

---

## 2. Project structure

```
satisfaction-project/
├── data/
│   └── clean/
│       └── glovo_reviews_clean.csv   <- cleaned reviews (main dataset)
├── check_arabizi.py                  <- estimates how many reviews contain Arabizi
├── requirements.txt                  <- list of Python libraries to install
├── .gitignore                        <- files Git must not upload (venv, caches)
└── README.md                         <- this file
```

The `venv/` folder (your Python environment) is **not** in GitHub. You create it yourself in step 2 below.

### Main columns in `glovo_reviews_clean.csv`

| Column | Meaning |
|---|---|
| `content` | the original review text |
| `text_norm` | the cleaned, lowercase version used for analysis |
| `high_satisfaction` | the target: 1 = high, 0 = not high |

(The file has more columns, such as the star score and date.)

---

## 3. Setup (do this once)

### Requirements

- **Python 3.10 or newer** (check with `python --version`)
- **Git** (check with `git --version`)
- A GitHub account, with access to the repository

### Step 1: Download the project

Open PowerShell, go to the folder where you want the project, then run:

```powershell
git clone https://github.com/Seddik-Ben-Hamouda/satisfaction-project.git
cd satisfaction-project
```

### Step 2: Create your own Python environment

A "virtual environment" is a private box of libraries for this project, so it doesn't mix with other things on your computer.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

When it works, you see `(venv)` at the start of your terminal line. You must activate it **every time you open a new terminal**.

> **If PowerShell says "running scripts is disabled":** run this once, then activate again:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

### Step 3: Install the libraries

```powershell
pip install -r requirements.txt
```

### Step 4: Check that everything works

```powershell
$env:PYTHONIOENCODING="utf-8"
python check_arabizi.py
```

You should see a share of about `0.029` and a table with two rows (`False` and `True`). If you do, you are ready.

> The `$env:PYTHONIOENCODING="utf-8"` line stops Windows from crashing when it prints Arabic characters. You need to run it once per terminal window.

---

## 4. Daily workflow with Git

Git is how we share work without overwriting each other. Follow this order **every time**.

**Before you start working: get the latest version**

```powershell
git pull origin main
```

**After you change or add something: save and share it**

```powershell
git add .
git commit -m "Short message saying what you changed"
git push
```

What each command does:

- `git pull` downloads what the others have pushed.
- `git add .` selects all your changes for the next snapshot.
- `git commit -m "..."` saves the snapshot on your computer. Write a clear message, like "Add chart of stars by quarter".
- `git push` uploads it to GitHub so the others can see it.

**Good habits**

- Always `git pull` before you start.
- Don't edit the same file as someone else at the same time. Tell each other who works on what.
- If Git says **"Please tell me who you are"**, run this once (with your own details):
  ```powershell
  git config --global user.name "Your Name"
  git config --global user.email "your@email.com"
  ```
- If a push is rejected, run `git pull origin main`, then push again.

---

## 5. Rules for working with the data

1. **Never remove digits inside words when cleaning text.** In Arabizi, digits are letters: the `5` in `5dhit` is a sound. Removing digits destroys the words. Digits-only tokens like `2024` are fine to handle separately.
2. **Don't edit the original data by hand.** Change the data with scripts, so anyone can re-run them and get the same result.
3. **Always read the sample, not only the statistics.** Print 20 random rows before trusting a number. A rule that looks fine on paper often catches the wrong things.
4. **Keep file paths relative** (like `data/clean/glovo_reviews_clean.csv`), never `C:\Users\...`, so the code runs on both our computers.
5. **Do not push `venv/`.** The `.gitignore` already blocks it.

---

## 6. Glossary

| Term | Meaning |
|---|---|
| **Repository (repo)** | the project folder tracked by Git |
| **Commit** | a saved snapshot of the project |
| **Push / Pull** | upload your commits / download others' commits |
| **Remote (`origin`)** | the copy of the repo hosted on GitHub |
| **Virtual environment (`venv`)** | a private set of Python libraries for this project |
| **Arabizi** | Arabic dialect written with Latin letters and numbers (`3lia`, `a7sen`) |
| **Target variable** | what the model tries to predict (`high_satisfaction`) |
| **Stopwords** | very common words (like "the", "et", "sans") that carry little meaning |

---

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| `python` is not recognized | Reinstall Python and tick "Add Python to PATH", or try `py` instead of `python` |
| `(venv)` doesn't show up | Re-run `.\venv\Scripts\Activate.ps1` from the project folder |
| `ModuleNotFoundError` | The venv isn't active, or run `pip install -r requirements.txt` again |
| `UnicodeEncodeError` when printing | Run `$env:PYTHONIOENCODING="utf-8"` |
| Script can't find the CSV | Make sure you run it from the project root (`cd satisfaction-project`) |
| Git push rejected | Run `git pull origin main`, then `git push` |

If something else breaks, copy the **full** error message and send it to the group.
