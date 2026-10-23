# Awesome DeepSeek Harness (Chinese Guide): dsh Tutorial, Plugins & Skills

[中文](README.md) | **English**

**DeepSeek Harness (`dsh`) is DeepSeek's open-source AI agent harness built on an "everything is a plugin" architecture (MIT).** This repo is a Chinese-first guide to installing dsh, configuring models and API keys, installing plugins and skills, changing the defaults that matter for privacy, and fixing common errors, plus a curated list of 68 plugins, skills and tutorials.

Last checked **2026-10-23** against dsh `0.2.1-rc` (developer preview: expect breaking changes). Maintained by [Orbis (orbiorbi.com)](https://orbiorbi.com/?utm_source=github&utm_medium=readme&utm_campaign=awesome-deepseek-harness-zh&utm_content=en-intro); not affiliated with DeepSeek.

## Quick start

| Method | Command / download |
|---|---|
| Desktop app (Windows x64, macOS) | [Windows](https://download.deepseek.com/desktop/dsh-latest-windows-x64.exe) · [macOS arm64](https://download.deepseek.com/desktop/dsh-latest-macos-arm64.dmg) · [macOS x64](https://download.deepseek.com/desktop/dsh-latest-macos-x64.dmg) |
| npx (official quick start) | `npx @deepseek-ai/dsh web`, then open `http://127.0.0.1:3080` (not `localhost`, which returns 403) |
| From source (Node 22.19+ / 24+, pnpm) | `pnpm install && pnpm run build && pnpm dsh web` |

Then: **Settings → Models** to add a DeepSeek API key, and **Choose workspace** (the composer stays disabled until you do).

## Defaults worth changing first

1. **Session-log upload is on by default** when using the official DeepSeek API: turn it off in Settings → General.
2. **OpenTelemetry upload applies to all users**: set `DSH_TELEMETRY_MODE=DISABLED`.
3. **The built-in web search** sends the `deepseek-official` key (as `x-api-key` and `Authorization`) to its configured base URL and costs a full model turn per search. Disable it when you use a third-party provider.
4. dsh runs model-generated commands and third-party plugins and has not been security-audited: use a VM or container.

## Guides (Chinese)

| Guide | Topics |
|---|---|
| [Install](docs/install.md) | Desktop, npx, global npm, source; npx appears to hang; Windows folder picker |
| [Models & API keys](docs/models.md) | DeepSeek, Kimi, GLM, custom OpenAI-compatible providers, gateway example |
| [Plugins](docs/plugins.md) | `dsh plugin --profile web add <pkg>`, plugin markets, 51 curated plugins |
| [Skills](docs/skills.md) | Skill directories and precedence, `SKILL.md` format, curated skills |
| [MCP](docs/mcp.md) | `@deepseek-ai/dsh-mcp-client` YAML config |
| [Privacy & security](docs/privacy-security.md) | Turn off uploads, proxy credential exposure, isolation |
| [Troubleshooting](docs/troubleshooting.md) | 403, connection failures, `UNKNOWN_MODEL`, output token limit |
| [Resources](docs/resources.md) | Official links, community tutorials, other lists |

## Use other models

dsh ships providers for Kimi (`moonshotai`), GLM (`zai`), OpenAI, Anthropic and more, and accepts any OpenAI- or Anthropic-compatible endpoint via **Settings → Models → Add model provider → Custom model API**. Gateway example with [Orbis](https://orbiorbi.com/en/docs/deepseek-harness/?utm_source=github&utm_medium=readme&utm_campaign=awesome-deepseek-harness-zh&utm_content=en-models): [docs/models.md](docs/models.md#接入第三方--聚合平台以-orbis-为例).

## Contributing

Suggest plugins, skills or tutorials via [Issues](../../issues/new/choose) or a PR to [`data/projects.json`](data/projects.json) (then run `python scripts/render.py`). Not accepted: jailbreak prompts, reverse-engineered APIs, "free model, no key" plugins of unknown origin, tools that borrow other people's subscriptions.

## License

[CC0 1.0](LICENSE). Disclosure: maintained by the Orbis team; Orbis links carry UTM tags for analytics, no referral rewards.
