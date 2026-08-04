# Awesome Skill

> A curated, automatically maintained list of reusable skills for AI coding agents.

[![Auto Update](https://github.com/Rodert/awesome-skill/actions/workflows/update-skills.yml/badge.svg)](https://github.com/Rodert/awesome-skill/actions)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

**Languages:** [English](README.md) | [中文](README.zh.md)

Awesome Skill discovers and organizes practical skills for [Codex](https://openai.com/codex/), Claude Code, Cursor, OpenCode, and compatible AI coding agents. The list is refreshed daily from GitHub and published as a searchable site.

## Browse Skills

- [Skill directory](https://rodert.github.io/awesome-skill/en/projects)
- [中文目录](https://rodert.github.io/awesome-skill/zh/projects)

## What Is A Skill?

A skill is a small, reusable package of instructions, references, scripts, and assets that gives an AI agent reliable domain expertise or a repeatable workflow. A high-quality skill is focused, documented, and usable by more than one project.

## Categories

- Coding
- Research
- Writing
- Data & Automation
- DevOps
- Creative
- Other

## Local Development

```bash
pnpm install
pnpm dev
```

To refresh the catalog locally, provide a GitHub token and run:

```bash
export GITHUB_TOKEN=github_pat_your_token
pnpm collect
pnpm generate
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) to submit a skill or improve a classification.
