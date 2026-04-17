from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import textwrap
from typing import Any

HELP_DESCRIPTION_COLUMN = 46
HELP_FLAG_DESCRIPTION_COLUMN = 48
HELP_TEXT_WIDTH = max(140, shutil.get_terminal_size(fallback=(140, 40)).columns)
USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[38;5;203m"
GRAY = "\033[38;5;245m"
LIGHT_GRAY = "\033[38;5;250m"
BLUE = "\033[38;5;75m"
CYAN = "\033[38;5;153m"
DIM = GRAY
GREEN = BLUE
YELLOW = BLUE
MAGENTA = CYAN

class MonarchHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def __init__(self, prog: str) -> None:
        super().__init__(prog, max_help_position=HELP_DESCRIPTION_COLUMN, width=HELP_TEXT_WIDTH)

    def _format_action(self, action: argparse.Action) -> str:
        text = super()._format_action(action)
        if isinstance(action, argparse._SubParsersAction):
            lines = text.splitlines()
            filtered_lines: list[str] = []
            removed = False
            for line in lines:
                if not removed and line.lstrip().startswith("{"):
                    removed = True
                    continue
                filtered_lines.append(line)
            suffix = "\n" if text.endswith("\n") else ""
            return "\n".join(filtered_lines) + suffix
        return text


class MonarchArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("formatter_class", MonarchHelpFormatter)
        self.extra_option_rows = kwargs.pop("extra_option_rows", [])
        super().__init__(*args, **kwargs)

    def format_help(self) -> str:
        text = super().format_help()
        if self.extra_option_rows:
            text = inject_extra_option_rows(text, self.extra_option_rows)
        return colorize_help_text(text)


def color(text: str, *codes: str) -> str:
    if not USE_COLOR or not codes:
        return text
    return f"{''.join(codes)}{text}{RESET}"


def colorize_help_text(text: str) -> str:
    colored_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()

        if "\033[" in line:
            colored_lines.append(line)
            continue

        if line.startswith("usage:"):
            colored_lines.append(color("usage:", BOLD, CYAN) + color(line[len("usage:"):], LIGHT_GRAY))
            continue

        if re.match(r"^[A-Za-z][A-Za-z0-9 /_-]*:$", stripped):
            heading = stripped[:-1].title() + ":"
            colored_lines.append(color(heading, BOLD, CYAN))
            continue

        if stripped.startswith("{") and stripped.endswith("} ..."):
            colored_lines.append(color(line, BLUE))
            continue

        entry_match = re.match(r"^(\s+)(\S(?:.*?\S)?)(\s{2,}.*)$", line)
        if entry_match:
            indent, token, description = entry_match.groups()
            colored_lines.append(f"{indent}{color(token, BOLD, BLUE)}{color(description, LIGHT_GRAY)}")
            continue

        if stripped.startswith("--") or stripped.startswith("-"):
            colored_lines.append(color(line, BLUE))
            continue

        if stripped:
            colored_lines.append(color(line, LIGHT_GRAY))
            continue

        colored_lines.append(line)

    return "\n".join(colored_lines) + ("\n" if text.endswith("\n") else "")


def inject_extra_option_rows(text: str, rows: list[tuple[str, str]]) -> str:
    lines = text.splitlines()
    output: list[str] = []
    index = 0
    inserted = False
    while index < len(lines):
        line = lines[index]
        output.append(line)
        if not inserted and line.strip().lower() == "options:":
            next_index = index + 1
            while next_index < len(lines) and not lines[next_index].strip():
                output.append(lines[next_index])
                next_index += 1

            for token, description in rows:
                output.extend(
                    format_help_columns(
                        2,
                        token,
                        description,
                        description_column=HELP_DESCRIPTION_COLUMN,
                        width=HELP_TEXT_WIDTH,
                    )
                )
            inserted = True
            index = next_index
            continue
        index += 1

    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def command_tree_group(text: str) -> str:
    return color(text, BOLD, BLUE)


def command_tree_item(text: str) -> str:
    return color(text, LIGHT_GRAY)


def format_help_columns(
    indent: int,
    token: str,
    description: str = "",
    *,
    token_styles: tuple[str, ...] = (),
    description_styles: tuple[str, ...] = (LIGHT_GRAY,),
    description_column: int = HELP_DESCRIPTION_COLUMN,
    width: int = HELP_TEXT_WIDTH,
) -> list[str]:
    prefix = " " * indent
    token_text = color(token, *token_styles) if token_styles else token
    description = description.strip()
    if not description:
        return [f"{prefix}{token_text}"]

    if len(token) + indent + 2 < description_column:
        gap = " " * (description_column - indent - len(token))
        wrapped = textwrap.wrap(description, width=max(20, width - description_column)) or [description]
        lines = [f"{prefix}{token_text}{gap}{color(wrapped[0], *description_styles)}"]
        continuation_prefix = " " * description_column
        for continuation in wrapped[1:]:
            lines.append(f"{continuation_prefix}{color(continuation, *description_styles)}")
        return lines

    wrapped = textwrap.wrap(description, width=max(20, width - description_column)) or [description]
    lines = [f"{prefix}{token_text}"]
    continuation_prefix = " " * description_column
    for continuation in wrapped:
        lines.append(f"{continuation_prefix}{color(continuation, *description_styles)}")
    return lines


def build_command_tree() -> str:
    tree = [
        ("auth", [("login", "Interactive login and save the local session file."), ("use-token", "Save a known Monarch token as the local session."), ("me", "Show the authenticated user."), ("clear-session", "Delete the saved local session file.")]),
        ("household", [("get", "Show the current household record."), ("members", "Show household members and current-user context."), ("preferences", "Show household preferences and budget settings.")]),
        ("accounts", [("has-accounts", "Show whether the household has accounts."), ("syncing", "Show whether any accounts are currently syncing."), ("notices", "List active institution notices."), ("page", "Show the accounts page payload with account-type summaries."), ("recent-balances", "Show recent account balance history."), ("filtered", "List accounts matching account filters."), ("aggregate-snapshots", "Show aggregate balance snapshots over time."), ("display-balance", "Show account display balances at one date."), ("snapshots-by-account-type", "Show account-type balance snapshots over time."), ("filters", "Show account filter data used by the web UI."), ("account-types", "Show available account types and subtypes."), ("refresh-status", "Show whether one account can be force refreshed."), ("latest-refresh", "Show the latest household force-refresh operation."), ("refresh-operation", "Show one force-refresh operation by ID."), ("refresh-account", "Request a force refresh for one account."), ("refresh-all", "Request a force refresh for all accounts."), ("institution-settings", "Show institution credentials, linked accounts, and subscription state."), ("institutions", "List institution metadata from the institution service."), ("institution", "Show one institution metadata record by ID.")]),
        ("subscription", [("details", "Show the smaller subscription details payload."), ("get", "Show the full billing/subscription payload with invoices."), ("modal", "Show the subscription modal payload with optional promo inputs."), ("premium-upgrade-plans", "Show available premium upgrade plans and referral context."), ("trial-status", "Show trial eligibility and entitlement state."), ("entitlements", "Show the current household entitlement list."), ("feature-entitlement-params", "Show feature-level entitlement requirements."), ("plus-tier-access", "Show current plus-tier entitlement access."), ("gifted-subscriptions", "Show gifted subscriptions purchased by the household."), ("referral-settings", "Show referral statistics and redemption totals.")]),
        ("settings", [("user-profile-flags", "Show user-profile flags and walkthrough state."), ("dashboard-config", "Show saved web/mobile dashboard layout config."), ("sidebar-data", "Show sidebar/profile/subscription summary data."), ("household-member-settings", "Show household member, invite, and access-grant settings."), ("security", "Show security settings, MFA state, and linked auth providers."), ("notification-preferences", "Show notification preference rows."), ("review-summary-by-user", "Show needs-review counts grouped by user."), ("business-entities-banner-profile", "Show business-entity banner profile state."), ("business-entities", "Show configured business entities."), ("has-activity", "Show whether the user has new activity."), ("oldest-deletable-synced-snapshot-date", "Show the oldest deletable synced snapshot date."), ("oldest-deletable-transaction-date", "Show the oldest deletable transaction date.")]),
        ("planning", [("budget-data", "Show budget data for a date range."), ("joint-data", "Show joint planning data for a date range.")]),
        ("goals", [("savings-goals", "List savings goals."), ("savings-goals-balances", "Show savings goals with this-month balances."), ("savings-goal-account", "Show one goal-linked account by ID."), ("dashboard-card", "Show the goals dashboard card payload."), ("legacy-migration", "Show legacy-goals migration state and debt accounts.")]),
        ("recurring", [("streams", "List recurring streams."), ("aggregated-items", "Show aggregated recurring items for a date range."), ("dashboard-upcoming", "Show upcoming recurring dashboard items for a date range."), ("paused-banner", "Show recurring paused-banner state.")]),
        ("investments", [("accounts", "List investment accounts."), ("dashboard-card", "Show the investments dashboard card payload."), ("portfolio", "Show portfolio performance and aggregate holdings."), ("security-history", "Show historical performance for one or more securities.")]),
        ("transactions", [("list", "List transactions with optional pagination and filters."), ("get", "Show one transaction by ID."), ("filters", "Fetch filter option data used by the transactions UI."), ("filters-metadata", "Fetch metadata for a supplied transaction filter object."), ("create", "Create a manual transaction using explicit flags or a JSON file."), ("update", "Update one transaction using explicit flags or a JSON file."), ("delete", "Delete one transaction by ID."), ("set-tags", "Replace the tags for one transaction."), ("tags", "List household transaction tags."), ("categories", "List transaction categories and groups.")]),
        ("merchants", [("search", "Search merchants by name."), ("household", "List household merchants."), ("recommended", "Show recommended merchants for a transaction."), ("update", "Update a merchant using explicit flags or a JSON file.")]),
        ("attachments", [("upload-info", "Get upload metadata for a transaction attachment."), ("add", "Add an attachment using explicit flags or a JSON file payload."), ("get", "Show one attachment by ID."), ("delete", "Delete one attachment by ID.")]),
        ("rules", [("list", "List transaction rules."), ("create", "Create one transaction rule using explicit flags or a JSON file."), ("update", "Update one transaction rule using explicit flags or a JSON file."), ("delete", "Delete one transaction rule by ID."), ("preview", "Preview a transaction rule against matching transactions."), ("update-order", "Update a transaction rule's order."), ("delete-all", "Delete all transaction rules.")]),
        ("reports", [("cash-flow-dashboard", "Show cash-flow dashboard totals by day."), ("cash-flow-entities", "Show cash-flow aggregates by category, group, and merchant."), ("cash-flow-timeframes", "Show cash-flow aggregates by year, month, and quarter."), ("data", "Show the general reports data payload.")]),
        ("retail-sync", [("settings", "Show retail sync extension settings."), ("get", "Show one retail sync record by ID."), ("list", "List retail sync records."), ("create", "Create one retail sync record from explicit flags or a JSON file."), ("create-bulk", "Create retail sync records in bulk from explicit flags or a JSON file."), ("start", "Start a retail sync by ID."), ("complete", "Complete a retail sync by ID."), ("delete", "Delete an unmatched retail sync by ID."), ("match", "Match a retail transaction to a Monarch transaction."), ("unmatch", "Unmatch a retail transaction."), ("update-order", "Update a retail order using explicit flags or a JSON file."), ("update-vendor-settings", "Update retail vendor settings using explicit flags or a JSON file.")]),
    ]
    lines = [color("Command Tree:", BOLD, CYAN)]
    for group, commands in tree:
        lines.append(f"  {command_tree_group(group)}")
        for command, description in commands:
            lines.extend(format_help_columns(4, command, description, token_styles=(LIGHT_GRAY,)))
    return "\n".join(lines)


def summarize_parser_actions(parser: argparse.ArgumentParser) -> list[str]:
    lines: list[str] = []
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            continue

        option_strings = list(action.option_strings)
        if option_strings == ["-h", "--help"]:
            continue

        if option_strings:
            token = ", ".join(option_strings)
            required = action.required
        else:
            metavar = action.metavar or action.dest
            token = f"<{str(metavar).lower()}>"
            required = True

        description = action.help or ""
        description = description.replace("%(default)s", str(action.default))
        if required:
            description = f"{description} [required]".strip()
        lines.extend(
            format_help_columns(
                6,
                token,
                description,
                token_styles=(GRAY,),
                description_styles=(GRAY,),
                description_column=HELP_FLAG_DESCRIPTION_COLUMN,
            )
        )
    return lines


def summarize_root_options(parser: argparse.ArgumentParser) -> list[str]:
    lines: list[str] = []
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            continue
        option_strings = list(action.option_strings)
        if not option_strings:
            continue
        token = ", ".join(option_strings)
        description = action.help or ""
        description = description.replace("%(default)s", str(action.default))
        lines.extend(
            format_help_columns(
                2,
                token,
                description,
                token_styles=(BLUE, BOLD),
                description_styles=(LIGHT_GRAY,),
            )
        )
    return lines


def summarize_command_groups(parser: argparse.ArgumentParser) -> list[str]:
    lines: list[str] = []
    for action in parser._actions:
        if not isinstance(action, argparse._SubParsersAction):
            continue
        for choice in action._get_subactions():
            lines.extend(
                format_help_columns(
                    4,
                    choice.dest,
                    choice.help or "",
                    token_styles=(BLUE, BOLD),
                    description_styles=(LIGHT_GRAY,),
                )
            )
    return lines


def print_help_all(parsers: dict[str, argparse.ArgumentParser]) -> None:
    root = parsers["root"]
    lines = [
        root.description or "",
        "",
        color("Options:", BOLD, CYAN),
        *summarize_root_options(root),
        "",
        color("Command Groups:", BOLD, CYAN),
        *summarize_command_groups(root),
        "",
        color("Command Tree:", BOLD, CYAN),
    ]
    current_group: str | None = None
    for key in parsers:
        if key == "root":
            continue

        if " " not in key:
            current_group = key
            lines.append(f"  {command_tree_group(current_group)}")
            continue

        group, command = key.split(" ", 1)
        if group != current_group:
            lines.append(f"  {command_tree_group(group)}")
            current_group = group
        parser = parsers[key]
        description = parser.description or ""
        lines.extend(format_help_columns(4, command, description, token_styles=(LIGHT_GRAY,)))
        lines.extend(summarize_parser_actions(parser))

    print("\n".join(lines).rstrip())
