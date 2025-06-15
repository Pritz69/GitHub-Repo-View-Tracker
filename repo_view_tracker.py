import os
import json
from github import Github, GithubException

# --- Configuration ---

# List of your repositories in 'username/repository_name' format
REPOSITORIES_TO_TRACK = [
    "Pritz69/LeetCode-Solutions",
    "Pritz69/GFG_POTD",
    "Pritz69/GitHub-Repo-View-Tracker",
    "Pritz69/UNFOLLOW-GITHUB-USERS-WHO-DONT-FOLLOW-US",
    "Pritz69/EmployeeManagementSystem-FULL-STACK-CRUD",
    "Pritz69/Newton-School-POTD",
    "Pritz69/5011251",
    "Pritz69/Portfolio_Website",
    "Pritz69/LeetCode-JS-30DaysChallenge",
    "Pritz69/Calculator",
    "Pritz69/Music_Player",
    "Pritz69/MemoryGame",
    "Pritz69/Terminal_Portfolio",
    "Pritz69/MovieRecommenderSite",
    "Pritz69/MAFSMBMDDPWI-FYP-2025",
    "Pritz69/Wine_Quality_Prediction_ML"
]
DATA_FILE = "repo_views.json"

# --- Utility Functions ---
def load_view_counts():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: '{DATA_FILE}' contains invalid JSON. Starting with empty counts.")
            return {}
    return {}

def save_view_counts(counts):
    with open(DATA_FILE, 'w') as f:
        json.dump(counts, f, indent=4)

# --- Main Functionality ---
def get_repository_views(repo_full_name, g):
    try:
        repo = g.get_repo(repo_full_name)
        traffic = repo.get_views_traffic()
        if traffic and hasattr(traffic, 'views'):
            return sum(view.count for view in traffic.views)
        else:
            return None
    except Exception as e:
        print(f"Error for {repo_full_name}: {e}")
        return None

def main():
    print("Connecting to GitHub...")
    g = Github(os.getenv("GITHUB_TOKEN"))  # Use GitHub Actions token
    print(f"Successfully authenticated as: {g.get_user().login}")

    view_counts = load_view_counts()
    updated_any_repo = False

    for repo_full_name in REPOSITORIES_TO_TRACK:
        print(f"Processing: {repo_full_name}")
        current_views = get_repository_views(repo_full_name, g)

        if current_views is not None:
            if repo_full_name not in view_counts:
                view_counts[repo_full_name] = {
                    "total_views_last_14_days": 0,
                    "last_recorded_total": 0,
                    "views_diff_last_run": 0,
                    "cumulative_views": 0
                }

            last_total = view_counts[repo_full_name].get("total_views_last_14_days", 0)
            diff = current_views - last_total

            view_counts[repo_full_name]["total_views_last_14_days"] = current_views
            view_counts[repo_full_name]["last_recorded_total"] = last_total
            view_counts[repo_full_name]["views_diff_last_run"] = diff
            view_counts[repo_full_name].setdefault("cumulative_views", 0) #if want to keep track of count from today
            # view_counts[repo_full_name].setdefault("cumulative_views", current_views) #if want to keep track of count from last 14 days views
            view_counts[repo_full_name]["cumulative_views"] += max(0, diff)

            print(f"  Updated {repo_full_name}: {current_views} views (last 14 days). Diff: {diff}")
            updated_any_repo = True

    if updated_any_repo or not os.path.exists(DATA_FILE):
        print(f"\nSaving updated view counts to '{DATA_FILE}'...")
        save_view_counts(view_counts)

    print("\n--- Current Repository View Statistics (Last 14 Days) ---")
    for repo, data in view_counts.items():
        print(f"{repo}: {data.get('total_views_last_14_days')} views, Diff: {data.get('views_diff_last_run')}, Cumulative: {data.get('cumulative_views')}")

if __name__ == "__main__":
    main()

