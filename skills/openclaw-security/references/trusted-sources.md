# Trusted Sources Reference

Publishers and registries that are generally considered reputable. Trust is never unconditional — always review code regardless of source.

## Package Registries

| Registry | URL | Notes |
|---|---|---|
| PyPI | pypi.org | Verify package age and download count |
| npm | npmjs.com | Check weekly downloads; beware new packages |
| crates.io | crates.io | Rust ecosystem; generally high quality |
| Maven Central | search.maven.org | Java/JVM; well-established |
| Homebrew | brew.sh | macOS; community-reviewed |

## GitHub Organizations (Generally Trusted)

- `github.com/anthropics` — Anthropic official
- `github.com/openai` — OpenAI official
- `github.com/microsoft` — Microsoft
- `github.com/google` — Google
- `github.com/aws` — Amazon Web Services
- `github.com/cli` — GitHub CLI official
- `github.com/ohmyzsh` — Oh My Zsh (popular shell framework)
- `github.com/homebrew` — Homebrew

## Trust Signals (Positive)

- Account age > 2 years
- Repo stars > 500 (for general tools)
- Active commit history spanning months/years
- Clear LICENSE file
- CHANGELOG or release notes present
- Verified organization badge on GitHub
- Package has been around for > 1 year
- High weekly download count on registries

## Trust Signals (Negative / Requires Scrutiny)

- Account created within the last 3 months
- Repo with < 5 commits
- No README or minimal documentation
- No LICENSE file
- Install script requires sudo with no explanation
- The URL looks like a CDN but resolves to an unknown IP
- README promises unusually powerful capabilities
- Package name is very close to a popular package but slightly different
