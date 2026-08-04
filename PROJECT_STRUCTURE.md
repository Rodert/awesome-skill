# Project Structure

```text
awesome-skill/
├── .github/workflows/       # Daily collection and GitHub Pages deployment
├── data/skills.json         # Canonical skill catalog
├── docs/                    # VitePress site source
│   ├── .vitepress/config.js # Site configuration
│   ├── data/skills.json     # Copy used by the site
│   ├── en/projects.md       # Generated English directory
│   └── zh/projects.md       # Generated Chinese directory
├── scripts/
│   ├── collect_skills.py    # GitHub collector and classifier
│   └── generate_markdown.py # Markdown and data generator
├── CONTRIBUTING.md
├── package.json
└── README.md
```

`collect_skills.py` fetches repositories from the GitHub Search API and writes the canonical JSON file. `generate_markdown.py` turns that data into the directory pages. GitHub Actions runs the two scripts daily, builds the documentation site, and deploys it to GitHub Pages.
