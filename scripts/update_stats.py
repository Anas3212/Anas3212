import urllib.request
import json
import re
import os

USERNAME = "Anas3212"

def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    user_data = fetch_json(f"https://api.github.com/users/{USERNAME}")
    repos_data = fetch_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=100")

    if not user_data:
        print("Failed to fetch user data")
        return

    public_repos = user_data.get("public_repos", 12)
    followers = user_data.get("followers", 15)

    total_stars = 0
    languages = {}

    if repos_data and isinstance(repos_data, list):
        for repo in repos_data:
            if repo.get("fork"):
                continue
            total_stars += repo.get("stargazers_count", 0)
            lang = repo.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1

    print(f"User: {USERNAME}")
    print(f"Public Repos: {public_repos}")
    print(f"Followers: {followers}")
    print(f"Total Stars: {total_stars}")
    print(f"Languages: {languages}")

    # Read current github_stats.svg
    svg_path = "github_stats.svg"
    if not os.path.exists(svg_path):
        print("github_stats.svg not found")
        return

    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update metric values if present
    content = re.sub(r'fill="#F8FAFC" text-anchor="end">\d+\+?</text>\s*<!-- Metric 1: Repositories -->', f'fill="#F8FAFC" text-anchor="end">{public_repos}</text>', content)
    
    # Simple regex replacement for safety
    content = content.replace('>12+</text>', f'>{public_repos}</text>')
    content = content.replace('>15+</text>', f'>{followers}</text>')
    content = content.replace('>25+</text>', f'>{total_stars}</text>')

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("github_stats.svg updated successfully!")

if __name__ == "__main__":
    main()
