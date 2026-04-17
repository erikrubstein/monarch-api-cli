from __future__ import annotations

import argparse
from getpass import getpass
from typing import Any, Callable

from monarch_api import MonarchClient

from .builders import *
from .runtime import *
from .summaries import output_result

def run_authenticated(func: Callable[[MonarchClient], Any], *, details: bool = False, summary_kind: str | None = None) -> None:
    with MonarchClient() as client:
        ensure_authenticated(client)
        result = func(client)
    output_result(result, details=details, summary_kind=summary_kind)


def cmd_auth_login(args: argparse.Namespace) -> None:
    with MonarchClient() as client:
        me = interactive_login(client)
    output_result(me, details=args.details, summary_kind="auth_me")


def cmd_auth_use_token(args: argparse.Namespace) -> None:
    token = args.token or getpass("Monarch token: ").strip()
    if not token:
        raise SystemExit("A token is required.")
    with MonarchClient() as client:
        client.auth.use_token(token, device_uuid=args.device_uuid)
        me = client.auth.get_me()
        ensure_session_dir()
        client.auth.save_session(SESSION_PATH)
        print_info(f"Saved session to {SESSION_PATH}")
    output_result(me, details=args.details, summary_kind="auth_me")


def cmd_auth_me(args: argparse.Namespace) -> None:
    run_authenticated(lambda client: client.auth.get_me(), details=args.details, summary_kind="auth_me")


def cmd_auth_clear_session(args: argparse.Namespace) -> None:
    SESSION_PATH.unlink(missing_ok=True)
    print_info(f"Deleted {SESSION_PATH}")


def cmd_household_get(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.household.get(),
        details=args.details,
        summary_kind="household",
    )


def cmd_household_members(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.household.members(),
        details=args.details,
        summary_kind="household_members",
    )


def cmd_household_preferences(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.household.preferences(),
        details=args.details,
        summary_kind="household_preferences",
    )


def cmd_accounts_has_accounts(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: {"hasAccounts": client.accounts.has_accounts()},
        details=args.details,
        summary_kind=None,
    )


def cmd_accounts_syncing(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.accounts.syncing_status(),
        details=args.details,
        summary_kind="accounts_syncing",
    )


def cmd_accounts_page(args: argparse.Namespace) -> None:
    filters = build_account_filter_input(args)
    run_authenticated(
        lambda client: client.accounts.page(filters=filters),
        details=args.details,
        summary_kind="accounts_page",
    )


def cmd_accounts_notices(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.accounts.active_institution_notices(),
        details=args.details,
        summary_kind="accounts_notices",
    )


def cmd_accounts_recent_balances(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.accounts.recent_balances(start_date=args.start_date),
        details=args.details,
        summary_kind="accounts_recent_balances",
    )


def cmd_accounts_filtered(args: argparse.Namespace) -> None:
    filters = build_account_filter_input(args)
    run_authenticated(
        lambda client: client.accounts.filtered(filters=filters),
        details=args.details,
        summary_kind="accounts_list",
    )


def cmd_accounts_institution_settings(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.accounts.institution_settings(),
        details=args.details,
        summary_kind="accounts_institution_settings",
    )


def cmd_accounts_institutions(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.accounts.institutions(ids=parse_id_list(args.id), include_logo=args.include_logo),
        details=args.details,
        summary_kind="accounts_institutions",
    )


def cmd_accounts_institution(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.accounts.institution(args.institution_id),
        details=args.details,
        summary_kind="accounts_institution",
    )


def cmd_accounts_aggregate_snapshots(args: argparse.Namespace) -> None:
    filters = build_aggregate_snapshot_filters(args)
    run_authenticated(
        lambda client: client.accounts.aggregate_snapshots(filters=filters),
        details=args.details,
        summary_kind="aggregate_snapshots",
    )


def cmd_accounts_display_balance(args: argparse.Namespace) -> None:
    date, filters = build_display_balance_input(args)
    run_authenticated(
        lambda client: client.accounts.display_balance_at_date(date=date, filters=filters),
        details=args.details,
        summary_kind="display_balances",
    )


def cmd_accounts_snapshots_by_account_type(args: argparse.Namespace) -> None:
    start_date, timeframe, filters = build_snapshots_by_account_type_input(args)
    run_authenticated(
        lambda client: client.accounts.snapshots_by_account_type(
            start_date=start_date,
            timeframe=timeframe,
            filters=filters,
        ),
        details=args.details,
        summary_kind="snapshots_by_account_type",
    )


def cmd_accounts_filters(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.accounts.filters(),
        details=args.details,
        summary_kind="accounts_filters",
    )


def cmd_accounts_account_types(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.accounts.account_types(),
        details=args.details,
        summary_kind="account_types",
    )


def cmd_accounts_refresh_status(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.accounts.force_refresh_account_status(args.account_id),
        details=args.details,
        summary_kind="force_refresh_account_status",
    )


def cmd_accounts_latest_refresh(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.accounts.latest_force_refresh_operation(),
        details=args.details,
        summary_kind="force_refresh_operation",
    )


def cmd_accounts_refresh_operation(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.accounts.force_refresh_operation(args.operation_id),
        details=args.details,
        summary_kind="force_refresh_operation",
    )


def cmd_accounts_refresh_account(args: argparse.Namespace) -> None:
    payload = build_force_refresh_account_input(args)
    run_authenticated(
        lambda client: client.accounts.force_refresh_account(payload),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_accounts_refresh_all(args: argparse.Namespace) -> None:
    payload = build_force_refresh_all_input(args)
    run_authenticated(
        lambda client: client.accounts.force_refresh_all(payload),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_subscription_details(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.subscription.details(),
        details=args.details,
        summary_kind="subscription_state",
    )


def cmd_subscription_get(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.subscription.subscription(),
        details=args.details,
        summary_kind="subscription",
    )


def cmd_subscription_modal(args: argparse.Namespace) -> None:
    payload = build_subscription_modal_input(args)
    run_authenticated(
        lambda client: client.subscription.modal(
            promo_code=payload.get("promoCode"),
            stripe_price_id=payload.get("stripePriceId", ""),
        ),
        details=args.details,
        summary_kind="subscription_modal",
    )


def cmd_subscription_premium_upgrade_plans(args: argparse.Namespace) -> None:
    payload = build_subscription_premium_upgrade_plans_input(args)
    run_authenticated(
        lambda client: client.subscription.premium_upgrade_plans(
            promo_code=payload.get("promoCode"),
            referral_code=payload.get("referralCode"),
            selected_plan_id=payload.get("selectedPlanId"),
        ),
        details=args.details,
        summary_kind="subscription_modal",
    )


def cmd_subscription_trial_status(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.subscription.trial_status(),
        details=args.details,
        summary_kind="subscription_state",
    )


def cmd_subscription_entitlements(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.subscription.entitlements(),
        details=args.details,
        summary_kind="subscription_state",
    )


def cmd_subscription_feature_entitlement_params(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.subscription.feature_entitlement_params(),
        details=args.details,
        summary_kind="feature_entitlement_params",
    )


def cmd_subscription_plus_tier_access(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.subscription.plus_tier_access(),
        details=args.details,
        summary_kind="subscription_state",
    )


def cmd_subscription_gifted_subscriptions(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.subscription.gifted_subscriptions(),
        details=args.details,
        summary_kind="gifted_subscriptions",
    )


def cmd_subscription_referral_settings(args: argparse.Namespace) -> None:
    payload = build_subscription_referral_settings_input(args)
    run_authenticated(
        lambda client: client.subscription.referral_settings(
            statistics_start_date=payload["statisticsStartDate"],
            statistics_end_date=payload["statisticsEndDate"],
            v1_payout_method=payload["v1PayoutMethod"],
            v2_payout_method=payload["v2PayoutMethod"],
        ),
        details=args.details,
        summary_kind="referral_settings",
    )


def cmd_settings_user_profile_flags(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.user_profile_flags(),
        details=args.details,
        summary_kind="user_profile_flags",
    )


def cmd_settings_dashboard_config(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.dashboard_config(),
        details=args.details,
        summary_kind="dashboard_config",
    )


def cmd_settings_sidebar_data(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.sidebar_data(promo_code=args.promo_code),
        details=args.details,
        summary_kind="sidebar_data",
    )


def cmd_settings_household_member_settings(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.household_member_settings(),
        details=args.details,
        summary_kind="household_member_settings",
    )


def cmd_settings_security(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.security_settings(),
        details=args.details,
        summary_kind="security_settings",
    )


def cmd_settings_notification_preferences(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.notification_preferences(),
        details=args.details,
        summary_kind="notification_preferences",
    )


def cmd_settings_review_summary_by_user(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.review_summary_by_user(),
        details=args.details,
        summary_kind="review_summary_by_user",
    )


def cmd_settings_business_entities_banner_profile(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.business_entities_banner_profile(),
        details=args.details,
        summary_kind="business_entities_banner_profile",
    )


def cmd_settings_business_entities(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.business_entities(),
        details=args.details,
        summary_kind="business_entities",
    )


def cmd_settings_has_activity(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.has_activity(),
        details=args.details,
        summary_kind=None,
    )


def cmd_settings_oldest_deletable_synced_snapshot_date(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.oldest_deletable_synced_snapshot_date(),
        details=args.details,
        summary_kind=None,
    )


def cmd_settings_oldest_deletable_transaction_date(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.settings.oldest_deletable_transaction_date(
            include_synced=args.include_synced,
            include_uploaded=args.include_uploaded,
            include_manual=args.include_manual,
        ),
        details=args.details,
        summary_kind=None,
    )


def cmd_planning_budget_data(args: argparse.Namespace) -> None:
    payload = build_date_range_input(args, "planning budget-data input")
    run_authenticated(
        lambda client: client.planning.budget_data(start_date=payload["startDate"], end_date=payload["endDate"]),
        details=args.details,
        summary_kind="planning",
    )


def cmd_planning_joint_data(args: argparse.Namespace) -> None:
    payload = build_date_range_input(args, "planning joint-data input")
    run_authenticated(
        lambda client: client.planning.joint_planning_data(start_date=payload["startDate"], end_date=payload["endDate"]),
        details=args.details,
        summary_kind="planning",
    )


def cmd_goals_savings_goals(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.goals.savings_goals(),
        details=args.details,
        summary_kind="goals",
    )


def cmd_goals_savings_goals_with_balances(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.goals.savings_goals_with_this_month_balances(),
        details=args.details,
        summary_kind="goals_with_balances",
    )


def cmd_goals_savings_goal_account(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.goals.savings_goal_account(args.account_id),
        details=args.details,
        summary_kind="goal_account",
    )


def cmd_goals_dashboard_card(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.goals.dashboard_card(),
        details=args.details,
        summary_kind="goals_dashboard",
    )


def cmd_goals_legacy_migration(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.goals.legacy_migration(),
        details=args.details,
        summary_kind="legacy_goals_migration",
    )


def cmd_recurring_streams(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.recurring.streams(include_liabilities=args.include_liabilities),
        details=args.details,
        summary_kind="recurring_streams",
    )


def cmd_recurring_aggregated_items(args: argparse.Namespace) -> None:
    payload = build_date_range_input(args, "recurring aggregated-items input")
    filters = build_recurring_filter_input(args)
    run_authenticated(
        lambda client: client.recurring.aggregated_items(
            start_date=payload["startDate"],
            end_date=payload["endDate"],
            filters=filters,
        ),
        details=args.details,
        summary_kind="aggregated_recurring",
    )


def cmd_recurring_dashboard_upcoming(args: argparse.Namespace) -> None:
    payload = build_date_range_input(args, "recurring dashboard-upcoming input")
    filters = build_recurring_filter_input(args)
    run_authenticated(
        lambda client: client.recurring.dashboard_upcoming_items(
            start_date=payload["startDate"],
            end_date=payload["endDate"],
            include_liabilities=args.include_liabilities,
            filters=filters,
        ),
        details=args.details,
        summary_kind="dashboard_upcoming_recurring",
    )


def cmd_recurring_paused_banner(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.recurring.paused_banner(),
        details=args.details,
        summary_kind="recurring_paused_banner",
    )


def cmd_investments_accounts(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.investments.accounts(),
        details=args.details,
        summary_kind="investments_accounts",
    )


def cmd_investments_dashboard_card(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.investments.dashboard_card(),
        details=args.details,
        summary_kind="investments_dashboard",
    )


def cmd_investments_portfolio(args: argparse.Namespace) -> None:
    portfolio_input = build_portfolio_input(args)
    run_authenticated(
        lambda client: client.investments.portfolio(portfolio_input=portfolio_input),
        details=args.details,
        summary_kind="portfolio",
    )


def cmd_investments_security_history(args: argparse.Namespace) -> None:
    input_data = build_security_history_input(args)
    run_authenticated(
        lambda client: client.investments.securities_historical_performance(input_data=input_data),
        details=args.details,
        summary_kind="security_history",
    )


def cmd_transactions_list(args: argparse.Namespace) -> None:
    filters = build_transaction_filter_input(args)
    run_authenticated(
        lambda client: client.transactions.list(
            offset=args.offset,
            limit=args.limit,
            filters=filters,
            order_by=args.order_by,
        ),
        details=args.details,
        summary_kind="transactions_list",
    )


def cmd_transactions_get(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.transactions.get(args.transaction_id, redirect_posted=not args.no_redirect_posted),
        details=args.details,
        summary_kind="transaction_detail",
    )


def cmd_transactions_filters(args: argparse.Namespace) -> None:
    include_ids = parse_id_list(args.include_id)
    run_authenticated(
        lambda client: client.transactions.filters(search=args.search, include_ids=include_ids or None),
        details=args.details,
        summary_kind="transaction_filters",
    )


def cmd_transactions_filters_metadata(args: argparse.Namespace) -> None:
    filters = build_transaction_filter_input(args)
    run_authenticated(
        lambda client: client.transactions.filters_metadata(filters),
        details=args.details,
        summary_kind="transaction_filters_metadata",
    )


def cmd_transactions_create(args: argparse.Namespace) -> None:
    payload = build_transaction_create_input(args)
    run_authenticated(
        lambda client: client.transactions.create(payload),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_transactions_update(args: argparse.Namespace) -> None:
    payload = build_transaction_update_input(args)
    run_authenticated(
        lambda client: client.transactions.update(payload),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_transactions_delete(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.transactions.delete(args.transaction_id),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_transactions_set_tags(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.transactions.set_tags(args.transaction_id, parse_id_list(args.tag_id)),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_transactions_tags(args: argparse.Namespace) -> None:
    bulk_params = load_json_file(args.bulk_params_json_file)
    run_authenticated(
        lambda client: client.transactions.tags(
            search=args.search,
            limit=args.limit,
            bulk_params=bulk_params,
            include_transaction_count=args.include_transaction_count,
        ),
        details=args.details,
        summary_kind="tags",
    )


def cmd_transactions_categories(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.transactions.categories(
            include_system_disabled_categories=args.include_system_disabled_categories,
        ),
        details=args.details,
        summary_kind="categories",
    )


def cmd_merchants_search(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.merchants.search(
            search=args.search,
            limit=args.limit,
            include_ids=parse_id_list(args.include_id) or None,
        ),
        details=args.details,
        summary_kind="merchants",
    )


def cmd_merchants_household(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.merchants.household(
            offset=args.offset,
            limit=args.limit,
            order_by=args.order_by,
            search=args.search,
        ),
        details=args.details,
        summary_kind="merchants",
    )


def cmd_merchants_recommended(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.merchants.recommended_for_transaction(args.transaction_id),
        details=args.details,
        summary_kind="merchants",
    )


def cmd_merchants_update(args: argparse.Namespace) -> None:
    payload = build_merchant_update_input(args)
    run_authenticated(
        lambda client: client.merchants.update(payload),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_attachments_upload_info(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.attachments.get_upload_info(args.transaction_id),
        details=args.details,
        summary_kind="attachment_upload_info",
    )


def cmd_attachments_add(args: argparse.Namespace) -> None:
    payload = build_attachment_add_input(args)
    run_authenticated(
        lambda client: client.attachments.add(payload),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_attachments_get(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.attachments.get(args.attachment_id),
        details=args.details,
        summary_kind="attachment",
    )


def cmd_attachments_delete(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: {"deleted": client.attachments.delete(args.attachment_id)},
        details=args.details,
        summary_kind="mutation",
    )


def cmd_rules_list(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.rules.list(),
        details=args.details,
        summary_kind="rules",
    )


def cmd_rules_create(args: argparse.Namespace) -> None:
    payload = build_rule_input(args, include_rule_id=False, context="rules create input")
    run_authenticated(
        lambda client: client.rules.create(payload),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_rules_update(args: argparse.Namespace) -> None:
    payload = build_rule_input(args, include_rule_id=True, context="rules update input")
    run_authenticated(
        lambda client: client.rules.update(payload),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_rules_delete(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.rules.delete(args.rule_id),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_rules_preview(args: argparse.Namespace) -> None:
    payload = build_rule_input(args, include_rule_id=False, context="rules preview input")
    run_authenticated(
        lambda client: client.rules.preview(payload, offset=args.offset),
        details=args.details,
        summary_kind="rule_preview",
    )


def cmd_rules_update_order(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.rules.update_order(args.rule_id, args.order),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_rules_delete_all(args: argparse.Namespace) -> None:
    if not args.yes:
        raise SystemExit(color("rules delete-all requires --yes.", RED, BOLD))
    run_authenticated(
        lambda client: client.rules.delete_all(),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_reports_cash_flow_dashboard(args: argparse.Namespace) -> None:
    filters = build_transaction_filter_input(args)
    run_authenticated(
        lambda client: client.reports.cash_flow_dashboard(filters=filters),
        details=args.details,
        summary_kind="cash_flow_dashboard",
    )


def cmd_reports_cash_flow_entities(args: argparse.Namespace) -> None:
    filters = build_transaction_filter_input(args)
    run_authenticated(
        lambda client: client.reports.cash_flow_entity_aggregates(filters=filters),
        details=args.details,
        summary_kind="cash_flow_entity_aggregates",
    )


def cmd_reports_cash_flow_timeframes(args: argparse.Namespace) -> None:
    filters = build_transaction_filter_input(args)
    run_authenticated(
        lambda client: client.reports.cash_flow_timeframe_aggregates(filters=filters),
        details=args.details,
        summary_kind="cash_flow_timeframe_aggregates",
    )


def cmd_reports_data(args: argparse.Namespace) -> None:
    filters = build_transaction_filter_input(args)
    run_authenticated(
        lambda client: client.reports.data(
            filters=filters,
            group_by=parse_id_list(args.group_by) or None,
            group_by_timeframe=args.group_by_timeframe,
            sort_by=args.sort_by,
            include_category=args.include_category,
            include_category_group=args.include_category_group,
            include_merchant=args.include_merchant,
            include_business_entity=args.include_business_entity,
            include_budget_variability=args.include_budget_variability,
            fill_empty_values=args.fill_empty_values,
        ),
        details=args.details,
        summary_kind="reports_data",
    )


def cmd_retail_sync_settings(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.retail_sync.get_settings(),
        details=args.details,
        summary_kind=None,
    )


def cmd_retail_sync_get(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.retail_sync.get(args.sync_id),
        details=args.details,
        summary_kind="retail_sync",
    )


def cmd_retail_sync_list(args: argparse.Namespace) -> None:
    filters = build_retail_sync_filter_input(args)
    run_authenticated(
        lambda client: client.retail_sync.list(
            filters=filters,
            offset=args.offset,
            limit=args.limit,
            include_total_count=not args.no_total_count,
        ),
        details=args.details,
        summary_kind="retail_sync_list",
    )


def cmd_retail_sync_create(args: argparse.Namespace) -> None:
    payload = build_retail_sync_create_input(args)
    run_authenticated(
        lambda client: client.retail_sync.create(payload),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_retail_sync_create_bulk(args: argparse.Namespace) -> None:
    payload = build_retail_sync_create_bulk_input(args)
    run_authenticated(
        lambda client: client.retail_sync.create_bulk(payload),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_retail_sync_start(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.retail_sync.start(args.sync_id),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_retail_sync_complete(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.retail_sync.complete(args.sync_id),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_retail_sync_delete(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.retail_sync.delete(args.sync_id),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_retail_sync_match(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.retail_sync.match_transaction(args.retail_transaction_id, args.transaction_id),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_retail_sync_unmatch(args: argparse.Namespace) -> None:
    run_authenticated(
        lambda client: client.retail_sync.unmatch_transaction(args.retail_transaction_id),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_retail_sync_update_order(args: argparse.Namespace) -> None:
    payload = build_retail_sync_update_order_input(args)
    run_authenticated(
        lambda client: client.retail_sync.update_order(payload),
        details=args.details,
        summary_kind="mutation",
    )


def cmd_retail_sync_update_vendor_settings(args: argparse.Namespace) -> None:
    payload = build_retail_sync_update_vendor_settings_input(args)
    run_authenticated(
        lambda client: client.retail_sync.update_vendor_settings(payload),
        details=args.details,
        summary_kind="mutation",
    )
