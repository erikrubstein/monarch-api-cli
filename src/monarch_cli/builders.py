from __future__ import annotations

import argparse
from typing import Any

from .runtime import (
    bool_override,
    load_json_file,
    load_json_list_file,
    load_json_object_file,
    merge_payload,
    parse_id_list,
    require_keys,
)
from .style import BOLD, RED, color

def build_transaction_create_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = merge_payload(
        load_json_file(args.input_json_file),
        {
            "date": args.date,
            "amount": args.amount,
            "merchantName": args.merchant_name,
            "accountId": args.account_id,
            "categoryId": args.category_id,
            "notes": args.notes,
            "ownerUserId": args.owner_user_id,
            "shouldUpdateBalance": args.should_update_balance,
        },
    )
    return require_keys(
        payload,
        ["date", "amount", "merchantName", "accountId", "categoryId"],
        "transactions create input",
    )


def build_transaction_update_input(args: argparse.Namespace) -> dict[str, Any]:
    hide_from_reports = bool_override(args.hide_from_reports, args.show_in_reports)
    payload = merge_payload(
        load_json_file(args.input_json_file),
        {
            "id": args.transaction_id,
            "date": args.date,
            "amount": args.amount,
            "name": args.merchant_name,
            "categoryId": args.category_id,
            "notes": args.notes,
            "ownerUserId": args.owner_user_id,
            "businessEntityId": args.business_entity_id,
            "hideFromReports": hide_from_reports,
        },
    )
    return require_keys(payload, ["id"], "transactions update input")


def build_merchant_update_input(args: argparse.Namespace) -> dict[str, Any]:
    recurring = bool_override(args.recurring, args.not_recurring)
    recurrence_is_active = bool_override(args.recurrence_is_active, args.recurrence_is_inactive)
    payload = merge_payload(
        load_json_file(args.input_json_file),
        {
            "id": args.merchant_id,
            "name": args.name,
            "recurring": recurring,
            "recurrenceAmount": args.recurrence_amount,
            "recurrenceIsActive": recurrence_is_active,
        },
    )
    return require_keys(payload, ["id"], "merchants update input")


def build_attachment_add_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = merge_payload(
        load_json_file(args.input_json_file),
        {
            "transactionId": args.transaction_id,
            "filename": args.filename,
            "publicId": args.public_id,
            "extension": args.extension,
            "sizeBytes": args.size_bytes,
        },
    )
    return require_keys(
        payload,
        ["transactionId", "filename", "publicId", "extension", "sizeBytes"],
        "attachments add input",
    )


def build_retail_sync_create_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = merge_payload(
        load_json_file(args.input_json_file),
        {
            "vendor": args.vendor,
            "isBackfill": args.is_backfill,
        },
    )
    return require_keys(payload, ["vendor"], "retail-sync create input")


def build_retail_sync_create_bulk_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = merge_payload(
        load_json_file(args.input_json_file),
        {
            "count": args.count,
        },
    )
    return require_keys(payload, ["count"], "retail-sync create-bulk input")


def build_retail_sync_update_order_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = merge_payload(
        load_json_file(args.input_json_file),
        {
            "retailOrderId": args.retail_order_id,
            "merchantName": args.merchant_name,
            "date": args.date,
            "totalBeforeTax": args.total_before_tax,
            "tax": args.tax,
            "tip": args.tip,
            "grandTotal": args.grand_total,
            "lineItemUpdates": load_json_file(args.line_item_updates_json_file),
            "transactionUpdates": load_json_file(args.transaction_updates_json_file),
        },
    )
    return require_keys(payload, ["retailOrderId"], "retail-sync update-order input")


def build_retail_sync_update_vendor_settings_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = merge_payload(
        load_json_file(args.input_json_file),
        {
            "vendor": args.vendor,
            "merchantName": args.merchant_name,
            "shouldCategorizeAndSplitTransactions": args.should_categorize_and_split_transactions,
            "shouldUpdatePastTransactions": args.should_update_past_transactions,
            "shouldUpdateTransactionsNotes": args.should_update_transactions_notes,
        },
    )
    return require_keys(payload, ["vendor"], "retail-sync update-vendor-settings input")


def build_rule_criteria_input(path: str | None, operator: str | None, value: str | None, context: str) -> list[dict[str, Any]] | None:
    payload = load_json_file(path)
    criteria: list[dict[str, Any]] = []
    if payload is not None:
        if isinstance(payload, dict):
            criteria = [payload]
        elif isinstance(payload, list) and all(isinstance(item, dict) for item in payload):
            criteria = list(payload)
        else:
            raise SystemExit(color(f"{context} must be a JSON object or array of JSON objects.", RED, BOLD))

    if operator is not None or value is not None:
        base = criteria[0] if len(criteria) == 1 else {}
        criteria = [
            merge_payload(
                base,
                {
                    "operator": operator,
                    "value": value,
                },
            )
        ]
    return criteria or None


def build_rule_amount_criteria_input(args: argparse.Namespace) -> dict[str, Any] | None:
    payload = load_json_object_file(args.amount_criteria_json_file, "rules amountCriteria input")
    amount_range = merge_payload(
        ((payload or {}).get("valueRange") if isinstance((payload or {}).get("valueRange"), dict) else None),
        {
            "lower": args.amount_lower,
            "upper": args.amount_upper,
        },
    )
    merged = merge_payload(
        payload,
        {
            "operator": args.amount_operator,
            "isExpense": args.amount_is_expense,
            "value": args.amount_value,
            "valueRange": amount_range or None,
        },
    )
    return merged or None


def build_rule_split_action_input(args: argparse.Namespace) -> dict[str, Any] | None:
    payload = load_json_object_file(args.split_transactions_action_json_file, "rules splitTransactionsAction input")
    merged = merge_payload(
        payload,
        {
            "amountType": args.split_amount_type,
            "splitsInfo": load_json_list_file(args.split_info_json_file, "rules splitTransactionsAction.splitsInfo"),
        },
    )
    return merged or None


def build_rule_input(args: argparse.Namespace, *, include_rule_id: bool, context: str) -> dict[str, Any]:
    payload = merge_payload(
        load_json_object_file(args.input_json_file, context),
        {
            "id": args.rule_id if include_rule_id else None,
            "merchantCriteriaUseOriginalStatement": args.merchant_criteria_use_original_statement,
            "merchantCriteria": build_rule_criteria_input(
                args.merchant_criteria_json_file,
                args.merchant_criteria_operator,
                args.merchant_criteria_value,
                "rules merchantCriteria input",
            ),
            "originalStatementCriteria": build_rule_criteria_input(
                args.original_statement_criteria_json_file,
                args.original_statement_criteria_operator,
                args.original_statement_criteria_value,
                "rules originalStatementCriteria input",
            ),
            "merchantNameCriteria": build_rule_criteria_input(
                args.merchant_name_criteria_json_file,
                args.merchant_name_criteria_operator,
                args.merchant_name_criteria_value,
                "rules merchantNameCriteria input",
            ),
            "amountCriteria": build_rule_amount_criteria_input(args),
            "categoryIds": parse_id_list(args.category_id) or None,
            "accountIds": parse_id_list(args.account_id) or None,
            "criteriaOwnerIsJoint": args.criteria_owner_is_joint,
            "criteriaOwnerUserIds": parse_id_list(args.criteria_owner_user_id) or None,
            "criteriaBusinessEntityIds": parse_id_list(args.criteria_business_entity_id) or None,
            "criteriaBusinessEntityIsUnassigned": args.criteria_business_entity_is_unassigned,
            "setMerchantAction": args.set_merchant_action,
            "setCategoryAction": args.set_category_action,
            "addTagsAction": parse_id_list(args.add_tag_action) or None,
            "linkGoalAction": args.link_goal_action,
            "linkSavingsGoalAction": args.link_savings_goal_action,
            "sendNotificationAction": args.send_notification_action,
            "setHideFromReportsAction": args.set_hide_from_reports_action,
            "reviewStatusAction": args.review_status_action,
            "needsReviewByUserAction": args.needs_review_by_user_action,
            "unassignNeedsReviewByUserAction": args.unassign_needs_review_by_user_action,
            "actionSetOwnerIsJoint": args.action_set_owner_is_joint,
            "actionSetOwner": args.action_set_owner,
            "actionSetBusinessEntity": args.action_set_business_entity,
            "actionSetBusinessEntityIsUnassigned": args.action_set_business_entity_is_unassigned,
            "splitTransactionsAction": build_rule_split_action_input(args),
        },
    )
    if include_rule_id:
        return require_keys(payload, ["id"], context)
    return payload


def build_transaction_filter_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_json_file(args.filters_json_file)
    if payload is not None and not isinstance(payload, dict):
        raise SystemExit(color("transactions filters input must be a JSON object.", RED, BOLD))

    merged = merge_payload(
        payload,
        {
            "startDate": args.start_date,
            "endDate": args.end_date,
            "search": args.search,
            "accounts": parse_id_list(args.account_id) or None,
            "tags": parse_id_list(args.tag_id) or None,
            "categories": parse_id_list(args.category_id) or None,
            "categoryType": args.category_type,
            "transactionVisibility": args.transaction_visibility,
        },
    )
    if "transactionVisibility" not in merged:
        merged["transactionVisibility"] = "non_hidden_transactions_only"
    return merged


def build_retail_sync_filter_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_json_file(args.filters_json_file)
    if payload is not None and not isinstance(payload, dict):
        raise SystemExit(color("retail-sync filters input must be a JSON object.", RED, BOLD))

    return merge_payload(
        payload,
        {
            "status": args.status,
            "vendor": args.vendor,
        },
    )


def build_account_filter_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_json_file(args.filters_json_file)
    if payload is not None and not isinstance(payload, dict):
        raise SystemExit(color("accounts filters input must be a JSON object.", RED, BOLD))

    return merge_payload(
        payload,
        {
            "accountSubtypes": parse_id_list(args.account_subtype) or None,
        },
    )


def build_force_refresh_account_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = merge_payload(
        load_json_object_file(args.input_json_file, "accounts refresh-account input"),
        {
            "accountId": args.account_id,
            "source": args.source,
        },
    )
    return require_keys(payload, ["accountId"], "accounts refresh-account input")


def build_force_refresh_all_input(args: argparse.Namespace) -> dict[str, Any] | None:
    payload = merge_payload(
        load_json_object_file(args.input_json_file, "accounts refresh-all input"),
        {
            "source": args.source,
        },
    )
    return payload or None


def build_portfolio_input(args: argparse.Namespace) -> dict[str, Any] | None:
    payload = merge_payload(
        load_json_object_file(args.input_json_file, "investments portfolio input"),
        {
            "startDate": args.start_date,
            "endDate": args.end_date,
        },
    )
    return payload or None


def build_security_history_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = merge_payload(
        load_json_object_file(args.input_json_file, "investments security-history input"),
        {
            "securityIds": parse_id_list(args.security_id) or None,
            "startDate": args.start_date,
            "endDate": args.end_date,
        },
    )
    return require_keys(payload, ["securityIds", "startDate", "endDate"], "investments security-history input")


def build_subscription_modal_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = merge_payload(
        load_json_object_file(args.input_json_file, "subscription modal input"),
        {
            "promoCode": args.promo_code,
            "stripePriceId": args.stripe_price_id,
        },
    )
    if payload.get("stripePriceId") is None:
        payload["stripePriceId"] = ""
    return payload


def build_subscription_premium_upgrade_plans_input(args: argparse.Namespace) -> dict[str, Any]:
    return merge_payload(
        load_json_object_file(args.input_json_file, "subscription premium-upgrade-plans input"),
        {
            "promoCode": args.promo_code,
            "referralCode": args.referral_code,
            "selectedPlanId": args.selected_plan_id,
        },
    )


def build_subscription_referral_settings_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = merge_payload(
        load_json_object_file(args.input_json_file, "subscription referral-settings input"),
        {
            "statisticsStartDate": args.statistics_start_date,
            "statisticsEndDate": args.statistics_end_date,
            "v1PayoutMethod": args.v1_payout_method,
            "v2PayoutMethod": args.v2_payout_method,
        },
    )
    return require_keys(
        payload,
        ["statisticsStartDate", "statisticsEndDate", "v1PayoutMethod", "v2PayoutMethod"],
        "subscription referral-settings input",
    )


def build_date_range_input(args: argparse.Namespace, context: str) -> dict[str, Any]:
    payload = merge_payload(
        load_json_object_file(args.input_json_file, context),
        {
            "startDate": args.start_date,
            "endDate": args.end_date,
        },
    )
    return require_keys(payload, ["startDate", "endDate"], context)


def build_recurring_filter_input(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_json_file(args.filters_json_file)
    if payload is not None and not isinstance(payload, dict):
        raise SystemExit(color("recurring filters input must be a JSON object.", RED, BOLD))
    return merge_payload(
        payload,
        {
            "isCompleted": args.is_completed,
        },
    )


def build_aggregate_snapshot_filters(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_json_file(args.filters_json_file)
    if payload is not None and not isinstance(payload, dict):
        raise SystemExit(color("accounts aggregate-snapshots filters must be a JSON object.", RED, BOLD))

    account_filters = merge_payload(
        ((payload or {}).get("accountFilters") if isinstance(payload, dict) else None),
        {
            "accountSubtypes": parse_id_list(args.account_subtype) or None,
        },
    )
    merged = merge_payload(
        payload,
        {
            "startDate": args.start_date,
            "endDate": args.end_date,
            "useAdaptiveGranularity": args.use_adaptive_granularity,
        },
    )
    if account_filters:
        merged["accountFilters"] = account_filters
    return require_keys(merged, ["startDate"], "accounts aggregate-snapshots filters")


def build_display_balance_input(args: argparse.Namespace) -> tuple[str, dict[str, Any]]:
    payload = load_json_object_file(args.input_json_file, "accounts display-balance input")
    filters = merge_payload(
        ((payload or {}).get("filters") if isinstance(payload, dict) else None),
        {
            "accountSubtypes": parse_id_list(args.account_subtype) or None,
        },
    )
    date = args.date or ((payload or {}).get("date") if isinstance(payload, dict) else None)
    if not date:
        raise SystemExit(color("accounts display-balance input is missing required field(s): date", RED, BOLD))
    return date, filters


def build_snapshots_by_account_type_input(args: argparse.Namespace) -> tuple[str, str, dict[str, Any]]:
    payload = load_json_object_file(args.input_json_file, "accounts snapshots-by-account-type input")
    filters = merge_payload(
        ((payload or {}).get("filters") if isinstance(payload, dict) else None),
        {
            "accountSubtypes": parse_id_list(args.account_subtype) or None,
        },
    )
    start_date = args.start_date or ((payload or {}).get("startDate") if isinstance(payload, dict) else None)
    timeframe = args.timeframe or ((payload or {}).get("timeframe") if isinstance(payload, dict) else None)
    missing: list[str] = []
    if not start_date:
        missing.append("startDate")
    if not timeframe:
        missing.append("timeframe")
    if missing:
        raise SystemExit(
            color(
                f"accounts snapshots-by-account-type input is missing required field(s): {', '.join(missing)}",
                RED,
                BOLD,
            )
        )
    return start_date, timeframe, filters
