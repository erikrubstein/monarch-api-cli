# monarch-api-cli

Installable command-line interface for the published [`monarch-api`](https://pypi.org/project/monarch-api/) Python client.

The package stays close to the current Monarch surface instead of adding a second abstraction layer on top of the API client. Commands are organized by domain and generally map one read or mutation workflow to one CLI command.

## Install

```bash
pip install monarch-api-cli
```

For local development:

```bash
pip install -e .[dev]
```

## Example

```bash
monarch auth login
monarch household preferences
monarch accounts page
monarch transactions list --limit 10
monarch reports cash-flow-dashboard --start-date 2026-04-01 --end-date 2026-04-16
```

## Notes

- Built on top of `monarch-api`, which remains the underlying Python client.
- Installed console command is `monarch`.
- Defaults to summarized output; use `--details` for raw payloads.
- Saves session state at `~/.monarch-api-cli/monarch_session.json`.
- Still accepts the legacy session path `~/.monarch-cli/monarch_session.json`.

## Implemented Surface

### `auth`

- `login`
- `use-token`
- `me`
- `clear-session`

### `household`

- `get`
- `members`
- `preferences`

### `accounts`

- `has-accounts`
- `syncing`
- `notices`
- `page`
- `recent-balances`
- `filtered`
- `aggregate-snapshots`
- `display-balance`
- `snapshots-by-account-type`
- `filters`
- `account-types`
- `refresh-status`
- `latest-refresh`
- `refresh-operation`
- `refresh-account`
- `refresh-all`
- `institution-settings`
- `institutions`
- `institution`

### `subscription`

- `details`
- `get`
- `modal`
- `premium-upgrade-plans`
- `trial-status`
- `entitlements`
- `feature-entitlement-params`
- `plus-tier-access`
- `gifted-subscriptions`
- `referral-settings`

### `settings`

- `user-profile-flags`
- `dashboard-config`
- `sidebar-data`
- `household-member-settings`
- `security`
- `notification-preferences`
- `review-summary-by-user`
- `business-entities-banner-profile`
- `business-entities`
- `has-activity`
- `oldest-deletable-synced-snapshot-date`
- `oldest-deletable-transaction-date`

### `planning`

- `budget-data`
- `joint-data`

### `goals`

- `savings-goals`
- `savings-goals-balances`
- `savings-goal-account`
- `dashboard-card`
- `legacy-migration`

### `recurring`

- `streams`
- `aggregated-items`
- `dashboard-upcoming`
- `paused-banner`

### `investments`

- `accounts`
- `dashboard-card`
- `portfolio`
- `security-history`

### `transactions`

- `list`
- `get`
- `filters`
- `filters-metadata`
- `create`
- `update`
- `delete`
- `set-tags`
- `tags`
- `categories`

### `merchants`

- `search`
- `household`
- `recommended`
- `update`

### `attachments`

- `upload-info`
- `add`
- `get`
- `delete`

### `rules`

- `list`
- `create`
- `update`
- `delete`
- `preview`
- `update-order`
- `delete-all`

### `reports`

- `cash-flow-dashboard`
- `cash-flow-entities`
- `cash-flow-timeframes`
- `data`

### `retail-sync`

- `settings`
- `get`
- `list`
- `create`
- `create-bulk`
- `start`
- `complete`
- `delete`
- `match`
- `unmatch`
- `update-order`
- `update-vendor-settings`

## Layout

- `src/monarch_cli/`: CLI implementation
- `tests/`: mocked verification for payload shaping and CLI behavior
- `skills/`: repo-local agent skills for recurring Monarch workflows
