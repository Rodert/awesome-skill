#!/usr/bin/env python3
"""Collect GitHub repositories that package reusable Agent Skills."""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "skills.json"
QUERIES = ["SKILL.md", "agent skill", "claude skill", "codex skill"]
def categorize(repo):
    text = " ".join([repo.get("name", ""), repo.get("description", ""), " ".join(repo.get("topics", []))]).lower()
    for category, words in {
        "coding": ("code", "coding", "programming", "developer", "software"),
        "research": ("research", "paper", "academic", "literature"),
        "writing": ("writing", "content", "copywriting", "documentation"),
        "data": ("data", "analytics", "spreadsheet", "sql", "automation"),
        "devops": ("devops", "deployment", "docker", "kubernetes", "security"),
        "creative": ("image", "video", "design", "creative", "media"),
    }.items():
        if any(word in text for word in words):
            return category
    return "other"


def request_json(url, token):
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "awesome-skill", "Authorization": f"Bearer {token}" if token else ""})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    token = os.environ.get("GITHUB_TOKEN", "")
    existing = json.loads(DATA_FILE.read_text(encoding="utf-8")) if DATA_FILE.exists() else {"skills": []}
    skills = {item["full_name"]: item for item in existing.get("skills", [])}
    if not token:
        print("GITHUB_TOKEN is not set; keeping existing data.")
    else:
        for query in QUERIES:
            params = urllib.parse.urlencode({"q": f'"{query}" in:readme stars:>=5', "sort": "stars", "order": "desc", "per_page": 50})
            try:
                for repo in request_json(f"https://api.github.com/search/repositories?{params}", token).get("items", []):
                    full_name = repo["full_name"]
                    skills[full_name] = {
                        "name": repo["name"], "full_name": full_name,
                        "description": repo.get("description") or "",
                        "url": repo["html_url"], "stars": repo.get("stargazers_count", 0),
                        "language": repo.get("language") or "N/A", "updated_at": repo.get("updated_at", ""),
                        "topics": repo.get("topics", []), "category": categorize(repo),
                        "owner": repo["owner"]["login"], "archived": repo.get("archived", False),
                        "has_skill_file": "SKILL.md" in (repo.get("description") or "") or "skill" in (repo.get("name") or "").lower(),
                    }
            except urllib.error.HTTPError as error:
                print(f"Search failed for {query}: HTTP {error.code}")
    output = {"last_updated": datetime.now(timezone.utc).isoformat(), "total": len(skills), "skills": sorted(skills.values(), key=lambda item: item["stars"], reverse=True)}
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output['total']} skills to {DATA_FILE}")


if __name__ == "__main__":
    main()
