from __future__ import annotations

import argparse
import json

from monarch_cli.builders import (
    build_portfolio_input,
    build_recurring_filter_input,
    build_retail_sync_filter_input,
    build_rule_input,
    build_security_history_input,
    build_transaction_filter_input,
)


def test_transaction_filter_input_merges_file_and_flag_overrides(tmp_path) -> None:
    path = tmp_path / "tx_filters.json"
    path.write_text(
        json.dumps(
            {
                "startDate": "2026-03-01",
                "endDate": "2026-04-01",
                "search": "from-file",
                "accounts": ["acct-from-file"],
                "tags": ["tag-from-file"],
                "categories": ["category-from-file"],
                "categoryType": "income",
                "transactionVisibility": "all_transactions",
            }
        ),
        encoding="utf-8",
    )

    args = argparse.Namespace(
        filters_json_file=str(path),
        start_date=None,
        end_date="2026-04-13",
        search="from-flag",
        account_id=["acct-from-flag-1", "acct-from-flag-2"],
        tag_id=["tag-from-flag-1", "tag-from-flag-2"],
        category_id=None,
        category_type="expense",
        transaction_visibility="non_hidden_transactions_only",
    )

    payload = build_transaction_filter_input(args)

    assert payload == {
        "startDate": "2026-03-01",
        "endDate": "2026-04-13",
        "search": "from-flag",
        "accounts": ["acct-from-flag-1", "acct-from-flag-2"],
        "tags": ["tag-from-flag-1", "tag-from-flag-2"],
        "categories": ["category-from-file"],
        "categoryType": "expense",
        "transactionVisibility": "non_hidden_transactions_only",
    }


def test_transaction_filter_input_applies_default_visibility() -> None:
    args = argparse.Namespace(
        filters_json_file=None,
        start_date="2026-03-01",
        end_date="2026-04-01",
        search=None,
        account_id=["account-1"],
        tag_id=None,
        category_id=["category-1"],
        category_type=None,
        transaction_visibility=None,
    )

    payload = build_transaction_filter_input(args)

    assert payload == {
        "startDate": "2026-03-01",
        "endDate": "2026-04-01",
        "accounts": ["account-1"],
        "categories": ["category-1"],
        "transactionVisibility": "non_hidden_transactions_only",
    }


def test_retail_sync_filter_input_merges_file_and_flags(tmp_path) -> None:
    path = tmp_path / "retail_filters.json"
    path.write_text(json.dumps({"status": "completed", "vendor": "amazon"}), encoding="utf-8")

    args = argparse.Namespace(
        filters_json_file=str(path),
        status="pending_matches",
        vendor="user_import",
    )

    payload = build_retail_sync_filter_input(args)

    assert payload == {
        "status": "pending_matches",
        "vendor": "user_import",
    }


def test_rule_input_builds_criteria_lists_and_merges_flags(tmp_path) -> None:
    path = tmp_path / "merchant_criteria.json"
    path.write_text(json.dumps({"operator": "eq", "value": "ignored"}), encoding="utf-8")

    args = argparse.Namespace(
        input_json_file=None,
        rule_id=None,
        merchant_criteria_use_original_statement=None,
        merchant_criteria_json_file=None,
        merchant_criteria_operator=None,
        merchant_criteria_value=None,
        original_statement_criteria_json_file=None,
        original_statement_criteria_operator=None,
        original_statement_criteria_value=None,
        merchant_name_criteria_json_file=str(path),
        merchant_name_criteria_operator="contains",
        merchant_name_criteria_value="venmo",
        amount_criteria_json_file=None,
        amount_operator=None,
        amount_is_expense=None,
        amount_value=None,
        amount_lower=None,
        amount_upper=None,
        category_id=None,
        account_id=None,
        criteria_owner_is_joint=None,
        criteria_owner_user_id=None,
        criteria_business_entity_id=None,
        criteria_business_entity_is_unassigned=None,
        set_merchant_action=None,
        set_category_action=None,
        add_tag_action=None,
        link_goal_action=None,
        link_savings_goal_action=None,
        send_notification_action=None,
        set_hide_from_reports_action=None,
        review_status_action=None,
        needs_review_by_user_action=None,
        unassign_needs_review_by_user_action=None,
        action_set_owner_is_joint=None,
        action_set_owner=None,
        action_set_business_entity=None,
        action_set_business_entity_is_unassigned=None,
        split_transactions_action_json_file=None,
        split_amount_type=None,
        split_info_json_file=None,
    )

    payload = build_rule_input(args, include_rule_id=False, context="rules preview input")

    assert payload == {
        "merchantNameCriteria": [{"operator": "contains", "value": "venmo"}],
    }


def test_portfolio_input_merges_file_and_flag_overrides(tmp_path) -> None:
    path = tmp_path / "portfolio_input.json"
    path.write_text(json.dumps({"startDate": "2026-01-01", "endDate": "2026-02-01"}), encoding="utf-8")

    args = argparse.Namespace(
        input_json_file=str(path),
        start_date=None,
        end_date="2026-04-01",
    )

    payload = build_portfolio_input(args)

    assert payload == {
        "startDate": "2026-01-01",
        "endDate": "2026-04-01",
    }


def test_security_history_input_requires_confirmed_fields() -> None:
    args = argparse.Namespace(
        input_json_file=None,
        security_id=["sec-1", "sec-2"],
        start_date="2026-03-01",
        end_date="2026-04-01",
    )

    payload = build_security_history_input(args)

    assert payload == {
        "securityIds": ["sec-1", "sec-2"],
        "startDate": "2026-03-01",
        "endDate": "2026-04-01",
    }


def test_recurring_filter_input_merges_file_and_flags(tmp_path) -> None:
    path = tmp_path / "recurring_filters.json"
    path.write_text(json.dumps({"isCompleted": True}), encoding="utf-8")

    args = argparse.Namespace(
        filters_json_file=str(path),
        is_completed=False,
    )

    payload = build_recurring_filter_input(args)

    assert payload == {"isCompleted": False}
