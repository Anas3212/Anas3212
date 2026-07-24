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

def fetch_views():
    url = f"https://komarev.com/ghpvc/?username={USERNAME}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            svg_text = resp.read().decode("utf-8")
            # Extract number from komarev SVG output
            matches = re.findall(r'<text[^>]*>(\d+)</text>', svg_text)
            if matches:
                return matches[-1]
    except Exception as e:
        print(f"Error fetching views: {e}")
    return "19"

def update_github_stats(public_repos, followers, total_stars):
    svg_path = "github_stats.svg"
    if not os.path.exists(svg_path):
        return

    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace('>12+</text>', f'>{public_repos}</text>')
    content = content.replace('>15+</text>', f'>{followers}</text>')
    content = content.replace('>25+</text>', f'>{total_stars}</text>')

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(content)

def update_quote_views(views_count):
    svg_path = "quote_views.svg"
    if not os.path.exists(svg_path):
        return

    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace hardcoded 25 with real views count
    # Gauge count
    content = re.sub(
        r'<text x="0" y="8" [^>]*>\d+</text>\s*<text [^>]*>PROFILE VIEWS</text>',
        f'<text x="0" y="8" font-family="\'JetBrains Mono\', monospace" font-size="42" font-weight="800" fill="#F8FAFC" text-anchor="middle">{views_count}</text>\n        <text x="0" y="28" font-family="\'Inter\', sans-serif" font-size="10" font-weight="700" fill="#94A3B8" letter-spacing="1" text-anchor="middle">PROFILE VIEWS</text>',
        content
    )

    # Stat cards
    content = re.sub(r'fill="#F8FAFC">25 <tspan', f'fill="#F8FAFC">{views_count} <tspan', content)
    content = re.sub(r'fill="#F8FAFC">25</text>\s*<text [^>]*>Since launched', f'fill="#F8FAFC">{views_count}</text>\n            <text x="94" y="48" font-family="\'Inter\', sans-serif" font-size="9.5" fill="#64748B">Since launched', content)

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated quote_views.svg with real profile view count: {views_count}")

def main():
    user_data = fetch_json(f"https://api.github.com/users/{USERNAME}")
    repos_data = fetch_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=100")
    views_count = fetch_views()

    if not user_data:
        print("Failed to fetch user data")
        return

    public_repos = user_data.get("public_repos", 10)
    followers = user_data.get("followers", 0)

    total_stars = 0
    if repos_data and isinstance(repos_data, list):
        for repo in repos_data:
            if repo.get("fork"):
                continue
            total_stars += repo.get("stargazers_count", 0)

    print(f"User: {USERNAME}")
    print(f"Public Repos: {public_repos}")
    print(f"Followers: {followers}")
    print(f"Total Stars: {total_stars}")
    print(f"Profile Views: {views_count}")

    update_github_stats(public_repos, followers, total_stars)
    update_quote_views(views_count)

if __name__ == "__main__":
    main()
