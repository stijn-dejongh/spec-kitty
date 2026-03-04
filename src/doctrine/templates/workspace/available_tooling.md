# Available Tooling (Session)

## Purpose
Record which preferred workspace tools are available at session startup, the final tooling decision for this session, and rationale for any missing-tool remediation guidance.

## Privacy Constraint
Do not store personally identifiable information (PII) in this file.

Do not include:
- IP addresses
- hostnames or system names
- usernames
- machine IDs or similar unique identifiers

## Session Summary
- Decision timestamp (UTC): <YYYY-MM-DDTHH:MM:SSZ>
- Final decision summary: <short summary>
- Rationale summary: <short rationale>

## Tool Availability
| Tool | Available (yes/no) | Version (optional) | Decision | Rationale / Remediation |
| --- | --- | --- | --- | --- |
| `.venv` (repo-local) | <yes/no> | <version-or-n/a> | <use/refresh/recreate/skip> | <reason + action if missing/outdated> |
| `poetry` | <yes/no> | <version-or-n/a> | <use/skip> | <reason + action if missing> |
| `uv` | <yes/no> | <version-or-n/a> | <use/skip> | <reason + action if missing> |
| `ruff` | <yes/no> | <version-or-n/a> | <use/skip> | <reason + action if missing> |
| `mypy` | <yes/no> | <version-or-n/a> | <use/skip> | <reason + action if missing> |
| local Mermaid tooling | <yes/no> | <version-or-n/a> | <use/skip> | <reason + action if missing> |
| `rg` (ripgrep) | <yes/no> | <version-or-n/a> | <use/skip> | <reason + action if missing> |

## Notes
- Keep this file session-focused and concise.
- Prefer actionable remediation text when a tool is missing.
