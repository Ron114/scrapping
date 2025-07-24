import os
import subprocess
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

# Load Git identity from .env
load_dotenv()
GIT_USER_NAME = os.getenv("GIT_USER_NAME")
GIT_USER_EMAIL = os.getenv("GIT_USER_EMAIL")

# Run a shell command
def run_command(command, env=None):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print("❌ Error:", result.stderr.strip())
    return result.stdout.strip()

# Build environment with git identity and commit datetime
def build_git_env(commit_datetime):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_datetime
    env["GIT_COMMITTER_DATE"] = commit_datetime
    env["GIT_AUTHOR_NAME"] = GIT_USER_NAME
    env["GIT_COMMITTER_NAME"] = GIT_USER_NAME
    env["GIT_AUTHOR_EMAIL"] = GIT_USER_EMAIL
    env["GIT_COMMITTER_EMAIL"] = GIT_USER_EMAIL
    return env

# Create a single commit at a specific datetime
def make_commit(commit_datetime):
    with open("activity.txt", "a") as f:
        f.write(f"Commit on {commit_datetime}\n")

    run_command("git add activity.txt")
    env = build_git_env(commit_datetime)
    run_command(f'git commit -m "Backdated commit on {commit_datetime}"', env=env)

# Generate multiple commits across a date range
def generate_commits(start_date, end_date, special_days=None):
    if special_days is None:
        special_days = set()

    current = start_date
    while current <= end_date:
        month_day = current.strftime("%m-%d")
        is_special = month_day in special_days
        num_commits = random.randint(15, 30) if is_special else random.randint(1, 30)

        for i in range(num_commits):
            hour = 8 + (i % 10)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_time = current.replace(hour=hour, minute=minute, second=second)
            make_commit(commit_time.isoformat())

        print(f"{'⭐️' if is_special else '✅'} {num_commits} commits on {current.date()}")
        current += timedelta(days=1)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    # Start from your GitHub account creation date
    start_date = datetime(2016, 11, 29)
    end_date = datetime.today()

    # Picked a few special days (can adjust freely)
    special_dates = {
        "01-01", "01-02", "01-03", "01-04", "01-05", "01-06", "01-07", "01-09", "01-13", "01-15", "01-16", "01-21", "01-23",
        "02-01", "02-03", "02-05", "02-08", "02-10", "02-14", "02-17", "02-20", "02-25", "02-28",
        "03-01", "03-03", "03-05", "03-08", "03-10", "03-12", "03-15", "03-17", "03-20", "03-25", "03-30",
        "04-01", "04-03", "04-05", "04-07", "04-10", "04-14", "04-18", "04-20", "04-22", "04-25", "04-30",
        "05-01", "05-03", "05-04", "05-05", "05-07", "05-09", "05-14", "05-20", "05-25", "05-28", "05-30",
        "06-01", "06-03", "06-05", "06-07", "06-10", "06-12", "06-15", "06-20", "06-22", "06-25", "06-30",
        "07-01", "07-03", "07-04", "07-07", "07-10", "07-12", "07-15", "07-21", "07-25", "07-28", "07-30",
        "08-01", "08-04", "08-08", "08-10", "08-12", "08-15", "08-17", "08-20", "08-24", "08-28", "08-30",
        "09-01", "09-03", "09-05", "09-08", "09-10", "09-14", "09-18", "09-20", "09-25", "09-27", "09-30",
        "10-01", "10-05", "10-08", "10-10", "10-13", "10-17", "10-20", "10-23", "10-27", "10-29", "10-31",
        "11-01", "11-03", "11-07", "11-10", "11-13", "11-17", "11-20", "11-23", "11-25", "11-28", "11-30",
        "12-01", "12-03", "12-05", "12-10", "12-14", "12-18", "12-22", "12-24", "12-25", "12-28", "12-31"
    }


    generate_commits(
        start_date=start_date,
        end_date=end_date,
        special_days=special_dates
    )

    # Push to GitHub
    run_command("git push origin main")
