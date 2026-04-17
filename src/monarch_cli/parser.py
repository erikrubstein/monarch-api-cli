from __future__ import annotations

import argparse

from .commands import *
from .style import BOLD, BLUE, CYAN, GREEN, MonarchArgumentParser, build_command_tree, color

def add_details_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--details",
        action="store_true",
        help="Print the full raw response instead of the summarized output.",
    )


def add_json_file_flag(parser: argparse.ArgumentParser, *, required: bool = False) -> None:
    parser.add_argument(
        "--input-json-file",
        required=required,
        help="Path to a JSON file containing the full mutation input object. Flag values override file values.",
    )


def add_filters_file_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--filters-json-file",
        help="Path to a JSON file containing the filters object to send. Flag values override file values.",
    )


def add_transaction_filter_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--start-date",
        help="Transaction/report filter startDate observed in traffic, in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--end-date",
        help="Transaction/report filter endDate observed in traffic, in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--search",
        help="Transaction/report filter search string observed in traffic.",
    )
    parser.add_argument(
        "--account-id",
        action="append",
        help="Account ID filter. Repeat to pass multiple account IDs.",
    )
    parser.add_argument(
        "--tag-id",
        action="append",
        help="Transaction tag ID filter. Repeat to pass multiple tag IDs.",
    )
    parser.add_argument(
        "--category-id",
        action="append",
        help="Category ID filter. Repeat to pass multiple category IDs.",
    )
    parser.add_argument(
        "--category-type",
        help="Category type filter observed in traffic, for example expense or income.",
    )
    parser.add_argument(
        "--transaction-visibility",
        help="Transaction visibility filter. Default: non_hidden_transactions_only.",
    )


def add_rule_input_flags(parser: argparse.ArgumentParser, *, include_rule_id: bool) -> None:
    if include_rule_id:
        parser.add_argument("--rule-id", help="Rule ID.")
    parser.add_argument(
        "--merchant-criteria-use-original-statement",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Value for merchantCriteriaUseOriginalStatement.",
    )
    add_optional_json_file_flag(
        parser,
        "--merchant-criteria-json-file",
        "Path to a JSON file containing the merchantCriteria object.",
    )
    parser.add_argument("--merchant-criteria-operator", help="merchantCriteria.operator value.")
    parser.add_argument("--merchant-criteria-value", help="merchantCriteria.value value.")
    add_optional_json_file_flag(
        parser,
        "--original-statement-criteria-json-file",
        "Path to a JSON file containing the originalStatementCriteria object.",
    )
    parser.add_argument("--original-statement-criteria-operator", help="originalStatementCriteria.operator value.")
    parser.add_argument("--original-statement-criteria-value", help="originalStatementCriteria.value value.")
    add_optional_json_file_flag(
        parser,
        "--merchant-name-criteria-json-file",
        "Path to a JSON file containing the merchantNameCriteria object.",
    )
    parser.add_argument("--merchant-name-criteria-operator", help="merchantNameCriteria.operator value.")
    parser.add_argument("--merchant-name-criteria-value", help="merchantNameCriteria.value value.")
    add_optional_json_file_flag(
        parser,
        "--amount-criteria-json-file",
        "Path to a JSON file containing the amountCriteria object.",
    )
    parser.add_argument("--amount-operator", help="amountCriteria.operator value.")
    parser.add_argument(
        "--amount-is-expense",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="amountCriteria.isExpense value.",
    )
    parser.add_argument("--amount-value", type=float, help="amountCriteria.value value.")
    parser.add_argument("--amount-lower", type=float, help="amountCriteria.valueRange.lower value.")
    parser.add_argument("--amount-upper", type=float, help="amountCriteria.valueRange.upper value.")
    parser.add_argument("--category-id", action="append", help="categoryIds value. Repeat to pass multiple IDs.")
    parser.add_argument("--account-id", action="append", help="accountIds value. Repeat to pass multiple IDs.")
    parser.add_argument(
        "--criteria-owner-is-joint",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="criteriaOwnerIsJoint value.",
    )
    parser.add_argument(
        "--criteria-owner-user-id",
        action="append",
        help="criteriaOwnerUserIds value. Repeat to pass multiple IDs.",
    )
    parser.add_argument(
        "--criteria-business-entity-id",
        action="append",
        help="criteriaBusinessEntityIds value. Repeat to pass multiple IDs.",
    )
    parser.add_argument(
        "--criteria-business-entity-is-unassigned",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="criteriaBusinessEntityIsUnassigned value.",
    )
    parser.add_argument("--set-merchant-action", help="Raw setMerchantAction value sent to the API.")
    parser.add_argument("--set-category-action", help="Raw setCategoryAction value sent to the API.")
    parser.add_argument(
        "--add-tag-action",
        action="append",
        help="addTagsAction value. Repeat to pass multiple IDs.",
    )
    parser.add_argument("--link-goal-action", help="linkGoalAction value.")
    parser.add_argument("--link-savings-goal-action", help="linkSavingsGoalAction value.")
    parser.add_argument(
        "--send-notification-action",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="sendNotificationAction value.",
    )
    parser.add_argument(
        "--set-hide-from-reports-action",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="setHideFromReportsAction value.",
    )
    parser.add_argument("--review-status-action", help="reviewStatusAction value.")
    parser.add_argument("--needs-review-by-user-action", help="needsReviewByUserAction value.")
    parser.add_argument(
        "--unassign-needs-review-by-user-action",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="unassignNeedsReviewByUserAction value.",
    )
    parser.add_argument(
        "--action-set-owner-is-joint",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="actionSetOwnerIsJoint value.",
    )
    parser.add_argument("--action-set-owner", help="actionSetOwner value.")
    parser.add_argument("--action-set-business-entity", help="actionSetBusinessEntity value.")
    parser.add_argument(
        "--action-set-business-entity-is-unassigned",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="actionSetBusinessEntityIsUnassigned value.",
    )
    add_optional_json_file_flag(
        parser,
        "--split-transactions-action-json-file",
        "Path to a JSON file containing the splitTransactionsAction object.",
    )
    parser.add_argument("--split-amount-type", help="splitTransactionsAction.amountType value.")
    add_optional_json_file_flag(
        parser,
        "--split-info-json-file",
        "Path to a JSON file containing the splitTransactionsAction.splitsInfo array.",
    )


def add_account_filter_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--account-subtype",
        action="append",
        help="Account subtype filter observed in traffic, for example checking or credit_card. Repeat to pass multiple values.",
    )


def add_recurring_filter_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--is-completed",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="RecurringTransactionFilter isCompleted value.",
    )


def add_optional_json_file_flag(parser: argparse.ArgumentParser, flag: str, help_text: str) -> None:
    parser.add_argument(flag, help=help_text)


def build_parser() -> tuple[argparse.ArgumentParser, dict[str, argparse.ArgumentParser]]:
    parsers: dict[str, argparse.ArgumentParser] = {}
    description = (
        "Interactive CLI for the currently implemented Monarch auth, household, account, subscription, settings, "
        "planning, goal, recurring, investment, transaction, merchant, attachment, rule, report, and retail sync "
        "endpoints."
    )
    examples = "\n".join(
        [
            color("Examples:", BOLD, CYAN),
            f"  {color('monarch --help', GREEN)}",
            f"  {color('monarch --help all', GREEN)}",
            f"  {color('monarch household preferences', GREEN)}",
            f"  {color('monarch accounts page --account-subtype checking', GREEN)}",
            f"  {color('monarch subscription details', GREEN)}",
            f"  {color('monarch investments portfolio --start-date 2026-03-13 --end-date 2026-04-13', GREEN)}",
            f"  {color('monarch transactions create -d 2026-04-15 -a -12.34 -m Coffee --account-id 1 --category-id 2', GREEN)}",
            f"  {color('monarch transactions create --help', GREEN)}",
        ]
    )
    root = MonarchArgumentParser(
        prog="monarch",
        description=description,
        epilog=f"{build_command_tree()}\n\n{examples}",
    )
    parsers["root"] = root
    for action in root._actions:
        if action.option_strings == ["-h", "--help"]:
            action.help = "show this help message and exit; use '--help all' for the expanded command tree"
            break
    root_sub = root.add_subparsers(dest="command", required=True, title="command groups")

    auth = root_sub.add_parser(
        "auth",
        help="Authentication and saved-session commands.",
        description="Authentication and saved-session commands.",
    )
    parsers["auth"] = auth
    auth_sub = auth.add_subparsers(dest="auth_command", required=True, title="auth commands")

    auth_login = auth_sub.add_parser(
        "login",
        help="Prompt for credentials, authenticate, and save the local session.",
        description="Prompt for credentials, authenticate, and save the local session file.",
    )
    parsers["auth login"] = auth_login
    add_details_flag(auth_login)
    auth_login.set_defaults(func=cmd_auth_login)

    auth_use_token = auth_sub.add_parser(
        "use-token",
        help="Save an existing Monarch token as the local session.",
        description="Save an existing Monarch token as the local session and verify it with /users/me/.",
    )
    parsers["auth use-token"] = auth_use_token
    auth_use_token.add_argument("--token", help="Monarch token to save. If omitted, you will be prompted.")
    auth_use_token.add_argument("--device-uuid", help="Optional device UUID to associate with the token.")
    add_details_flag(auth_use_token)
    auth_use_token.set_defaults(func=cmd_auth_use_token)

    auth_me = auth_sub.add_parser(
        "me",
        help="Show the authenticated user profile.",
        description="Show the authenticated user profile from /users/me/.",
    )
    parsers["auth me"] = auth_me
    add_details_flag(auth_me)
    auth_me.set_defaults(func=cmd_auth_me)

    auth_clear = auth_sub.add_parser(
        "clear-session",
        help="Delete the saved local session file.",
        description="Delete the saved local session file.",
    )
    parsers["auth clear-session"] = auth_clear
    auth_clear.set_defaults(func=cmd_auth_clear_session)

    household = root_sub.add_parser(
        "household",
        help="Household record, member list, and preference commands.",
        description="Household record, member list, and preference commands.",
    )
    parsers["household"] = household
    household_sub = household.add_subparsers(dest="household_command", required=True, title="household commands")

    household_get = household_sub.add_parser(
        "get",
        help="Show the current household record.",
        description="Show the current household record.",
    )
    parsers["household get"] = household_get
    add_details_flag(household_get)
    household_get.set_defaults(func=cmd_household_get)

    household_members = household_sub.add_parser(
        "members",
        help="Show household members and current-user context.",
        description="Show household members and current-user context.",
    )
    parsers["household members"] = household_members
    add_details_flag(household_members)
    household_members.set_defaults(func=cmd_household_members)

    household_preferences = household_sub.add_parser(
        "preferences",
        help="Show household preferences and budget settings.",
        description="Show household preferences and budget settings.",
    )
    parsers["household preferences"] = household_preferences
    add_details_flag(household_preferences)
    household_preferences.set_defaults(func=cmd_household_preferences)

    accounts = root_sub.add_parser(
        "accounts",
        help="Account presence, sync status, institution settings, metadata, page payloads, and filtered account lists.",
        description="Account presence, sync status, institution settings, metadata, page payloads, and filtered account lists.",
    )
    parsers["accounts"] = accounts
    accounts_sub = accounts.add_subparsers(dest="accounts_command", required=True, title="account commands")

    accounts_has_accounts = accounts_sub.add_parser(
        "has-accounts",
        help="Show whether the household has accounts.",
        description="Show whether the household has accounts.",
    )
    parsers["accounts has-accounts"] = accounts_has_accounts
    add_details_flag(accounts_has_accounts)
    accounts_has_accounts.set_defaults(func=cmd_accounts_has_accounts)

    accounts_syncing = accounts_sub.add_parser(
        "syncing",
        help="Show whether any accounts are currently syncing.",
        description="Show whether any accounts are currently syncing.",
    )
    parsers["accounts syncing"] = accounts_syncing
    add_details_flag(accounts_syncing)
    accounts_syncing.set_defaults(func=cmd_accounts_syncing)

    accounts_notices = accounts_sub.add_parser(
        "notices",
        help="List active institution notices.",
        description="List active institution notices.",
    )
    parsers["accounts notices"] = accounts_notices
    add_details_flag(accounts_notices)
    accounts_notices.set_defaults(func=cmd_accounts_notices)

    accounts_page = accounts_sub.add_parser(
        "page",
        help="Show the accounts page payload with account-type summaries.",
        description="Show the accounts page payload with account-type summaries.",
    )
    parsers["accounts page"] = accounts_page
    add_filters_file_flag(accounts_page)
    add_account_filter_flags(accounts_page)
    add_details_flag(accounts_page)
    accounts_page.set_defaults(func=cmd_accounts_page)

    accounts_recent_balances = accounts_sub.add_parser(
        "recent-balances",
        help="Show recent account balance history.",
        description="Show recent account balance history.",
    )
    parsers["accounts recent-balances"] = accounts_recent_balances
    accounts_recent_balances.add_argument("--start-date", help="Start date for recent balances, for example 2026-03-13.")
    add_details_flag(accounts_recent_balances)
    accounts_recent_balances.set_defaults(func=cmd_accounts_recent_balances)

    accounts_filtered = accounts_sub.add_parser(
        "filtered",
        help="List accounts matching account filters.",
        description="List accounts matching account filters.",
    )
    parsers["accounts filtered"] = accounts_filtered
    add_filters_file_flag(accounts_filtered)
    add_account_filter_flags(accounts_filtered)
    add_details_flag(accounts_filtered)
    accounts_filtered.set_defaults(func=cmd_accounts_filtered)

    accounts_aggregate_snapshots = accounts_sub.add_parser(
        "aggregate-snapshots",
        help="Show aggregate balance snapshots over time.",
        description="Show aggregate balance snapshots over time using explicit flags or a JSON file.",
    )
    parsers["accounts aggregate-snapshots"] = accounts_aggregate_snapshots
    add_filters_file_flag(accounts_aggregate_snapshots)
    accounts_aggregate_snapshots.add_argument("--start-date", help="Aggregate snapshot startDate in YYYY-MM-DD format.")
    accounts_aggregate_snapshots.add_argument("--end-date", help="Optional aggregate snapshot endDate in YYYY-MM-DD format.")
    accounts_aggregate_snapshots.add_argument(
        "--use-adaptive-granularity",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Aggregate snapshot useAdaptiveGranularity value.",
    )
    add_account_filter_flags(accounts_aggregate_snapshots)
    add_details_flag(accounts_aggregate_snapshots)
    accounts_aggregate_snapshots.set_defaults(func=cmd_accounts_aggregate_snapshots)

    accounts_display_balance = accounts_sub.add_parser(
        "display-balance",
        help="Show account display balances at one date.",
        description="Show account display balances at one date using explicit flags or a JSON file.",
    )
    parsers["accounts display-balance"] = accounts_display_balance
    add_json_file_flag(accounts_display_balance)
    accounts_display_balance.add_argument("--date", help="Balance date in YYYY-MM-DD format.")
    add_account_filter_flags(accounts_display_balance)
    add_details_flag(accounts_display_balance)
    accounts_display_balance.set_defaults(func=cmd_accounts_display_balance)

    accounts_snapshots_by_account_type = accounts_sub.add_parser(
        "snapshots-by-account-type",
        help="Show account-type balance snapshots over time.",
        description="Show account-type balance snapshots over time using explicit flags or a JSON file.",
    )
    parsers["accounts snapshots-by-account-type"] = accounts_snapshots_by_account_type
    add_json_file_flag(accounts_snapshots_by_account_type)
    accounts_snapshots_by_account_type.add_argument("--start-date", help="Snapshot startDate in YYYY-MM-DD format.")
    accounts_snapshots_by_account_type.add_argument("--timeframe", help="Snapshot timeframe, for example month.")
    add_account_filter_flags(accounts_snapshots_by_account_type)
    add_details_flag(accounts_snapshots_by_account_type)
    accounts_snapshots_by_account_type.set_defaults(func=cmd_accounts_snapshots_by_account_type)

    accounts_filters = accounts_sub.add_parser(
        "filters",
        help="Show account filter data used by the web UI.",
        description="Show account filter data used by the web UI.",
    )
    parsers["accounts filters"] = accounts_filters
    add_details_flag(accounts_filters)
    accounts_filters.set_defaults(func=cmd_accounts_filters)

    accounts_account_types = accounts_sub.add_parser(
        "account-types",
        help="Show available account types and subtypes.",
        description="Show available account types and subtypes.",
    )
    parsers["accounts account-types"] = accounts_account_types
    add_details_flag(accounts_account_types)
    accounts_account_types.set_defaults(func=cmd_accounts_account_types)

    accounts_refresh_status = accounts_sub.add_parser(
        "refresh-status",
        help="Show whether one account can be force refreshed.",
        description="Show whether one account can be force refreshed.",
    )
    parsers["accounts refresh-status"] = accounts_refresh_status
    accounts_refresh_status.add_argument("account_id", help="Account ID.")
    add_details_flag(accounts_refresh_status)
    accounts_refresh_status.set_defaults(func=cmd_accounts_refresh_status)

    accounts_latest_refresh = accounts_sub.add_parser(
        "latest-refresh",
        help="Show the latest household force-refresh operation.",
        description="Show the latest household force-refresh operation.",
    )
    parsers["accounts latest-refresh"] = accounts_latest_refresh
    add_details_flag(accounts_latest_refresh)
    accounts_latest_refresh.set_defaults(func=cmd_accounts_latest_refresh)

    accounts_refresh_operation = accounts_sub.add_parser(
        "refresh-operation",
        help="Show one force-refresh operation by ID.",
        description="Show one force-refresh operation by ID.",
    )
    parsers["accounts refresh-operation"] = accounts_refresh_operation
    accounts_refresh_operation.add_argument("operation_id", help="Force-refresh operation ID.")
    add_details_flag(accounts_refresh_operation)
    accounts_refresh_operation.set_defaults(func=cmd_accounts_refresh_operation)

    accounts_refresh_account = accounts_sub.add_parser(
        "refresh-account",
        help="Request a force refresh for one account.",
        description="Request a force refresh for one account.",
    )
    parsers["accounts refresh-account"] = accounts_refresh_account
    add_json_file_flag(accounts_refresh_account)
    accounts_refresh_account.add_argument("--account-id", help="Account ID to refresh.")
    accounts_refresh_account.add_argument("--source", help="Optional source string sent to the API.")
    add_details_flag(accounts_refresh_account)
    accounts_refresh_account.set_defaults(func=cmd_accounts_refresh_account)

    accounts_refresh_all = accounts_sub.add_parser(
        "refresh-all",
        help="Request a force refresh for all accounts.",
        description="Request a force refresh for all accounts.",
    )
    parsers["accounts refresh-all"] = accounts_refresh_all
    add_json_file_flag(accounts_refresh_all)
    accounts_refresh_all.add_argument("--source", help="Optional source string sent to the API.")
    add_details_flag(accounts_refresh_all)
    accounts_refresh_all.set_defaults(func=cmd_accounts_refresh_all)

    accounts_institution_settings = accounts_sub.add_parser(
        "institution-settings",
        help="Show institution credentials, linked accounts, and subscription state.",
        description="Show institution credentials, linked accounts, and subscription state.",
    )
    parsers["accounts institution-settings"] = accounts_institution_settings
    add_details_flag(accounts_institution_settings)
    accounts_institution_settings.set_defaults(func=cmd_accounts_institution_settings)

    accounts_institutions = accounts_sub.add_parser(
        "institutions",
        help="List institution metadata from the institution service.",
        description="List institution metadata from the institution service.",
    )
    parsers["accounts institutions"] = accounts_institutions
    accounts_institutions.add_argument(
        "--id",
        action="append",
        help="Institution ID to include. Repeat to pass multiple IDs.",
    )
    accounts_institutions.add_argument(
        "--include-logo",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Whether to include base64 logo payloads in the institution service response.",
    )
    add_details_flag(accounts_institutions)
    accounts_institutions.set_defaults(func=cmd_accounts_institutions)

    accounts_institution = accounts_sub.add_parser(
        "institution",
        help="Show one institution metadata record by ID.",
        description="Show one institution metadata record by ID.",
    )
    parsers["accounts institution"] = accounts_institution
    accounts_institution.add_argument("institution_id", help="Institution ID.")
    add_details_flag(accounts_institution)
    accounts_institution.set_defaults(func=cmd_accounts_institution)

    subscription = root_sub.add_parser(
        "subscription",
        help="Subscription, billing, entitlements, gifted-subscription, and referral commands.",
        description="Subscription, billing, entitlements, gifted-subscription, and referral commands.",
    )
    parsers["subscription"] = subscription
    subscription_sub = subscription.add_subparsers(dest="subscription_command", required=True, title="subscription commands")

    subscription_details = subscription_sub.add_parser(
        "details",
        help="Show the smaller subscription details payload.",
        description="Show the smaller subscription details payload.",
    )
    parsers["subscription details"] = subscription_details
    add_details_flag(subscription_details)
    subscription_details.set_defaults(func=cmd_subscription_details)

    subscription_get = subscription_sub.add_parser(
        "get",
        help="Show the full billing/subscription payload with invoices.",
        description="Show the full billing/subscription payload with invoices.",
    )
    parsers["subscription get"] = subscription_get
    add_details_flag(subscription_get)
    subscription_get.set_defaults(func=cmd_subscription_get)

    subscription_modal = subscription_sub.add_parser(
        "modal",
        help="Show the subscription modal payload with optional promo inputs.",
        description="Show the subscription modal payload with optional promo inputs using explicit flags or a JSON file.",
    )
    parsers["subscription modal"] = subscription_modal
    add_json_file_flag(subscription_modal)
    subscription_modal.add_argument("--promo-code", help="Optional promoCode value.")
    subscription_modal.add_argument("--stripe-price-id", help='Optional stripePriceId value. Defaults to "" when omitted.')
    add_details_flag(subscription_modal)
    subscription_modal.set_defaults(func=cmd_subscription_modal)

    subscription_premium_upgrade_plans = subscription_sub.add_parser(
        "premium-upgrade-plans",
        help="Show available premium upgrade plans and referral context.",
        description="Show available premium upgrade plans and referral context using explicit flags or a JSON file.",
    )
    parsers["subscription premium-upgrade-plans"] = subscription_premium_upgrade_plans
    add_json_file_flag(subscription_premium_upgrade_plans)
    subscription_premium_upgrade_plans.add_argument("--promo-code", help="Optional promoCode value.")
    subscription_premium_upgrade_plans.add_argument("--referral-code", help="Optional referralCode value.")
    subscription_premium_upgrade_plans.add_argument("--selected-plan-id", help="Optional selectedPlanId value.")
    add_details_flag(subscription_premium_upgrade_plans)
    subscription_premium_upgrade_plans.set_defaults(func=cmd_subscription_premium_upgrade_plans)

    subscription_trial_status = subscription_sub.add_parser(
        "trial-status",
        help="Show trial eligibility and entitlement state.",
        description="Show trial eligibility and entitlement state.",
    )
    parsers["subscription trial-status"] = subscription_trial_status
    add_details_flag(subscription_trial_status)
    subscription_trial_status.set_defaults(func=cmd_subscription_trial_status)

    subscription_entitlements = subscription_sub.add_parser(
        "entitlements",
        help="Show the current household entitlement list.",
        description="Show the current household entitlement list.",
    )
    parsers["subscription entitlements"] = subscription_entitlements
    add_details_flag(subscription_entitlements)
    subscription_entitlements.set_defaults(func=cmd_subscription_entitlements)

    subscription_feature_entitlement_params = subscription_sub.add_parser(
        "feature-entitlement-params",
        help="Show feature-level entitlement requirements.",
        description="Show feature-level entitlement requirements.",
    )
    parsers["subscription feature-entitlement-params"] = subscription_feature_entitlement_params
    add_details_flag(subscription_feature_entitlement_params)
    subscription_feature_entitlement_params.set_defaults(func=cmd_subscription_feature_entitlement_params)

    subscription_plus_tier_access = subscription_sub.add_parser(
        "plus-tier-access",
        help="Show current plus-tier entitlement access.",
        description="Show current plus-tier entitlement access.",
    )
    parsers["subscription plus-tier-access"] = subscription_plus_tier_access
    add_details_flag(subscription_plus_tier_access)
    subscription_plus_tier_access.set_defaults(func=cmd_subscription_plus_tier_access)

    subscription_gifted_subscriptions = subscription_sub.add_parser(
        "gifted-subscriptions",
        help="Show gifted subscriptions purchased by the household.",
        description="Show gifted subscriptions purchased by the household.",
    )
    parsers["subscription gifted-subscriptions"] = subscription_gifted_subscriptions
    add_details_flag(subscription_gifted_subscriptions)
    subscription_gifted_subscriptions.set_defaults(func=cmd_subscription_gifted_subscriptions)

    subscription_referral_settings = subscription_sub.add_parser(
        "referral-settings",
        help="Show referral statistics and redemption totals.",
        description="Show referral statistics and redemption totals using explicit flags or a JSON file.",
    )
    parsers["subscription referral-settings"] = subscription_referral_settings
    add_json_file_flag(subscription_referral_settings)
    subscription_referral_settings.add_argument(
        "--statistics-start-date",
        help="statisticsStartDate value, for example 2026-01-01T00:00:00.000-06:00.",
    )
    subscription_referral_settings.add_argument(
        "--statistics-end-date",
        help="statisticsEndDate value, for example 2026-12-31T23:59:59.999-06:00.",
    )
    subscription_referral_settings.add_argument("--v1-payout-method", help="v1PayoutMethod value.")
    subscription_referral_settings.add_argument("--v2-payout-method", help="v2PayoutMethod value.")
    add_details_flag(subscription_referral_settings)
    subscription_referral_settings.set_defaults(func=cmd_subscription_referral_settings)

    settings = root_sub.add_parser(
        "settings",
        help="Profile, sidebar, security, notification, business-entity, and activity commands.",
        description="Profile, sidebar, security, notification, business-entity, and activity commands.",
    )
    parsers["settings"] = settings
    settings_sub = settings.add_subparsers(dest="settings_command", required=True, title="settings commands")

    settings_user_profile_flags = settings_sub.add_parser(
        "user-profile-flags",
        help="Show user-profile flags and walkthrough state.",
        description="Show user-profile flags and walkthrough state.",
    )
    parsers["settings user-profile-flags"] = settings_user_profile_flags
    add_details_flag(settings_user_profile_flags)
    settings_user_profile_flags.set_defaults(func=cmd_settings_user_profile_flags)

    settings_dashboard_config = settings_sub.add_parser(
        "dashboard-config",
        help="Show saved web/mobile dashboard layout config.",
        description="Show saved web/mobile dashboard layout config.",
    )
    parsers["settings dashboard-config"] = settings_dashboard_config
    add_details_flag(settings_dashboard_config)
    settings_dashboard_config.set_defaults(func=cmd_settings_dashboard_config)

    settings_sidebar_data = settings_sub.add_parser(
        "sidebar-data",
        help="Show sidebar/profile/subscription summary data.",
        description="Show sidebar/profile/subscription summary data.",
    )
    parsers["settings sidebar-data"] = settings_sidebar_data
    settings_sidebar_data.add_argument("--promo-code", help="Optional promoCode value.")
    add_details_flag(settings_sidebar_data)
    settings_sidebar_data.set_defaults(func=cmd_settings_sidebar_data)

    settings_household_member_settings = settings_sub.add_parser(
        "household-member-settings",
        help="Show household member, invite, and access-grant settings.",
        description="Show household member, invite, and access-grant settings.",
    )
    parsers["settings household-member-settings"] = settings_household_member_settings
    add_details_flag(settings_household_member_settings)
    settings_household_member_settings.set_defaults(func=cmd_settings_household_member_settings)

    settings_security = settings_sub.add_parser(
        "security",
        help="Show security settings, MFA state, and linked auth providers.",
        description="Show security settings, MFA state, and linked auth providers.",
    )
    parsers["settings security"] = settings_security
    add_details_flag(settings_security)
    settings_security.set_defaults(func=cmd_settings_security)

    settings_notification_preferences = settings_sub.add_parser(
        "notification-preferences",
        help="Show notification preference rows.",
        description="Show notification preference rows.",
    )
    parsers["settings notification-preferences"] = settings_notification_preferences
    add_details_flag(settings_notification_preferences)
    settings_notification_preferences.set_defaults(func=cmd_settings_notification_preferences)

    settings_review_summary_by_user = settings_sub.add_parser(
        "review-summary-by-user",
        help="Show needs-review counts grouped by user.",
        description="Show needs-review counts grouped by user.",
    )
    parsers["settings review-summary-by-user"] = settings_review_summary_by_user
    add_details_flag(settings_review_summary_by_user)
    settings_review_summary_by_user.set_defaults(func=cmd_settings_review_summary_by_user)

    settings_business_entities_banner_profile = settings_sub.add_parser(
        "business-entities-banner-profile",
        help="Show business-entity banner profile state.",
        description="Show business-entity banner profile state.",
    )
    parsers["settings business-entities-banner-profile"] = settings_business_entities_banner_profile
    add_details_flag(settings_business_entities_banner_profile)
    settings_business_entities_banner_profile.set_defaults(func=cmd_settings_business_entities_banner_profile)

    settings_business_entities = settings_sub.add_parser(
        "business-entities",
        help="Show configured business entities.",
        description="Show configured business entities.",
    )
    parsers["settings business-entities"] = settings_business_entities
    add_details_flag(settings_business_entities)
    settings_business_entities.set_defaults(func=cmd_settings_business_entities)

    settings_has_activity = settings_sub.add_parser(
        "has-activity",
        help="Show whether the user has new activity.",
        description="Show whether the user has new activity.",
    )
    parsers["settings has-activity"] = settings_has_activity
    add_details_flag(settings_has_activity)
    settings_has_activity.set_defaults(func=cmd_settings_has_activity)

    settings_oldest_synced_snapshot = settings_sub.add_parser(
        "oldest-deletable-synced-snapshot-date",
        help="Show the oldest deletable synced snapshot date.",
        description="Show the oldest deletable synced snapshot date.",
    )
    parsers["settings oldest-deletable-synced-snapshot-date"] = settings_oldest_synced_snapshot
    add_details_flag(settings_oldest_synced_snapshot)
    settings_oldest_synced_snapshot.set_defaults(func=cmd_settings_oldest_deletable_synced_snapshot_date)

    settings_oldest_deletable_transaction = settings_sub.add_parser(
        "oldest-deletable-transaction-date",
        help="Show the oldest deletable transaction date.",
        description="Show the oldest deletable transaction date.",
    )
    parsers["settings oldest-deletable-transaction-date"] = settings_oldest_deletable_transaction
    settings_oldest_deletable_transaction.add_argument(
        "--include-synced",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Whether synced transactions should be included.",
    )
    settings_oldest_deletable_transaction.add_argument(
        "--include-uploaded",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Whether uploaded transactions should be included.",
    )
    settings_oldest_deletable_transaction.add_argument(
        "--include-manual",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Whether manual transactions should be included.",
    )
    add_details_flag(settings_oldest_deletable_transaction)
    settings_oldest_deletable_transaction.set_defaults(func=cmd_settings_oldest_deletable_transaction_date)

    planning = root_sub.add_parser(
        "planning",
        help="Budget and joint-planning commands.",
        description="Budget and joint-planning commands.",
    )
    parsers["planning"] = planning
    planning_sub = planning.add_subparsers(dest="planning_command", required=True, title="planning commands")

    planning_budget_data = planning_sub.add_parser(
        "budget-data",
        help="Show budget data for a date range.",
        description="Show budget data for a date range using explicit flags or a JSON file.",
    )
    parsers["planning budget-data"] = planning_budget_data
    add_json_file_flag(planning_budget_data)
    planning_budget_data.add_argument("--start-date", help="Budget query startDate in YYYY-MM-DD format.")
    planning_budget_data.add_argument("--end-date", help="Budget query endDate in YYYY-MM-DD format.")
    add_details_flag(planning_budget_data)
    planning_budget_data.set_defaults(func=cmd_planning_budget_data)

    planning_joint_data = planning_sub.add_parser(
        "joint-data",
        help="Show joint planning data for a date range.",
        description="Show joint planning data for a date range using explicit flags or a JSON file.",
    )
    parsers["planning joint-data"] = planning_joint_data
    add_json_file_flag(planning_joint_data)
    planning_joint_data.add_argument("--start-date", help="Joint planning query startDate in YYYY-MM-DD format.")
    planning_joint_data.add_argument("--end-date", help="Joint planning query endDate in YYYY-MM-DD format.")
    add_details_flag(planning_joint_data)
    planning_joint_data.set_defaults(func=cmd_planning_joint_data)

    goals = root_sub.add_parser(
        "goals",
        help="Savings-goal and goal-dashboard commands.",
        description="Savings-goal and goal-dashboard commands.",
    )
    parsers["goals"] = goals
    goals_sub = goals.add_subparsers(dest="goals_command", required=True, title="goal commands")

    goals_savings_goals = goals_sub.add_parser(
        "savings-goals",
        help="List savings goals.",
        description="List savings goals.",
    )
    parsers["goals savings-goals"] = goals_savings_goals
    add_details_flag(goals_savings_goals)
    goals_savings_goals.set_defaults(func=cmd_goals_savings_goals)

    goals_savings_goals_balances = goals_sub.add_parser(
        "savings-goals-balances",
        help="Show savings goals with this-month balances.",
        description="Show savings goals with this-month balances.",
    )
    parsers["goals savings-goals-balances"] = goals_savings_goals_balances
    add_details_flag(goals_savings_goals_balances)
    goals_savings_goals_balances.set_defaults(func=cmd_goals_savings_goals_with_balances)

    goals_savings_goal_account = goals_sub.add_parser(
        "savings-goal-account",
        help="Show one goal-linked account by ID.",
        description="Show one goal-linked account by ID.",
    )
    parsers["goals savings-goal-account"] = goals_savings_goal_account
    goals_savings_goal_account.add_argument("account_id", help="Account ID.")
    add_details_flag(goals_savings_goal_account)
    goals_savings_goal_account.set_defaults(func=cmd_goals_savings_goal_account)

    goals_dashboard = goals_sub.add_parser(
        "dashboard-card",
        help="Show the goals dashboard card payload.",
        description="Show the goals dashboard card payload.",
    )
    parsers["goals dashboard-card"] = goals_dashboard
    add_details_flag(goals_dashboard)
    goals_dashboard.set_defaults(func=cmd_goals_dashboard_card)

    goals_legacy_migration = goals_sub.add_parser(
        "legacy-migration",
        help="Show legacy-goals migration state and debt accounts.",
        description="Show legacy-goals migration state and debt accounts.",
    )
    parsers["goals legacy-migration"] = goals_legacy_migration
    add_details_flag(goals_legacy_migration)
    goals_legacy_migration.set_defaults(func=cmd_goals_legacy_migration)

    recurring = root_sub.add_parser(
        "recurring",
        help="Recurring stream, aggregate, dashboard, and banner commands.",
        description="Recurring stream, aggregate, dashboard, and banner commands.",
    )
    parsers["recurring"] = recurring
    recurring_sub = recurring.add_subparsers(dest="recurring_command", required=True, title="recurring commands")

    recurring_streams = recurring_sub.add_parser(
        "streams",
        help="List recurring streams.",
        description="List recurring streams.",
    )
    parsers["recurring streams"] = recurring_streams
    recurring_streams.add_argument(
        "--include-liabilities",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Whether to include liability streams.",
    )
    add_details_flag(recurring_streams)
    recurring_streams.set_defaults(func=cmd_recurring_streams)

    recurring_aggregated = recurring_sub.add_parser(
        "aggregated-items",
        help="Show aggregated recurring items for a date range.",
        description="Show aggregated recurring items for a date range using explicit flags or JSON filters.",
    )
    parsers["recurring aggregated-items"] = recurring_aggregated
    add_json_file_flag(recurring_aggregated)
    add_filters_file_flag(recurring_aggregated)
    recurring_aggregated.add_argument("--start-date", help="Recurring aggregation startDate in YYYY-MM-DD format.")
    recurring_aggregated.add_argument("--end-date", help="Recurring aggregation endDate in YYYY-MM-DD format.")
    add_recurring_filter_flags(recurring_aggregated)
    add_details_flag(recurring_aggregated)
    recurring_aggregated.set_defaults(func=cmd_recurring_aggregated_items)

    recurring_dashboard = recurring_sub.add_parser(
        "dashboard-upcoming",
        help="Show upcoming recurring dashboard items for a date range.",
        description="Show upcoming recurring dashboard items for a date range using explicit flags or JSON filters.",
    )
    parsers["recurring dashboard-upcoming"] = recurring_dashboard
    add_json_file_flag(recurring_dashboard)
    add_filters_file_flag(recurring_dashboard)
    recurring_dashboard.add_argument("--start-date", help="Recurring dashboard startDate in YYYY-MM-DD format.")
    recurring_dashboard.add_argument("--end-date", help="Recurring dashboard endDate in YYYY-MM-DD format.")
    recurring_dashboard.add_argument(
        "--include-liabilities",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Whether to include liabilities in the dashboard query.",
    )
    add_recurring_filter_flags(recurring_dashboard)
    add_details_flag(recurring_dashboard)
    recurring_dashboard.set_defaults(func=cmd_recurring_dashboard_upcoming)

    recurring_paused = recurring_sub.add_parser(
        "paused-banner",
        help="Show recurring paused-banner state.",
        description="Show recurring paused-banner state.",
    )
    parsers["recurring paused-banner"] = recurring_paused
    add_details_flag(recurring_paused)
    recurring_paused.set_defaults(func=cmd_recurring_paused_banner)

    investments = root_sub.add_parser(
        "investments",
        help="Investment accounts, dashboard card, portfolio, and security-history commands.",
        description="Investment accounts, dashboard card, portfolio, and security-history commands.",
    )
    parsers["investments"] = investments
    investments_sub = investments.add_subparsers(dest="investments_command", required=True, title="investment commands")

    investments_accounts = investments_sub.add_parser(
        "accounts",
        help="List investment accounts.",
        description="List investment accounts.",
    )
    parsers["investments accounts"] = investments_accounts
    add_details_flag(investments_accounts)
    investments_accounts.set_defaults(func=cmd_investments_accounts)

    investments_dashboard = investments_sub.add_parser(
        "dashboard-card",
        help="Show the investments dashboard card payload.",
        description="Show the investments dashboard card payload.",
    )
    parsers["investments dashboard-card"] = investments_dashboard
    add_details_flag(investments_dashboard)
    investments_dashboard.set_defaults(func=cmd_investments_dashboard_card)

    investments_portfolio = investments_sub.add_parser(
        "portfolio",
        help="Show portfolio performance and aggregate holdings.",
        description="Show portfolio performance and aggregate holdings using explicit flags or a JSON file.",
    )
    parsers["investments portfolio"] = investments_portfolio
    add_json_file_flag(investments_portfolio)
    investments_portfolio.add_argument("--start-date", help="PortfolioInput startDate in YYYY-MM-DD format.")
    investments_portfolio.add_argument("--end-date", help="PortfolioInput endDate in YYYY-MM-DD format.")
    add_details_flag(investments_portfolio)
    investments_portfolio.set_defaults(func=cmd_investments_portfolio)

    investments_security_history = investments_sub.add_parser(
        "security-history",
        help="Show historical performance for one or more securities.",
        description="Show historical performance for one or more securities using explicit flags or a JSON file.",
    )
    parsers["investments security-history"] = investments_security_history
    add_json_file_flag(investments_security_history)
    investments_security_history.add_argument(
        "--security-id",
        action="append",
        help="Security ID. Repeat to request multiple securities.",
    )
    investments_security_history.add_argument("--start-date", help="History startDate in YYYY-MM-DD format.")
    investments_security_history.add_argument("--end-date", help="History endDate in YYYY-MM-DD format.")
    add_details_flag(investments_security_history)
    investments_security_history.set_defaults(func=cmd_investments_security_history)

    transactions = root_sub.add_parser(
        "transactions",
        help="Transaction listing, lookup, filters, create, update, delete, tags, and categories.",
        description="Transaction listing, lookup, filters, create, update, delete, tags, and categories.",
    )
    parsers["transactions"] = transactions
    transactions_sub = transactions.add_subparsers(dest="transactions_command", required=True, title="transaction commands")

    tx_list = transactions_sub.add_parser(
        "list",
        help="List transactions with optional filters and pagination.",
        description="List transactions with optional filters and pagination.",
    )
    parsers["transactions list"] = tx_list
    tx_list.add_argument("--offset", type=int, help="Result offset to request.")
    tx_list.add_argument("--limit", type=int, default=25, help="Maximum number of transactions to return.")
    tx_list.add_argument("--order-by", default="date", help="Sort field sent to the API. Default: date.")
    add_filters_file_flag(tx_list)
    add_transaction_filter_flags(tx_list)
    add_details_flag(tx_list)
    tx_list.set_defaults(func=cmd_transactions_list)

    tx_get = transactions_sub.add_parser(
        "get",
        help="Show one transaction by ID.",
        description="Show one transaction by ID.",
    )
    parsers["transactions get"] = tx_get
    tx_get.add_argument("transaction_id", help="Transaction ID.")
    tx_get.add_argument(
        "--no-redirect-posted",
        action="store_true",
        help="Disable the redirectPosted behavior used by the drawer query.",
    )
    add_details_flag(tx_get)
    tx_get.set_defaults(func=cmd_transactions_get)

    tx_filters = transactions_sub.add_parser(
        "filters",
        help="Fetch transaction filter option data.",
        description="Fetch transaction filter option data used by the transactions UI.",
    )
    parsers["transactions filters"] = tx_filters
    tx_filters.add_argument("--search", help="Optional search string.")
    tx_filters.add_argument(
        "--include-id",
        action="append",
        help="Include a specific entity ID. Repeat to pass multiple IDs.",
    )
    add_details_flag(tx_filters)
    tx_filters.set_defaults(func=cmd_transactions_filters)

    tx_filters_metadata = transactions_sub.add_parser(
        "filters-metadata",
        help="Fetch metadata for a transaction filters object.",
        description="Fetch metadata for a transaction filters object.",
    )
    parsers["transactions filters-metadata"] = tx_filters_metadata
    add_filters_file_flag(tx_filters_metadata)
    add_transaction_filter_flags(tx_filters_metadata)
    add_details_flag(tx_filters_metadata)
    tx_filters_metadata.set_defaults(func=cmd_transactions_filters_metadata)

    tx_create = transactions_sub.add_parser(
        "create",
        help="Create a manual transaction using flags or a JSON file.",
        description="Create a manual transaction using explicit flags or a JSON file.",
    )
    parsers["transactions create"] = tx_create
    add_json_file_flag(tx_create)
    tx_create.add_argument("-d", "--date", help="Transaction date, for example 2026-04-15.")
    tx_create.add_argument("-a", "--amount", type=float, help="Transaction amount.")
    tx_create.add_argument("-m", "--merchant-name", help="Merchant name.")
    tx_create.add_argument("--account-id", help="Account ID.")
    tx_create.add_argument("--category-id", help="Category ID.")
    tx_create.add_argument("-n", "--notes", help="Optional notes.")
    tx_create.add_argument("--owner-user-id", help="Owner user ID.")
    tx_create.add_argument(
        "--should-update-balance",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Whether Monarch should update the account balance for this manual transaction.",
    )
    add_details_flag(tx_create)
    tx_create.set_defaults(func=cmd_transactions_create)

    tx_update = transactions_sub.add_parser(
        "update",
        help="Update one transaction using flags or a JSON file.",
        description="Update one transaction using explicit flags or a JSON file.",
    )
    parsers["transactions update"] = tx_update
    add_json_file_flag(tx_update)
    tx_update.add_argument("-i", "--transaction-id", help="Transaction ID to update.")
    tx_update.add_argument("-d", "--date", help="Updated transaction date.")
    tx_update.add_argument("-a", "--amount", type=float, help="Updated transaction amount.")
    tx_update.add_argument("-m", "--merchant-name", help="Updated merchant name.")
    tx_update.add_argument("--category-id", help="Updated category ID.")
    tx_update.add_argument("-n", "--notes", help="Updated notes.")
    tx_update.add_argument("--owner-user-id", help="Updated owner user ID.")
    tx_update.add_argument("--business-entity-id", help="Updated business entity ID.")
    tx_update.add_argument("--hide-from-reports", action="store_true", help="Hide the transaction from reports.")
    tx_update.add_argument("--show-in-reports", action="store_true", help="Show the transaction in reports.")
    add_details_flag(tx_update)
    tx_update.set_defaults(func=cmd_transactions_update)

    tx_delete = transactions_sub.add_parser(
        "delete",
        help="Delete one transaction by ID.",
        description="Delete one transaction by ID.",
    )
    parsers["transactions delete"] = tx_delete
    tx_delete.add_argument("transaction_id", help="Transaction ID.")
    add_details_flag(tx_delete)
    tx_delete.set_defaults(func=cmd_transactions_delete)

    tx_set_tags = transactions_sub.add_parser(
        "set-tags",
        help="Replace the tags for one transaction.",
        description="Replace the tags for one transaction.",
    )
    parsers["transactions set-tags"] = tx_set_tags
    tx_set_tags.add_argument("transaction_id", help="Transaction ID.")
    tx_set_tags.add_argument(
        "--tag-id",
        action="append",
        required=True,
        help="Tag ID to apply. Repeat to pass multiple tag IDs.",
    )
    add_details_flag(tx_set_tags)
    tx_set_tags.set_defaults(func=cmd_transactions_set_tags)

    tx_tags = transactions_sub.add_parser(
        "tags",
        help="List household transaction tags.",
        description="List household transaction tags.",
    )
    parsers["transactions tags"] = tx_tags
    tx_tags.add_argument("--search", help="Optional search string.")
    tx_tags.add_argument("--limit", type=int, help="Maximum number of tags to return.")
    tx_tags.add_argument(
        "--bulk-params-json-file",
        help="Path to a JSON file containing the bulkParams object.",
    )
    tx_tags.add_argument(
        "--include-transaction-count",
        action="store_true",
        help="Include per-tag transaction counts when supported.",
    )
    add_details_flag(tx_tags)
    tx_tags.set_defaults(func=cmd_transactions_tags)

    tx_categories = transactions_sub.add_parser(
        "categories",
        help="List categories and category groups.",
        description="List categories and category groups.",
    )
    parsers["transactions categories"] = tx_categories
    tx_categories.add_argument(
        "--include-system-disabled-categories",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Whether to include system-disabled categories.",
    )
    add_details_flag(tx_categories)
    tx_categories.set_defaults(func=cmd_transactions_categories)

    merchants = root_sub.add_parser(
        "merchants",
        help="Merchant search, household merchant listing, recommendations, and updates.",
        description="Merchant search, household merchant listing, recommendations, and updates.",
    )
    parsers["merchants"] = merchants
    merchants_sub = merchants.add_subparsers(dest="merchants_command", required=True, title="merchant commands")

    merchants_search = merchants_sub.add_parser(
        "search",
        help="Search merchants by name.",
        description="Search merchants by name.",
    )
    parsers["merchants search"] = merchants_search
    merchants_search.add_argument("--search", help="Optional search string.")
    merchants_search.add_argument("--limit", type=int, default=20, help="Maximum number of merchants to return.")
    merchants_search.add_argument(
        "--include-id",
        action="append",
        help="Merchant ID to force-include in the response. Repeat to pass multiple IDs.",
    )
    add_details_flag(merchants_search)
    merchants_search.set_defaults(func=cmd_merchants_search)

    merchants_household = merchants_sub.add_parser(
        "household",
        help="List household merchants.",
        description="List household merchants.",
    )
    parsers["merchants household"] = merchants_household
    merchants_household.add_argument("--offset", type=int, default=0, help="Result offset.")
    merchants_household.add_argument("--limit", type=int, default=50, help="Maximum number of merchants to return.")
    merchants_household.add_argument(
        "--order-by",
        default="TRANSACTION_COUNT",
        help="Ordering value sent to the API. Default: TRANSACTION_COUNT.",
    )
    merchants_household.add_argument("--search", help="Optional search string.")
    add_details_flag(merchants_household)
    merchants_household.set_defaults(func=cmd_merchants_household)

    merchants_recommended = merchants_sub.add_parser(
        "recommended",
        help="Show recommended merchants for a transaction.",
        description="Show recommended merchants for a transaction.",
    )
    parsers["merchants recommended"] = merchants_recommended
    merchants_recommended.add_argument("transaction_id", help="Transaction ID.")
    add_details_flag(merchants_recommended)
    merchants_recommended.set_defaults(func=cmd_merchants_recommended)

    merchants_update = merchants_sub.add_parser(
        "update",
        help="Update one merchant using flags or a JSON file.",
        description="Update one merchant using explicit flags or a JSON file.",
    )
    parsers["merchants update"] = merchants_update
    add_json_file_flag(merchants_update)
    merchants_update.add_argument("--merchant-id", help="Merchant ID to update.")
    merchants_update.add_argument("--name", help="Updated merchant name.")
    merchants_update.add_argument("--recurrence-amount", type=float, help="Recurring amount.")
    merchants_update.add_argument("--recurring", action="store_true", help="Mark the merchant as recurring.")
    merchants_update.add_argument("--not-recurring", action="store_true", help="Mark the merchant as not recurring.")
    merchants_update.add_argument(
        "--recurrence-is-active",
        action="store_true",
        help="Mark recurring detection as active.",
    )
    merchants_update.add_argument(
        "--recurrence-is-inactive",
        action="store_true",
        help="Mark recurring detection as inactive.",
    )
    add_details_flag(merchants_update)
    merchants_update.set_defaults(func=cmd_merchants_update)

    attachments = root_sub.add_parser(
        "attachments",
        help="Attachment upload info, add, fetch, and delete.",
        description="Attachment upload info, add, fetch, and delete.",
    )
    parsers["attachments"] = attachments
    attachments_sub = attachments.add_subparsers(dest="attachments_command", required=True, title="attachment commands")

    attachments_upload_info = attachments_sub.add_parser(
        "upload-info",
        help="Get attachment upload metadata for a transaction.",
        description="Get attachment upload metadata for a transaction.",
    )
    parsers["attachments upload-info"] = attachments_upload_info
    attachments_upload_info.add_argument("transaction_id", help="Transaction ID.")
    add_details_flag(attachments_upload_info)
    attachments_upload_info.set_defaults(func=cmd_attachments_upload_info)

    attachments_add = attachments_sub.add_parser(
        "add",
        help="Add an attachment using explicit flags or a JSON file payload.",
        description="Add an attachment using explicit flags or a JSON file payload.",
    )
    parsers["attachments add"] = attachments_add
    add_json_file_flag(attachments_add)
    attachments_add.add_argument("--transaction-id", help="Transaction ID that should receive the attachment.")
    attachments_add.add_argument("--filename", help="Final attachment filename.")
    attachments_add.add_argument("--public-id", help="Uploaded storage public ID.")
    attachments_add.add_argument("--extension", help="File extension without the dot, for example pdf or jpg.")
    attachments_add.add_argument("--size-bytes", type=int, help="Attachment size in bytes.")
    add_details_flag(attachments_add)
    attachments_add.set_defaults(func=cmd_attachments_add)

    attachments_get = attachments_sub.add_parser(
        "get",
        help="Show one attachment by ID.",
        description="Show one attachment by ID.",
    )
    parsers["attachments get"] = attachments_get
    attachments_get.add_argument("attachment_id", help="Attachment ID.")
    add_details_flag(attachments_get)
    attachments_get.set_defaults(func=cmd_attachments_get)

    attachments_delete = attachments_sub.add_parser(
        "delete",
        help="Delete one attachment by ID.",
        description="Delete one attachment by ID.",
    )
    parsers["attachments delete"] = attachments_delete
    attachments_delete.add_argument("attachment_id", help="Attachment ID.")
    add_details_flag(attachments_delete)
    attachments_delete.set_defaults(func=cmd_attachments_delete)

    rules = root_sub.add_parser(
        "rules",
        help="Transaction rule commands.",
        description="Transaction rule commands.",
    )
    parsers["rules"] = rules
    rules_sub = rules.add_subparsers(dest="rules_command", required=True, title="rule commands")

    rules_list = rules_sub.add_parser(
        "list",
        help="List transaction rules.",
        description="List transaction rules.",
    )
    parsers["rules list"] = rules_list
    add_details_flag(rules_list)
    rules_list.set_defaults(func=cmd_rules_list)

    rules_create = rules_sub.add_parser(
        "create",
        help="Create one transaction rule using explicit flags or a JSON file.",
        description="Create one transaction rule using explicit flags or a JSON file.",
    )
    parsers["rules create"] = rules_create
    add_json_file_flag(rules_create)
    add_rule_input_flags(rules_create, include_rule_id=False)
    add_details_flag(rules_create)
    rules_create.set_defaults(func=cmd_rules_create)

    rules_update = rules_sub.add_parser(
        "update",
        help="Update one transaction rule using explicit flags or a JSON file.",
        description="Update one transaction rule using explicit flags or a JSON file.",
    )
    parsers["rules update"] = rules_update
    add_json_file_flag(rules_update)
    add_rule_input_flags(rules_update, include_rule_id=True)
    add_details_flag(rules_update)
    rules_update.set_defaults(func=cmd_rules_update)

    rules_delete = rules_sub.add_parser(
        "delete",
        help="Delete one transaction rule by ID.",
        description="Delete one transaction rule by ID.",
    )
    parsers["rules delete"] = rules_delete
    rules_delete.add_argument("rule_id", help="Rule ID.")
    add_details_flag(rules_delete)
    rules_delete.set_defaults(func=cmd_rules_delete)

    rules_preview = rules_sub.add_parser(
        "preview",
        help="Preview a transaction rule against matching transactions.",
        description="Preview a transaction rule against matching transactions.",
    )
    parsers["rules preview"] = rules_preview
    add_json_file_flag(rules_preview)
    add_rule_input_flags(rules_preview, include_rule_id=False)
    rules_preview.add_argument("--offset", type=int, help="Preview result offset.")
    add_details_flag(rules_preview)
    rules_preview.set_defaults(func=cmd_rules_preview)

    rules_update_order = rules_sub.add_parser(
        "update-order",
        help="Update a transaction rule's order.",
        description="Update a transaction rule's order.",
    )
    parsers["rules update-order"] = rules_update_order
    rules_update_order.add_argument("rule_id", help="Rule ID.")
    rules_update_order.add_argument("order", type=int, help="New rule order.")
    add_details_flag(rules_update_order)
    rules_update_order.set_defaults(func=cmd_rules_update_order)

    rules_delete_all = rules_sub.add_parser(
        "delete-all",
        help="Delete all transaction rules.",
        description="Delete all transaction rules.",
    )
    parsers["rules delete-all"] = rules_delete_all
    rules_delete_all.add_argument(
        "--yes",
        action="store_true",
        help="Confirm deletion of all transaction rules.",
    )
    add_details_flag(rules_delete_all)
    rules_delete_all.set_defaults(func=cmd_rules_delete_all)

    reports = root_sub.add_parser(
        "reports",
        help="Cash-flow and reports commands.",
        description="Cash-flow and reports commands.",
    )
    parsers["reports"] = reports
    reports_sub = reports.add_subparsers(dest="reports_command", required=True, title="report commands")

    reports_dashboard = reports_sub.add_parser(
        "cash-flow-dashboard",
        help="Show cash-flow dashboard totals by day.",
        description="Show cash-flow dashboard totals by day.",
    )
    parsers["reports cash-flow-dashboard"] = reports_dashboard
    add_filters_file_flag(reports_dashboard)
    add_transaction_filter_flags(reports_dashboard)
    add_details_flag(reports_dashboard)
    reports_dashboard.set_defaults(func=cmd_reports_cash_flow_dashboard)

    reports_entities = reports_sub.add_parser(
        "cash-flow-entities",
        help="Show cash-flow aggregates by category, group, and merchant.",
        description="Show cash-flow aggregates by category, group, and merchant.",
    )
    parsers["reports cash-flow-entities"] = reports_entities
    add_filters_file_flag(reports_entities)
    add_transaction_filter_flags(reports_entities)
    add_details_flag(reports_entities)
    reports_entities.set_defaults(func=cmd_reports_cash_flow_entities)

    reports_timeframes = reports_sub.add_parser(
        "cash-flow-timeframes",
        help="Show cash-flow aggregates by year, month, and quarter.",
        description="Show cash-flow aggregates by year, month, and quarter.",
    )
    parsers["reports cash-flow-timeframes"] = reports_timeframes
    add_filters_file_flag(reports_timeframes)
    add_transaction_filter_flags(reports_timeframes)
    add_details_flag(reports_timeframes)
    reports_timeframes.set_defaults(func=cmd_reports_cash_flow_timeframes)

    reports_data = reports_sub.add_parser(
        "data",
        help="Show the general reports data payload.",
        description="Show the general reports data payload.",
    )
    parsers["reports data"] = reports_data
    add_filters_file_flag(reports_data)
    add_transaction_filter_flags(reports_data)
    reports_data.add_argument(
        "--group-by",
        action="append",
        help="Reports groupBy entity, for example category or category_group. Repeat to pass multiple values.",
    )
    reports_data.add_argument(
        "--group-by-timeframe",
        help="Reports timeframe grouping, for example month or quarter.",
    )
    reports_data.add_argument("--sort-by", help="Reports sort value, for example sum_expense.")
    reports_data.add_argument("--include-category", action="store_true", help="Include category fields in report groups.")
    reports_data.add_argument("--include-category-group", action="store_true", help="Include category-group fields in report groups.")
    reports_data.add_argument("--include-merchant", action="store_true", help="Include merchant fields in report groups.")
    reports_data.add_argument("--include-business-entity", action="store_true", help="Include business-entity fields in report groups.")
    reports_data.add_argument("--include-budget-variability", action="store_true", help="Include budget-variability fields in report groups.")
    reports_data.add_argument(
        "--fill-empty-values",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Whether the reports query should request fillEmptyValues.",
    )
    add_details_flag(reports_data)
    reports_data.set_defaults(func=cmd_reports_data)

    retail_sync = root_sub.add_parser(
        "retail-sync",
        help="Retail sync settings, lookup, list, mutation, and matching commands.",
        description="Retail sync settings, lookup, list, mutation, and matching commands.",
    )
    parsers["retail-sync"] = retail_sync
    retail_sub = retail_sync.add_subparsers(dest="retail_sync_command", required=True, title="retail sync commands")

    retail_settings = retail_sub.add_parser(
        "settings",
        help="Show retail sync extension settings.",
        description="Show retail sync extension settings.",
    )
    parsers["retail-sync settings"] = retail_settings
    add_details_flag(retail_settings)
    retail_settings.set_defaults(func=cmd_retail_sync_settings)

    retail_get = retail_sub.add_parser(
        "get",
        help="Show one retail sync record by ID.",
        description="Show one retail sync record by ID.",
    )
    parsers["retail-sync get"] = retail_get
    retail_get.add_argument("sync_id", help="Retail sync ID.")
    add_details_flag(retail_get)
    retail_get.set_defaults(func=cmd_retail_sync_get)

    retail_list = retail_sub.add_parser(
        "list",
        help="List retail sync records.",
        description="List retail sync records.",
    )
    parsers["retail-sync list"] = retail_list
    add_filters_file_flag(retail_list)
    retail_list.add_argument(
        "--status",
        help="Retail sync status filter, for example pending_matches or completed.",
    )
    retail_list.add_argument(
        "--vendor",
        help="Retail sync vendor filter, for example user_import.",
    )
    retail_list.add_argument("--offset", type=int, default=0, help="Result offset.")
    retail_list.add_argument("--limit", type=int, default=50, help="Maximum number of retail syncs to return.")
    retail_list.add_argument(
        "--no-total-count",
        action="store_true",
        help="Do not request totalCount in the response.",
    )
    add_details_flag(retail_list)
    retail_list.set_defaults(func=cmd_retail_sync_list)

    retail_create = retail_sub.add_parser(
        "create",
        help="Create one retail sync record from explicit flags or a JSON file.",
        description="Create one retail sync record from explicit flags or a JSON file.",
    )
    parsers["retail-sync create"] = retail_create
    add_json_file_flag(retail_create)
    retail_create.add_argument("--vendor", help="Retail sync vendor enum value, for example USER_IMPORT.")
    retail_create.add_argument(
        "--is-backfill",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Whether the new retail sync should be created as a backfill.",
    )
    add_details_flag(retail_create)
    retail_create.set_defaults(func=cmd_retail_sync_create)

    retail_create_bulk = retail_sub.add_parser(
        "create-bulk",
        help="Create retail sync records in bulk from explicit flags or a JSON file.",
        description="Create retail sync records in bulk from explicit flags or a JSON file.",
    )
    parsers["retail-sync create-bulk"] = retail_create_bulk
    add_json_file_flag(retail_create_bulk)
    retail_create_bulk.add_argument("--count", type=int, help="Number of retail sync records to create.")
    add_details_flag(retail_create_bulk)
    retail_create_bulk.set_defaults(func=cmd_retail_sync_create_bulk)

    retail_start = retail_sub.add_parser(
        "start",
        help="Start a retail sync by ID.",
        description="Start a retail sync by ID.",
    )
    parsers["retail-sync start"] = retail_start
    retail_start.add_argument("sync_id", help="Retail sync ID.")
    add_details_flag(retail_start)
    retail_start.set_defaults(func=cmd_retail_sync_start)

    retail_complete = retail_sub.add_parser(
        "complete",
        help="Complete a retail sync by ID.",
        description="Complete a retail sync by ID.",
    )
    parsers["retail-sync complete"] = retail_complete
    retail_complete.add_argument("sync_id", help="Retail sync ID.")
    add_details_flag(retail_complete)
    retail_complete.set_defaults(func=cmd_retail_sync_complete)

    retail_delete = retail_sub.add_parser(
        "delete",
        help="Delete an unmatched retail sync by ID.",
        description="Delete an unmatched retail sync by ID.",
    )
    parsers["retail-sync delete"] = retail_delete
    retail_delete.add_argument("sync_id", help="Retail sync ID.")
    add_details_flag(retail_delete)
    retail_delete.set_defaults(func=cmd_retail_sync_delete)

    retail_match = retail_sub.add_parser(
        "match",
        help="Match a retail transaction to a Monarch transaction.",
        description="Match a retail transaction to a Monarch transaction.",
    )
    parsers["retail-sync match"] = retail_match
    retail_match.add_argument("retail_transaction_id", help="Retail transaction ID.")
    retail_match.add_argument("transaction_id", help="Monarch transaction ID.")
    add_details_flag(retail_match)
    retail_match.set_defaults(func=cmd_retail_sync_match)

    retail_unmatch = retail_sub.add_parser(
        "unmatch",
        help="Unmatch a retail transaction.",
        description="Unmatch a retail transaction.",
    )
    parsers["retail-sync unmatch"] = retail_unmatch
    retail_unmatch.add_argument("retail_transaction_id", help="Retail transaction ID.")
    add_details_flag(retail_unmatch)
    retail_unmatch.set_defaults(func=cmd_retail_sync_unmatch)

    retail_update_order = retail_sub.add_parser(
        "update-order",
        help="Update a retail order from explicit flags or a JSON file.",
        description="Update a retail order from explicit flags or a JSON file.",
    )
    parsers["retail-sync update-order"] = retail_update_order
    add_json_file_flag(retail_update_order)
    retail_update_order.add_argument("--retail-order-id", help="Retail order ID to update.")
    retail_update_order.add_argument("--merchant-name", help="Updated order merchant name.")
    retail_update_order.add_argument("--date", help="Updated order date.")
    retail_update_order.add_argument("--total-before-tax", type=float, help="Updated pre-tax total.")
    retail_update_order.add_argument("--tax", type=float, help="Updated tax total.")
    retail_update_order.add_argument("--tip", type=float, help="Updated tip total.")
    retail_update_order.add_argument("--grand-total", type=float, help="Updated grand total.")
    add_optional_json_file_flag(
        retail_update_order,
        "--line-item-updates-json-file",
        "Path to a JSON file containing the lineItemUpdates array.",
    )
    add_optional_json_file_flag(
        retail_update_order,
        "--transaction-updates-json-file",
        "Path to a JSON file containing the transactionUpdates array.",
    )
    add_details_flag(retail_update_order)
    retail_update_order.set_defaults(func=cmd_retail_sync_update_order)

    retail_update_vendor_settings = retail_sub.add_parser(
        "update-vendor-settings",
        help="Update retail vendor settings from explicit flags or a JSON file.",
        description="Update retail vendor settings from explicit flags or a JSON file.",
    )
    parsers["retail-sync update-vendor-settings"] = retail_update_vendor_settings
    add_json_file_flag(retail_update_vendor_settings)
    retail_update_vendor_settings.add_argument("--vendor", help="Retail sync vendor enum value to update.")
    retail_update_vendor_settings.add_argument("--merchant-name", help="Merchant name to scope vendor settings to.")
    retail_update_vendor_settings.add_argument(
        "--should-categorize-and-split-transactions",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Whether imported retail transactions should be categorized and split automatically.",
    )
    retail_update_vendor_settings.add_argument(
        "--should-update-past-transactions",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Whether past transactions should also be updated.",
    )
    retail_update_vendor_settings.add_argument(
        "--should-update-transactions-notes",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Whether linked transaction notes should be updated.",
    )
    add_details_flag(retail_update_vendor_settings)
    retail_update_vendor_settings.set_defaults(func=cmd_retail_sync_update_vendor_settings)

    return root, parsers
