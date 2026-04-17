# CLI Recipes

## Transaction Analysis

Use when the user wants to inspect spending, review transactions, find unusual merchants, or prepare cleanup actions.

Common commands:

```bash
monarch transactions list --limit 25
monarch transactions list --start-date 2026-04-01 --end-date 2026-04-16 --search coffee
monarch transactions get <transaction-id>
monarch transactions filters
monarch transactions filters-metadata --start-date 2026-04-01 --end-date 2026-04-16 --account-id <id>
monarch transactions tags
monarch transactions categories
```

Guidance:

- Use `transactions list` for quick review.
- Use `transactions get` before any targeted mutation.
- Use `transactions filters` or `filters-metadata` to discover valid IDs before building complex filters.

## Budget And Planning

Use when the user asks about budget status, monthly planning, or household budget settings.

Common commands:

```bash
monarch planning budget-data --start-date 2026-04-01 --end-date 2026-04-30
monarch household preferences
monarch reports data --start-date 2026-04-01 --end-date 2026-04-30 --group-by category
```

Guidance:

- Start with `planning budget-data` for explicit budget analysis.
- Use `household preferences` when the question is about settings, rollover, or household budgeting behavior.
- Use `reports data` when the user needs grouped comparisons or custom slices.

## Cash Flow And Reporting

Use when the user asks for income vs expense trends, grouped cash flow, or time-series summaries.

Common commands:

```bash
monarch reports cash-flow-dashboard --start-date 2026-01-01 --end-date 2026-04-16
monarch reports cash-flow-entities --start-date 2026-04-01 --end-date 2026-04-16
monarch reports cash-flow-timeframes --start-date 2026-01-01 --end-date 2026-04-16
monarch reports data --start-date 2026-04-01 --end-date 2026-04-16 --group-by merchant --sort-by sum_expense
```

Guidance:

- Use `cash-flow-dashboard` for day-level trend summaries.
- Use `cash-flow-entities` for category/group/merchant attribution.
- Use `reports data` when the built-in summaries are too coarse.

## Accounts And Balances

Use when the user asks about balances, account trends, sync health, or institution issues.

Common commands:

```bash
monarch accounts page
monarch accounts recent-balances --start-date 2026-04-01
monarch accounts aggregate-snapshots --start-date 2026-01-01 --timeframe month
monarch accounts display-balance --date 2026-04-16
monarch accounts syncing
monarch accounts notices
monarch accounts institution-settings
```

Guidance:

- Use `accounts page` for a household-level view.
- Use `recent-balances` or `aggregate-snapshots` for trend questions.
- Use `syncing`, `notices`, and `institution-settings` for operational/debugging issues.

## Goals And Recurring Items

Use when the user asks about savings goals, goal-linked accounts, or recurring income/expense expectations.

Common commands:

```bash
monarch goals savings-goals
monarch goals savings-goals-balances
monarch goals dashboard-card
monarch recurring streams
monarch recurring aggregated-items --start-date 2026-04-01 --end-date 2026-04-30
monarch recurring dashboard-upcoming --start-date 2026-04-16 --end-date 2026-05-16
```

Guidance:

- Use `goals savings-goals-balances` for progress questions.
- Use `recurring aggregated-items` or `dashboard-upcoming` for expected bills or income.

## Safe Mutation Workflow

Use when the user explicitly wants to change data.

Typical flow:

```bash
monarch transactions get <transaction-id>
monarch transactions update --transaction-id <transaction-id> --category-id <category-id>
monarch transactions get <transaction-id>
```

Other mutation families:

```bash
monarch transactions set-tags <transaction-id> --tag-id <tag-id>
monarch merchants update --merchant-id <merchant-id> --name "New Name"
monarch rules preview --merchant-name-criteria-operator contains --merchant-name-criteria-value venmo
monarch rules create ...
```

Guidance:

- Inspect first, mutate second, verify third.
- Prefer a single targeted update over a rule or bulk-like operation unless the user explicitly wants automation.
- Use `rules preview` before `rules create` or `rules update`.

## JSON Payloads

Use JSON files when the payload is too complex or repeated enough that flags become error-prone.

Examples:

```bash
monarch transactions create --input-json-file payload.json
monarch transactions update --input-json-file payload.json
monarch rules create --input-json-file rule.json
monarch reports data --filters-json-file filters.json --group-by category
```

Guidance:

- Keep JSON payloads minimal.
- Prefer explicit flags when only a few fields are needed.
- Mention in the final response whether a file-based payload was used.
