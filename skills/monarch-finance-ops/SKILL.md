---
name: monarch-finance-ops
description: Analyze, reconcile, budget, and safely manage Monarch financial data through the `monarch` CLI in this repository. Use when asked to inspect spending, cash flow, budgets, account balances, recurring transactions, merchants, tags, goals, reports, or transaction rules, and when preparing safe transaction-management workflows or JSON filter payloads for this CLI.
---

# Monarch Finance Ops

## Overview

Use the repo's `monarch` command to inspect or manage Monarch data with a bias toward read-only analysis first. Treat live mutations as high-risk financial operations: confirm intent from the user's request, inspect current state before changing it, and summarize exactly what changed.

Read [references/cli-recipes.md](references/cli-recipes.md) when you need task-to-command mappings, filter examples, or domain-specific command recipes.

## Workflow

### 1. Confirm the operating mode

- Prefer read-only commands for analysis, reconciliation, reporting, and discovery.
- Treat `transactions create`, `transactions update`, `transactions delete`, `transactions set-tags`, `merchants update`, `rules create`, `rules update`, `rules delete`, and similar commands as live mutations.
- If the user asked for analysis, recommendations, or tracking help, do not mutate data unless they clearly escalated to an action request.

### 2. Start with the narrowest read-only query that answers the question

- Use `--details` when you need raw payloads for deeper analysis.
- Use focused filters rather than dumping broad datasets when the user has a bounded question.
- Prefer `reports`, `planning`, `goals`, `accounts`, and read-only `transactions` commands before considering manual calculations.

### 3. Convert the user question into one of these buckets

- Spending or transaction review
- Cash flow or reporting
- Budget status or planning
- Account balance, trend, or institution health
- Goal or savings progress
- Cleanup or operational changes to transactions, merchants, tags, or rules

Use [references/cli-recipes.md](references/cli-recipes.md) to select the matching command family.

### 4. For analysis tasks, produce both evidence and interpretation

- Show the exact command(s) used.
- Summarize what the data says in plain language.
- Separate facts from inference.
- If the user would benefit from follow-up actions, propose them before running them.

### 5. For mutation tasks, use a safe change loop

1. Inspect current state with a read-only command.
2. Build the smallest mutation payload that satisfies the request.
3. If the request is ambiguous or could affect many records, stop and clarify instead of guessing.
4. Run the mutation.
5. Re-read the affected entity when possible.
6. Report exactly what changed.

## Safety Rules

- Never delete or rewrite financial data unless the user explicitly asked for that result.
- Never assume a merchant rename, category change, or rule update is harmless; verify the target record first.
- Prefer targeted changes over bulk changes.
- Use JSON payload files only when the mutation shape is complex enough to justify them.
- When working with a real account, mention that the operation is live if there is any chance the user may not realize it.

## Operating Notes

- The installed command is `monarch`.
- The default saved session is `~/.monarch-api-cli/monarch_session.json`.
- The previous session path `~/.monarch-cli/monarch_session.json` is still accepted as a legacy location.
- For raw machine-readable payloads, prefer `--details`.
- For broad analysis requests, save intermediate outputs to local temp files only if that materially improves clarity or repeatability.

## Common Intent Mapping

- "Where is the money going?" -> `transactions list`, `transactions filters`, `reports cash-flow-*`, `reports data`
- "How am I doing against budget?" -> `planning budget-data`, `household preferences`, `reports data`
- "What changed in account balances?" -> `accounts recent-balances`, `accounts aggregate-snapshots`, `accounts display-balance`
- "What recurring bills or income should I expect?" -> `recurring streams`, `recurring aggregated-items`, `recurring dashboard-upcoming`
- "Help me fix transaction categorization/tags/merchant names" -> inspect with `transactions get` or `transactions list`, then mutate with the smallest targeted command
- "Help me create rules for recurring cleanup" -> inspect current transactions and existing rules first, then use `rules preview` before `rules create`

## References

- Read [references/cli-recipes.md](references/cli-recipes.md) for command recipes and example filter patterns.
