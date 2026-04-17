from __future__ import annotations

from typing import Any

from .runtime import print_json

def summarize_transaction_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "date": item.get("date"),
        "amount": item.get("amount"),
        "pending": item.get("pending"),
        "merchant": (item.get("merchant") or {}).get("name"),
        "category": (item.get("category") or {}).get("name"),
        "account": (item.get("account") or {}).get("displayName"),
        "notes": item.get("notes"),
        "needsReview": item.get("needsReview"),
        "tags": [tag.get("name") for tag in item.get("tags", [])],
        "attachmentsCount": len(item.get("attachments", [])),
    }


def summarize_transactions_list(payload: dict[str, Any]) -> dict[str, Any]:
    all_transactions = payload["allTransactions"]
    return {
        "totalCount": all_transactions.get("totalCount"),
        "totalSelectableCount": all_transactions.get("totalSelectableCount"),
        "transactionRuleCount": len(payload.get("transactionRules", [])),
        "transactions": [summarize_transaction_item(item) for item in payload.get("results", [])],
    }


def summarize_transaction_detail(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        **summarize_transaction_item(payload),
        "originalDate": payload.get("originalDate"),
        "reviewedAt": payload.get("reviewedAt"),
        "reviewedByUser": (payload.get("reviewedByUser") or {}).get("name"),
        "hideFromReports": payload.get("hideFromReports"),
        "isManual": payload.get("isManual"),
        "isRecurring": payload.get("isRecurring"),
        "hasSplitTransactions": payload.get("hasSplitTransactions"),
        "splitTransactionsCount": len(payload.get("splitTransactions", [])),
        "updatedByRetailSync": payload.get("updatedByRetailSync"),
        "linkedRetailTransactionId": payload.get("linkedRetailTransactionId"),
        "attachments": [
            {
                "id": attachment.get("id"),
                "filename": attachment.get("filename"),
                "extension": attachment.get("extension"),
                "sizeBytes": attachment.get("sizeBytes"),
            }
            for attachment in payload.get("attachments", [])
        ],
    }


def summarize_collection(items: list[dict[str, Any]], fields: list[str]) -> list[dict[str, Any]]:
    return [{field: item.get(field) for field in fields} for item in items]


def summarize_filters(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "categoryGroups": summarize_collection(payload.get("categoryGroups", []), ["id", "name", "order"]),
        "goals": summarize_collection(payload.get("goalsV2", []), ["id", "name", "archivedAt", "priority"]),
        "savingsGoals": summarize_collection(payload.get("savingsGoals", []), ["id", "name", "archivedAt", "priority"]),
        "merchants": summarize_collection(payload.get("merchants", []), ["id", "name", "transactionCount"]),
        "accounts": summarize_collection(payload.get("accounts", []), ["id", "displayName", "logoUrl"]),
        "tags": summarize_collection(payload.get("householdTransactionTags", []), ["id", "name", "order", "color"]),
        "users": summarize_collection((payload.get("myHousehold") or {}).get("users", []), ["id", "displayName"]),
        "householdPreferences": payload.get("householdPreferences"),
    }


def summarize_filters_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "categories": summarize_collection(payload.get("categories", []), ["id", "name", "icon"]),
        "categoryGroups": summarize_collection(payload.get("categoryGroups", []), ["id", "name"]),
        "accounts": summarize_collection(payload.get("accounts", []), ["id", "displayName"]),
        "merchants": summarize_collection(payload.get("merchants", []), ["id", "name"]),
        "tags": summarize_collection(payload.get("tags", []), ["id", "name", "color"]),
        "goals": summarize_collection(payload.get("goals", []), ["id", "name"]),
        "savingsGoals": summarize_collection(payload.get("savingsGoals", []), ["id", "name"]),
        "needsReviewByUser": summarize_collection(payload.get("needsReviewByUser", []), ["id", "name"]),
    }


def summarize_categories(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "categoryGroupCount": len(payload.get("categoryGroups", [])),
        "categoryGroups": summarize_collection(payload.get("categoryGroups", []), ["id", "name", "order", "type"]),
        "categoryCount": len(payload.get("categories", [])),
        "categories": summarize_collection(payload.get("categories", []), ["id", "name", "icon", "isDisabled"]),
    }


def summarize_tags(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "tags": summarize_collection(payload, ["id", "name", "color", "order", "transactionCount"]),
    }


def summarize_merchants(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "merchants": summarize_collection(payload, ["id", "name", "transactionCount", "logoUrl", "source"]),
    }


def summarize_mutation_payload(payload: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for key in ("deleted", "success", "errors"):
        if key in payload:
            summary[key] = payload.get(key)
    if "transaction" in payload:
        transaction = payload.get("transaction") or {}
        summary["transaction"] = {"id": transaction.get("id")}
        if transaction.get("tags") is not None:
            summary["transaction"]["tagIds"] = [tag.get("id") for tag in transaction.get("tags", [])]
    if "merchant" in payload:
        merchant = payload.get("merchant") or {}
        summary["merchant"] = {
            "id": merchant.get("id"),
            "name": merchant.get("name"),
            "recurringTransactionStream": merchant.get("recurringTransactionStream"),
        }
    if "attachment" in payload:
        attachment = payload.get("attachment") or {}
        summary["attachment"] = {
            "id": attachment.get("id"),
            "filename": attachment.get("filename"),
            "extension": attachment.get("extension"),
            "sizeBytes": attachment.get("sizeBytes"),
        }
    if "retailSync" in payload:
        retail_sync = payload.get("retailSync") or {}
        summary["retailSync"] = {"id": retail_sync.get("id"), "status": retail_sync.get("status")}
    if "retailSyncs" in payload:
        summary["retailSyncs"] = summarize_collection(payload.get("retailSyncs", []), ["id", "status"])
    if "retailVendorSettings" in payload:
        summary["retailVendorSettings"] = payload.get("retailVendorSettings")
    if "forceRefreshOperationId" in payload:
        summary["forceRefreshOperationId"] = payload.get("forceRefreshOperationId")
    if "transactionRules" in payload:
        summary["transactionRules"] = summarize_rules(payload.get("transactionRules", []))
    return summary or payload


def summarize_attachment_upload_info(payload: dict[str, Any]) -> dict[str, Any]:
    info = payload.get("info") or {}
    return {
        "path": info.get("path"),
        "requestParams": info.get("requestParams"),
    }


def summarize_attachment(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": payload.get("id"),
        "filename": payload.get("filename"),
        "extension": payload.get("extension"),
        "sizeBytes": payload.get("sizeBytes"),
        "originalAssetUrl": payload.get("originalAssetUrl"),
    }


def summarize_retail_order(order: dict[str, Any]) -> dict[str, Any]:
    retail_transactions = order.get("retailTransactions", [])
    matched_transactions = [
        {
            "retailTransactionId": transaction.get("id"),
            "transactionId": (transaction.get("transaction") or {}).get("id"),
            "merchant": ((transaction.get("transaction") or {}).get("merchant") or {}).get("name"),
            "total": transaction.get("total"),
            "transactionType": transaction.get("transactionType"),
            "transactionUpdateSkipped": transaction.get("transactionUpdateSkipped"),
        }
        for transaction in retail_transactions
    ]
    return {
        "id": order.get("id"),
        "merchantName": order.get("merchantName"),
        "vendor": order.get("vendor"),
        "vendorOrderId": order.get("vendorOrderId"),
        "date": order.get("date"),
        "grandTotal": order.get("grandTotal"),
        "totalBeforeTax": order.get("totalBeforeTax"),
        "tax": order.get("tax"),
        "tip": order.get("tip"),
        "displayStatus": order.get("displayStatus"),
        "lineItemCount": len(order.get("retailLineItems", [])),
        "retailTransactions": matched_transactions,
    }


def summarize_retail_sync(payload: dict[str, Any]) -> dict[str, Any]:
    attachments = payload.get("attachments", [])
    orders = payload.get("orders", [])
    return {
        "id": payload.get("id"),
        "status": payload.get("status"),
        "vendor": payload.get("vendor"),
        "startedAt": payload.get("startedAt"),
        "endedAt": payload.get("endedAt"),
        "createdAt": payload.get("createdAt"),
        "updatedAt": payload.get("updatedAt"),
        "attachmentCount": len(attachments),
        "attachments": [
            {
                "id": attachment.get("id"),
                "filename": attachment.get("filename"),
                "extension": attachment.get("extension"),
                "sizeBytes": attachment.get("sizeBytes"),
            }
            for attachment in attachments
        ],
        "orderCount": len(orders),
        "orders": [summarize_retail_order(order) for order in orders],
    }


def summarize_retail_sync_list(payload: dict[str, Any]) -> dict[str, Any]:
    syncs = payload.get("results") or payload.get("retailSyncs") or []
    return {
        "totalCount": payload.get("totalCount"),
        "count": len(syncs),
        "retailSyncs": [summarize_retail_sync(item) for item in syncs],
    }


def summarize_auth_me(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": payload.get("id"),
        "email": payload.get("email"),
        "name": payload.get("name"),
        "displayName": payload.get("displayName"),
        "householdId": (payload.get("household") or {}).get("id"),
    }


def summarize_household(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": payload.get("id"),
        "name": payload.get("name"),
        "address": payload.get("address"),
        "city": payload.get("city"),
        "state": payload.get("state"),
        "zipCode": payload.get("zipCode"),
        "country": payload.get("country"),
    }


def summarize_household_members(payload: dict[str, Any]) -> dict[str, Any]:
    household = payload.get("myHousehold") or {}
    return {
        "meId": (payload.get("me") or {}).get("id"),
        "householdId": household.get("id"),
        "memberCount": len(household.get("users", [])),
        "members": summarize_collection(household.get("users", []), ["id", "name", "displayName", "householdRole"]),
    }


def summarize_household_preferences(payload: dict[str, Any]) -> dict[str, Any]:
    preferences = payload.get("householdPreferences") or {}
    return {
        "id": preferences.get("id"),
        "newTransactionsNeedReview": preferences.get("newTransactionsNeedReview"),
        "uncategorizedTransactionsNeedReview": preferences.get("uncategorizedTransactionsNeedReview"),
        "pendingTransactionsCanBeEdited": preferences.get("pendingTransactionsCanBeEdited"),
        "accountGroupOrder": preferences.get("accountGroupOrder"),
        "collaborationToolsEnabled": preferences.get("collaborationToolsEnabled"),
        "investmentTransactionsEnabled": preferences.get("investmentTransactionsEnabled"),
        "budgetSystem": payload.get("budgetSystem"),
        "budgetApplyToFutureMonthsDefault": payload.get("budgetApplyToFutureMonthsDefault"),
    }


def summarize_account_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "displayName": item.get("displayName"),
        "displayBalance": item.get("displayBalance"),
        "signedBalance": item.get("signedBalance"),
        "type": (item.get("type") or {}).get("display") or (item.get("type") or {}).get("name"),
        "subtype": ((item.get("subtype") or {}).get("display") if isinstance(item.get("subtype"), dict) else None),
        "isAsset": item.get("isAsset"),
        "isHidden": item.get("isHidden"),
        "syncDisabled": item.get("syncDisabled"),
        "includeInNetWorth": item.get("includeInNetWorth"),
        "institution": (item.get("institution") or {}).get("name"),
        "owner": (item.get("ownedByUser") or {}).get("displayName"),
        "businessEntity": (item.get("businessEntity") or {}).get("name"),
    }


def summarize_accounts_page(payload: dict[str, Any]) -> dict[str, Any]:
    summaries = payload.get("accountTypeSummaries", [])
    return {
        "hasAccounts": payload.get("hasAccounts"),
        "accountTypeSummaryCount": len(summaries),
        "accountTypeSummaries": [
            {
                "type": ((summary.get("type") or {}).get("display") or (summary.get("type") or {}).get("name")),
                "group": (summary.get("type") or {}).get("group"),
                "isAsset": summary.get("isAsset"),
                "totalDisplayBalance": summary.get("totalDisplayBalance"),
                "accountCount": len(summary.get("accounts", [])),
                "accounts": [summarize_account_item(account) for account in summary.get("accounts", [])],
            }
            for summary in summaries
        ],
        "householdPreferences": payload.get("householdPreferences"),
    }


def summarize_accounts_recent_balances(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "accounts": [
            {
                "id": item.get("id"),
                "type": ((item.get("type") or {}).get("display") or (item.get("type") or {}).get("name")),
                "group": (item.get("type") or {}).get("group"),
                "includeInNetWorth": item.get("includeInNetWorth"),
                "recentBalanceCount": len(item.get("recentBalances") or []),
                "recentBalances": item.get("recentBalances"),
            }
            for item in payload
        ],
    }


def summarize_aggregate_snapshots(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "firstDate": (payload[0] or {}).get("date") if payload else None,
        "lastDate": (payload[-1] or {}).get("date") if payload else None,
        "snapshots": summarize_collection(payload, ["date", "balance", "assetsBalance", "liabilitiesBalance"]),
    }


def summarize_display_balances(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "accounts": [
            {
                "id": item.get("id"),
                "displayBalance": item.get("displayBalance"),
                "includeInNetWorth": item.get("includeInNetWorth"),
                "type": (item.get("type") or {}).get("name"),
            }
            for item in payload
        ],
    }


def summarize_snapshots_by_account_type(payload: dict[str, Any]) -> dict[str, Any]:
    snapshots = payload.get("snapshotsByAccountType", [])
    return {
        "snapshotCount": len(snapshots),
        "accountTypeCount": len(payload.get("accountTypes", [])),
        "accountTypes": summarize_collection(payload.get("accountTypes", []), ["name", "group"]),
        "snapshots": summarize_collection(snapshots, ["accountType", "month", "balance"]),
    }


def summarize_accounts_syncing(payload: dict[str, Any]) -> dict[str, Any]:
    return {"hasAccountsSyncing": payload.get("hasAccountsSyncing")}


def summarize_account_filters(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "accountCount": len(payload.get("accounts", [])),
        "accounts": summarize_collection(payload.get("accounts", []), ["id", "displayName", "logoUrl", "icon"]),
        "userCount": len((payload.get("myHousehold") or {}).get("users", [])),
        "users": summarize_collection((payload.get("myHousehold") or {}).get("users", []), ["id", "name"]),
        "householdPreferences": payload.get("householdPreferences"),
    }


def summarize_account_types(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "accountTypes": [
            {
                "name": item.get("name"),
                "display": item.get("display"),
                "group": item.get("group"),
                "showForSyncedAccounts": item.get("showForSyncedAccounts"),
                "possibleSubtypes": summarize_collection(item.get("possibleSubtypes", []), ["name", "display"]),
            }
            for item in payload
        ],
    }


def summarize_force_refresh_account_status(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": payload.get("id"),
        "canBeForceRefreshed": payload.get("canBeForceRefreshed"),
        "hasSyncOrRecentRefreshRequest": payload.get("hasSyncOrRecentRefreshRequest"),
    }


def summarize_force_refresh_operation(payload: dict[str, Any]) -> dict[str, Any]:
    accounts = payload.get("accounts") or []
    return {
        "id": payload.get("id"),
        "state": payload.get("state"),
        "completedAccountCount": payload.get("completedAccountCount"),
        "totalAccountCount": payload.get("totalAccountCount"),
        "accounts": [
            {
                "accountId": item.get("accountId"),
                "state": item.get("state"),
                "newTransactionCount": item.get("newTransactionCount"),
                "updatedTransactionCount": item.get("updatedTransactionCount"),
                "startedAt": item.get("startedAt"),
                "completedAt": item.get("completedAt"),
                "timedOut": item.get("timedOut"),
                "errorMessage": item.get("errorMessage"),
            }
            for item in accounts
        ],
    }


def summarize_investments_accounts(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "accounts": [
            {
                "id": item.get("id"),
                "displayName": item.get("displayName"),
                "subtype": (item.get("subtype") or {}).get("display"),
                "isTaxable": item.get("isTaxable"),
                "syncDisabled": item.get("syncDisabled"),
                "includeInNetWorth": item.get("includeInNetWorth"),
            }
            for item in payload
        ],
    }


def summarize_investments_dashboard(payload: dict[str, Any]) -> dict[str, Any]:
    performance = (payload.get("portfolio") or {}).get("performance") or {}
    return {
        "totalValue": performance.get("totalValue"),
        "oneDayChangeDollars": performance.get("oneDayChangeDollars"),
        "topMovers": summarize_collection(
            performance.get("topMovers", []),
            ["id", "name", "ticker", "oneDayChangePercent", "currentPrice"],
        ),
    }


def summarize_portfolio(payload: dict[str, Any]) -> dict[str, Any]:
    performance = payload.get("performance") or {}
    aggregate_holdings = ((payload.get("aggregateHoldings") or {}).get("edges") or [])
    return {
        "totalValue": performance.get("totalValue"),
        "totalChangePercent": performance.get("totalChangePercent"),
        "totalChangeDollars": performance.get("totalChangeDollars"),
        "oneDayChangePercent": performance.get("oneDayChangePercent"),
        "historicalPointCount": len(performance.get("historicalChart", [])),
        "benchmarkCount": len(performance.get("benchmarks", [])),
        "aggregateHoldingCount": len(aggregate_holdings),
        "aggregateHoldings": [
            {
                "id": ((item.get("node") or {}).get("id")),
                "ticker": (((item.get("node") or {}).get("security") or {}).get("ticker")),
                "securityName": (((item.get("node") or {}).get("security") or {}).get("name")),
                "totalValue": ((item.get("node") or {}).get("totalValue")),
                "quantity": ((item.get("node") or {}).get("quantity")),
                "holdingCount": len(((item.get("node") or {}).get("holdings") or [])),
            }
            for item in aggregate_holdings
        ],
    }


def summarize_security_history(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "securities": [
            {
                "securityId": (item.get("security") or {}).get("id"),
                "historicalPointCount": len(item.get("historicalChart", [])),
                "firstDate": ((item.get("historicalChart") or [None])[0] or {}).get("date")
                if item.get("historicalChart")
                else None,
                "lastDate": ((item.get("historicalChart") or [None])[-1] or {}).get("date")
                if item.get("historicalChart")
                else None,
            }
            for item in payload
        ],
    }


def summarize_subscription_state(payload: dict[str, Any]) -> dict[str, Any]:
    payment_method = payload.get("paymentMethod") or {}
    active_promo_code = payload.get("activePromoCode") or {}
    return {
        "id": payload.get("id"),
        "billingPeriod": payload.get("billingPeriod"),
        "paymentSource": payload.get("paymentSource"),
        "hasPremiumEntitlement": payload.get("hasPremiumEntitlement"),
        "entitlements": payload.get("entitlements"),
        "isOnFreeTrial": payload.get("isOnFreeTrial"),
        "eligibleForTrial": payload.get("eligibleForTrial"),
        "trialEndsAt": payload.get("trialEndsAt"),
        "trialDurationDays": payload.get("trialDurationDays"),
        "plusTrialEndsAt": payload.get("plusTrialEndsAt"),
        "currentPeriodEndsAt": payload.get("currentPeriodEndsAt"),
        "nextPaymentAmount": payload.get("nextPaymentAmount"),
        "willCancelAtPeriodEnd": payload.get("willCancelAtPeriodEnd"),
        "hasStripeSubscriptionId": payload.get("hasStripeSubscriptionId"),
        "hasChargedForLifetime": payload.get("hasChargedForLifetime"),
        "hasBillingIssue": payload.get("hasBillingIssue"),
        "analyticsFreemiumSummaryStatus": payload.get("analyticsFreemiumSummaryStatus"),
        "referralCode": payload.get("referralCode"),
        "activePromoCode": active_promo_code.get("code"),
        "paymentMethodLastFour": payment_method.get("lastFour"),
        "paymentMethodBrand": payment_method.get("brand"),
        "activeSponsorshipId": (payload.get("activeSponsorship") or {}).get("id"),
        "isEligibleForCoreToPlusPromo": payload.get("isEligibleForCoreToPlusPromo"),
    }


def summarize_subscription_plans(plans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "name": item.get("name"),
            "period": item.get("period"),
            "tier": item.get("tier"),
            "pricePerPeriodDollars": item.get("pricePerPeriodDollars"),
            "discountedPricePerPeriodDollars": item.get("discountedPricePerPeriodDollars"),
            "stripeId": item.get("stripeId"),
            "newTrialEndsAt": item.get("newTrialEndsAt"),
            "requirePaymentMethod": item.get("requirePaymentMethod"),
            "sponsoredBy": (item.get("sponsoredBy") or {}).get("name"),
        }
        for item in plans
    ]


def summarize_subscription_payload(payload: dict[str, Any]) -> dict[str, Any]:
    invoices = payload.get("invoices") or []
    constants = payload.get("constants") or {}
    return {
        "subscription": summarize_subscription_state(payload.get("subscription") or {}),
        "creditBalance": payload.get("creditBalance"),
        "monthlyPriceDollars": constants.get("monthlyPriceDollars"),
        "invoiceCount": len(invoices),
        "invoices": [
            {
                "id": item.get("id"),
                "date": item.get("date"),
                "amount": item.get("amount"),
                "receiptUrl": item.get("receiptUrl"),
            }
            for item in invoices
        ],
    }


def summarize_subscription_modal(payload: dict[str, Any]) -> dict[str, Any]:
    offering = payload.get("subscriptionOffering") or {}
    plus_upgrade_trial = payload.get("plusUpgradeTrial") or {}
    return {
        "subscription": summarize_subscription_state(payload.get("subscription") or {}),
        "plusUpgradeTrial": {
            "trialDays": plus_upgrade_trial.get("trialDays"),
            "isEligible": plus_upgrade_trial.get("isEligible"),
        },
        "subscriptionOffering": {
            "promoCodeError": offering.get("promoCodeError"),
            "promoCodeDescription": offering.get("promoCodeDescription"),
            "promoCodeDuration": offering.get("promoCodeDuration"),
            "promoCodeDurationInMonths": offering.get("promoCodeDurationInMonths"),
            "planCount": len(offering.get("plans") or []),
            "plans": summarize_subscription_plans(offering.get("plans") or []),
        },
    }


def summarize_feature_entitlement_params(payload: dict[str, Any]) -> dict[str, Any]:
    entitlement_params = payload.get("entitlementParams") or {}
    return {
        "subscriptionId": payload.get("id"),
        "featureCount": len(entitlement_params.get("features") or []),
        "features": summarize_collection(entitlement_params.get("features", []), ["feature", "requiredEntitlements"]),
        "constantCount": len(entitlement_params.get("constants") or []),
        "constants": summarize_collection(
            entitlement_params.get("constants", []),
            ["entitlement", "maxCredentials", "maxTransactionRules"],
        ),
    }


def summarize_gifted_subscriptions(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "giftedSubscriptions": summarize_collection(
            payload,
            ["id", "createdAt", "recipientName", "promoCode", "status", "redeemedAt"],
        ),
    }


def summarize_referral_settings(payload: dict[str, Any]) -> dict[str, Any]:
    constants = payload.get("constants") or {}
    legacy_statistics = payload.get("legacyReferralStatistics") or {}
    referral_statistics = payload.get("referralStatistics") or {}
    redemptions = payload.get("referralRedemptions") or []
    return {
        "constants": {
            "referralAnnualRewardLimitUsd": constants.get("referralAnnualRewardLimitUsd"),
            "referralV2ProgramLaunchDate": constants.get("referralV2ProgramLaunchDate"),
        },
        "legacyReferralStatistics": legacy_statistics,
        "referralStatistics": referral_statistics,
        "redemptionCount": len(redemptions),
        "referralRedemptions": summarize_collection(
            redemptions,
            ["id", "creditsEarned", "creditsEarnedAt"],
        ),
    }


def summarize_user_profile_flags(payload: dict[str, Any]) -> dict[str, Any]:
    return payload


def summarize_dashboard_config(payload: dict[str, Any]) -> dict[str, Any]:
    dashboard_config = ((payload.get("preferences") or {}).get("dashboardConfig") or {})
    web_config = dashboard_config.get("web") or {}
    mobile_config = dashboard_config.get("mobile") or {}
    return {
        "householdId": payload.get("id"),
        "web": {
            "layout": web_config.get("layout"),
            "widgetCount": len(web_config.get("widgets") or []),
            "widgets": web_config.get("widgets"),
        },
        "mobile": {
            "layout": mobile_config.get("layout"),
            "widgetCount": len(mobile_config.get("widgets") or []),
            "widgets": mobile_config.get("widgets"),
        },
    }


def summarize_sidebar_data(payload: dict[str, Any]) -> dict[str, Any]:
    me = payload.get("me") or {}
    offering = payload.get("subscriptionOffering") or {}
    return {
        "me": {
            "id": me.get("id"),
            "displayName": me.get("displayName"),
            "email": me.get("email"),
            "sponsorAccountName": me.get("sponsorAccountName"),
        },
        "subscription": summarize_subscription_state(payload.get("subscription") or {}),
        "subscriptionOffering": {
            "promoCodeError": offering.get("promoCodeError"),
            "promoCodeDescription": offering.get("promoCodeDescription"),
            "planCount": len(offering.get("plans") or []),
            "plans": summarize_collection(offering.get("plans", []), ["period", "pricePerPeriodDollars"]),
        },
    }


def summarize_household_member_settings(payload: dict[str, Any]) -> dict[str, Any]:
    household = payload.get("myHousehold") or {}
    users = household.get("users") or []
    invites = payload.get("householdInvites") or []
    access_grants = payload.get("householdAccessGrants") or []
    return {
        "me": {
            "id": (payload.get("me") or {}).get("id"),
            "householdRole": (payload.get("me") or {}).get("householdRole"),
        },
        "householdId": household.get("id"),
        "userCount": len(users),
        "users": [
            {
                "id": item.get("id"),
                "displayName": item.get("displayName"),
                "email": item.get("email"),
                "householdRole": item.get("householdRole"),
                "hasMfaOn": item.get("hasMfaOn"),
            }
            for item in users
        ],
        "inviteCount": len(invites),
        "invites": summarize_collection(invites, ["id", "invitedEmail", "createdAt", "isRevoked", "usedAt"]),
        "accessGrantCount": len(access_grants),
        "accessGrants": summarize_collection(access_grants, ["id", "toEmail", "toName", "createdAt", "expiresAt"]),
    }


def summarize_security_settings(payload: dict[str, Any]) -> dict[str, Any]:
    me = payload.get("me") or {}
    return {
        "me": {
            "id": me.get("id"),
            "email": me.get("email"),
            "hasMfaOn": me.get("hasMfaOn"),
            "isVerified": me.get("isVerified"),
            "hasPassword": me.get("hasPassword"),
            "externalAuthProviders": summarize_collection(
                me.get("externalAuthProviders", []),
                ["provider", "email"],
            ),
            "pendingEmailUpdateVerification": (me.get("pendingEmailUpdateVerification") or {}).get("email"),
            "activeSupportAccountAccessGrant": me.get("activeSupportAccountAccessGrant"),
        },
        "userDiscordData": payload.get("userDiscordData"),
    }


def summarize_notification_preferences(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "notificationPreferences": summarize_collection(
            payload,
            [
                "id",
                "group",
                "type",
                "title",
                "description",
                "emailEnabled",
                "pushEnabled",
                "inAppEnabled",
            ],
        ),
    }


def summarize_review_summary_by_user(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "byNeedsReviewByUser": [
            {
                "userId": ((item.get("groupBy") or {}).get("needsReviewByUser") or {}).get("id"),
                "userName": ((item.get("groupBy") or {}).get("needsReviewByUser") or {}).get("name"),
                "count": (item.get("summary") or {}).get("count"),
            }
            for item in payload
        ],
    }


def summarize_business_entities_banner_profile(payload: dict[str, Any]) -> dict[str, Any]:
    return payload


def summarize_business_entities(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "businessEntities": [
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "description": item.get("description"),
                "structure": item.get("structure"),
                "accountsCount": item.get("accountsCount"),
                "transactionsCount": item.get("transactionsCount"),
            }
            for item in payload
        ],
    }


def summarize_planning_payload(payload: dict[str, Any]) -> dict[str, Any]:
    budget_data = payload.get("budgetData") or {}
    budget_status = payload.get("budgetStatus") or {}
    return {
        "budgetSystem": payload.get("budgetSystem"),
        "budgetStatus": {
            "hasBudget": budget_status.get("hasBudget"),
            "hasTransactions": budget_status.get("hasTransactions"),
            "willCreateBudgetFromEmptyDefaultCategories": budget_status.get("willCreateBudgetFromEmptyDefaultCategories"),
        }
        if budget_status
        else None,
        "categoryGroupCount": len(payload.get("categoryGroups", [])),
        "goalCount": len(payload.get("goalsV2", [])),
        "savingsGoalMonthlyBudgetAmountCount": len(payload.get("savingsGoalMonthlyBudgetAmounts", [])),
        "budgetData": {
            "monthlyAmountsByCategoryCount": len(budget_data.get("monthlyAmountsByCategory", [])),
            "monthlyAmountsByCategoryGroupCount": len(budget_data.get("monthlyAmountsByCategoryGroup", [])),
            "monthlyAmountsForFlexExpenseCount": len(budget_data.get("monthlyAmountsForFlexExpense", [])),
            "totalsByMonthCount": len(budget_data.get("totalsByMonth", [])),
        },
    }


def summarize_goal_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "type": item.get("type"),
        "status": item.get("status"),
        "priority": item.get("priority"),
        "currentBalance": item.get("currentBalance"),
        "targetAmount": item.get("targetAmount"),
        "targetDate": item.get("targetDate"),
        "plannedMonthlyContribution": item.get("plannedMonthlyContribution"),
        "progress": item.get("progress"),
        "allocationCount": len(item.get("allocationAmountsByAccount", [])),
    }


def summarize_goals_list(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "goals": [summarize_goal_item(item) for item in payload],
    }


def summarize_goals_with_balances(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "goalsBalanceThisMonth": payload.get("goalsBalanceThisMonth"),
        "currentTotalBalanceForGoals": payload.get("currentTotalBalanceForGoals"),
        "goals": [summarize_goal_item(item) for item in payload.get("savingsGoals", [])],
    }


def summarize_goal_account(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": payload.get("id"),
        "displayName": payload.get("displayName"),
        "displayBalance": payload.get("displayBalance"),
        "availableBalanceForGoalsUnmemoized": payload.get("availableBalanceForGoalsUnmemoized"),
        "includeInGoalContributions": payload.get("includeInGoalContributions"),
        "goalAllocatedAmount": payload.get("goalAllocatedAmount"),
        "linkedGoalId": (payload.get("linkedGoal") or {}).get("id"),
        "subtype": (payload.get("subtype") or {}).get("display"),
    }


def summarize_goals_dashboard(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "goals": [
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "type": item.get("type"),
                "priority": item.get("priority"),
                "currentAmount": item.get("currentAmount"),
                "completionPercent": item.get("completionPercent"),
                "allocationCount": len(item.get("accountAllocations", [])),
            }
            for item in payload
        ],
    }


def summarize_legacy_goals_migration(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "migratedToSavingsGoals": payload.get("migratedToSavingsGoals"),
        "legacyGoalMigrationCount": len(payload.get("legacyGoalsMigrationData", [])),
        "debtAccountCount": len(payload.get("debtAccounts", [])),
        "debtAccounts": summarize_collection(
            payload.get("debtAccounts", []),
            ["id", "displayName", "displayBalance", "minimumPayment", "plannedPayment", "excludeFromDebtPaydown"],
        ),
    }


def summarize_recurring_streams(payload: list[dict[str, Any]]) -> dict[str, Any]:
    streams = [item.get("stream") or {} for item in payload]
    return {
        "count": len(streams),
        "streams": [
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "frequency": item.get("frequency"),
                "amount": item.get("amount"),
                "reviewStatus": item.get("reviewStatus"),
                "recurringType": item.get("recurringType"),
                "dayOfTheMonth": item.get("dayOfTheMonth"),
                "isApproximate": item.get("isApproximate"),
                "merchantId": (item.get("merchant") or {}).get("id"),
                "liabilityAccountId": (((item.get("creditReportLiabilityAccount") or {}).get("account") or {}).get("id")),
            }
            for item in streams
        ],
    }


def summarize_aggregated_recurring(payload: dict[str, Any]) -> dict[str, Any]:
    groups = payload.get("groups", [])
    return {
        "groupCount": len(groups),
        "aggregatedSummary": payload.get("aggregatedSummary"),
        "groups": [
            {
                "status": (item.get("groupBy") or {}).get("status"),
                "resultCount": len(item.get("results", [])),
                "summary": item.get("summary"),
            }
            for item in groups
        ],
    }


def summarize_dashboard_upcoming_recurring(payload: dict[str, Any]) -> dict[str, Any]:
    items = payload.get("recurringTransactionItems", [])
    return {
        "remainingDueAmount": (payload.get("recurringRemainingDue") or {}).get("amount"),
        "itemCount": len(items),
        "items": [
            {
                "streamId": (item.get("stream") or {}).get("id"),
                "name": (item.get("stream") or {}).get("name"),
                "frequency": (item.get("stream") or {}).get("frequency"),
                "date": item.get("date"),
                "amount": item.get("amount"),
                "isPast": item.get("isPast"),
                "accountId": (item.get("account") or {}).get("id"),
            }
            for item in items
        ],
    }


def summarize_recurring_paused_banner(payload: dict[str, Any]) -> dict[str, Any]:
    spinwheel_user = payload.get("spinwheelUser") or {}
    return {
        "isBillSyncTrackingEnabled": spinwheel_user.get("isBillSyncTrackingEnabled"),
    }


def summarize_institution_notice_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "institutionId": item.get("institutionId"),
        "severity": item.get("severity"),
        "dataProvider": item.get("dataProvider"),
        "startsAt": item.get("startsAt"),
        "showAsWarnBeforeConnecting": item.get("showAsWarnBeforeConnecting"),
        "publicMessage": item.get("publicMessage"),
    }


def summarize_institution_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "preferredDataProvider": item.get("preferred_data_provider"),
        "active": item.get("active"),
        "popularity": item.get("popularity"),
        "hasIssuesReported": item.get("has_issues_reported"),
        "hasIssuesReportedMessage": item.get("has_issues_reported_message"),
        "newConnectionsDisabled": item.get("new_connections_disabled"),
        "noticeCount": len(item.get("notices") or []),
        "dataProviderMetrics": [metric.get("data_provider") for metric in item.get("data_provider_metrics", [])],
    }


def summarize_accounts_institution_settings(payload: dict[str, Any]) -> dict[str, Any]:
    credentials = payload.get("credentials", [])
    accounts = payload.get("accounts", [])
    return {
        "credentialCount": len(credentials),
        "credentials": [
            {
                "id": item.get("id"),
                "institution": ((item.get("institution") or {}).get("name")),
                "dataProvider": item.get("dataProvider"),
                "updateRequired": item.get("updateRequired"),
                "displayLastUpdatedAt": item.get("displayLastUpdatedAt"),
                "syncDisabledAt": item.get("syncDisabledAt"),
                "syncDisabledReason": item.get("syncDisabledReason"),
                "disconnectedFromDataProviderAt": item.get("disconnectedFromDataProviderAt"),
            }
            for item in credentials
        ],
        "accountCount": len(accounts),
        "accounts": [
            {
                "id": item.get("id"),
                "displayName": item.get("displayName"),
                "subtype": ((item.get("subtype") or {}).get("display")),
                "mask": item.get("mask"),
                "deletedAt": item.get("deletedAt"),
                "hideFromList": item.get("hideFromList"),
                "credentialId": (item.get("credential") or {}).get("id"),
                "owner": (item.get("ownedByUser") or {}).get("displayName"),
                "displayLastUpdatedAt": item.get("displayLastUpdatedAt"),
            }
            for item in accounts
        ],
        "subscription": payload.get("subscription"),
    }


def summarize_accounts_institutions(payload: dict[str, Any]) -> dict[str, Any]:
    items = payload.get("items", [])
    return {
        "type": payload.get("type"),
        "count": payload.get("count"),
        "offset": payload.get("offset"),
        "nextOffset": payload.get("next_offset"),
        "institutions": [summarize_institution_item(item) for item in items],
    }


def summarize_accounts_institution(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": payload.get("type"),
        "id": payload.get("id"),
        "institution": summarize_institution_item(payload.get("data") or {}),
    }


def summarize_rules(payload: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(payload),
        "rules": [
            {
                "id": item.get("id"),
                "order": item.get("order"),
                "merchantCriteriaUseOriginalStatement": item.get("merchantCriteriaUseOriginalStatement"),
                "categoryCount": len(item.get("categories", [])),
                "accountCount": len(item.get("accounts", [])),
                "tagActionCount": len(item.get("addTagsAction") or []),
                "recentApplicationCount": item.get("recentApplicationCount"),
                "lastAppliedAt": item.get("lastAppliedAt"),
                "setMerchantAction": (item.get("setMerchantAction") or {}).get("name"),
                "setCategoryAction": (item.get("setCategoryAction") or {}).get("name"),
                "reviewStatusAction": item.get("reviewStatusAction"),
                "setHideFromReportsAction": item.get("setHideFromReportsAction"),
            }
            for item in payload
        ],
    }


def summarize_rule_preview(payload: dict[str, Any]) -> dict[str, Any]:
    results = payload.get("results") or []
    return {
        "totalCount": payload.get("totalCount"),
        "resultCount": len(results),
        "results": [
            {
                "transactionId": ((item.get("transaction") or {}).get("id")),
                "date": ((item.get("transaction") or {}).get("date")),
                "amount": ((item.get("transaction") or {}).get("amount")),
                "merchant": (((item.get("transaction") or {}).get("merchant") or {}).get("name")),
                "currentCategory": (((item.get("transaction") or {}).get("category") or {}).get("name")),
                "newName": item.get("newName"),
                "newCategory": ((item.get("newCategory") or {}).get("name")),
                "newOwner": ((item.get("newOwnerUser") or {}).get("displayName")),
                "newOwnerIsJoint": item.get("newOwnerIsJoint"),
                "newHideFromReports": item.get("newHideFromReports"),
                "newTags": [tag.get("name") for tag in (item.get("newTags") or [])],
                "newGoal": ((item.get("newGoal") or {}).get("name")),
                "newBusinessEntity": ((item.get("newBusinessEntity") or {}).get("name")),
                "newBusinessEntityIsUnassigned": item.get("newBusinessEntityIsUnassigned"),
                "newSplitTransactions": item.get("newSplitTransactions"),
            }
            for item in results
        ],
    }


def summarize_cash_flow_dashboard(payload: dict[str, Any]) -> dict[str, Any]:
    by_day = payload.get("byDay") or []
    return {
        "dayCount": len(by_day),
        "days": [
            {
                "day": (item.get("groupBy") or {}).get("day"),
                "sumExpense": (item.get("summary") or {}).get("sumExpense"),
            }
            for item in by_day
        ],
    }


def summarize_cash_flow_entity_aggregates(payload: dict[str, Any]) -> dict[str, Any]:
    summary_items = payload.get("summary") or []
    overall_summary = ((summary_items[0] or {}).get("summary") if summary_items else None)
    return {
        "categoryCount": len(payload.get("byCategory") or []),
        "categoryGroupCount": len(payload.get("byCategoryGroup") or []),
        "merchantCount": len(payload.get("byMerchant") or []),
        "summary": overall_summary,
        "categories": [
            {
                "id": ((item.get("groupBy") or {}).get("category") or {}).get("id"),
                "name": ((item.get("groupBy") or {}).get("category") or {}).get("name"),
                "sum": (item.get("summary") or {}).get("sum"),
            }
            for item in (payload.get("byCategory") or [])
        ],
        "categoryGroups": [
            {
                "id": ((item.get("groupBy") or {}).get("categoryGroup") or {}).get("id"),
                "name": ((item.get("groupBy") or {}).get("categoryGroup") or {}).get("name"),
                "type": ((item.get("groupBy") or {}).get("categoryGroup") or {}).get("type"),
                "sum": (item.get("summary") or {}).get("sum"),
            }
            for item in (payload.get("byCategoryGroup") or [])
        ],
        "merchants": [
            {
                "id": ((item.get("groupBy") or {}).get("merchant") or {}).get("id"),
                "name": ((item.get("groupBy") or {}).get("merchant") or {}).get("name"),
                "sumIncome": (item.get("summary") or {}).get("sumIncome"),
                "sumExpense": (item.get("summary") or {}).get("sumExpense"),
            }
            for item in (payload.get("byMerchant") or [])
        ],
    }


def summarize_cash_flow_timeframe_aggregates(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "yearCount": len(payload.get("byYear") or []),
        "monthCount": len(payload.get("byMonth") or []),
        "quarterCount": len(payload.get("byQuarter") or []),
        "years": [
            {
                "year": (item.get("groupBy") or {}).get("year"),
                "summary": item.get("summary"),
            }
            for item in (payload.get("byYear") or [])
        ],
        "months": [
            {
                "month": (item.get("groupBy") or {}).get("month"),
                "summary": item.get("summary"),
            }
            for item in (payload.get("byMonth") or [])
        ],
        "quarters": [
            {
                "quarter": (item.get("groupBy") or {}).get("quarter"),
                "summary": item.get("summary"),
            }
            for item in (payload.get("byQuarter") or [])
        ],
    }


def summarize_report_group(item: dict[str, Any]) -> dict[str, Any]:
    group_by = item.get("groupBy") or {}
    entity_type = None
    entity_name = None
    for key in ("category", "categoryGroup", "merchant", "businessEntity", "budgetVariability"):
        value = group_by.get(key)
        if isinstance(value, dict):
            entity_type = key
            entity_name = value.get("name")
            break
    return {
        "entityType": entity_type,
        "entityName": entity_name,
        "date": group_by.get("date"),
        "summary": {
            "sum": (item.get("summary") or {}).get("sum"),
            "count": (item.get("summary") or {}).get("count"),
            "sumIncome": (item.get("summary") or {}).get("sumIncome"),
            "sumExpense": (item.get("summary") or {}).get("sumExpense"),
            "savingsRate": (item.get("summary") or {}).get("savingsRate"),
            "first": (item.get("summary") or {}).get("first"),
            "last": (item.get("summary") or {}).get("last"),
        },
    }


def summarize_reports_data(payload: dict[str, Any]) -> dict[str, Any]:
    reports = payload.get("reports") or {}
    if isinstance(reports, list):
        group_items = reports
        report_summary = None
    else:
        group_items = reports.get("groupBy", [])
        report_summary = reports.get("summary")
    aggregates = payload.get("aggregates") or {}
    if isinstance(aggregates, list):
        aggregate_summary = ((aggregates[0] or {}).get("summary") if aggregates else None)
    else:
        aggregate_summary = aggregates.get("summary")
    return {
        "groupCount": len(group_items),
        "reportSummary": report_summary,
        "aggregateSummary": aggregate_summary,
        "groups": [summarize_report_group(item) for item in group_items],
    }


def summarize_identity(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": payload.get("id"),
        "name": payload.get("name"),
        "displayName": payload.get("displayName"),
        "email": payload.get("email"),
    }


def output_result(value: Any, *, details: bool = False, summary_kind: str | None = None) -> None:
    if details:
        print_json(value)
        return

    summary = value
    if summary_kind == "auth_me" and isinstance(value, dict):
        summary = summarize_auth_me(value)
    elif summary_kind == "household" and isinstance(value, dict):
        summary = summarize_household(value)
    elif summary_kind == "household_members" and isinstance(value, dict):
        summary = summarize_household_members(value)
    elif summary_kind == "household_preferences" and isinstance(value, dict):
        summary = summarize_household_preferences(value)
    elif summary_kind == "accounts_page" and isinstance(value, dict):
        summary = summarize_accounts_page(value)
    elif summary_kind == "accounts_recent_balances" and isinstance(value, list):
        summary = summarize_accounts_recent_balances(value)
    elif summary_kind == "aggregate_snapshots" and isinstance(value, list):
        summary = summarize_aggregate_snapshots(value)
    elif summary_kind == "display_balances" and isinstance(value, list):
        summary = summarize_display_balances(value)
    elif summary_kind == "snapshots_by_account_type" and isinstance(value, dict):
        summary = summarize_snapshots_by_account_type(value)
    elif summary_kind == "accounts_list" and isinstance(value, list):
        summary = {"count": len(value), "accounts": [summarize_account_item(item) for item in value]}
    elif summary_kind == "accounts_syncing" and isinstance(value, dict):
        summary = summarize_accounts_syncing(value)
    elif summary_kind == "accounts_filters" and isinstance(value, dict):
        summary = summarize_account_filters(value)
    elif summary_kind == "account_types" and isinstance(value, list):
        summary = summarize_account_types(value)
    elif summary_kind == "force_refresh_account_status" and isinstance(value, dict):
        summary = summarize_force_refresh_account_status(value)
    elif summary_kind == "force_refresh_operation" and isinstance(value, dict):
        summary = summarize_force_refresh_operation(value)
    elif summary_kind == "accounts_notices" and isinstance(value, list):
        summary = {
            "count": len(value),
            "notices": [summarize_institution_notice_item(item) for item in value],
        }
    elif summary_kind == "accounts_institution_settings" and isinstance(value, dict):
        summary = summarize_accounts_institution_settings(value)
    elif summary_kind == "accounts_institutions" and isinstance(value, dict):
        summary = summarize_accounts_institutions(value)
    elif summary_kind == "accounts_institution" and isinstance(value, dict):
        summary = summarize_accounts_institution(value)
    elif summary_kind == "subscription_state" and isinstance(value, dict):
        summary = summarize_subscription_state(value)
    elif summary_kind == "subscription" and isinstance(value, dict):
        summary = summarize_subscription_payload(value)
    elif summary_kind == "subscription_modal" and isinstance(value, dict):
        summary = summarize_subscription_modal(value)
    elif summary_kind == "feature_entitlement_params" and isinstance(value, dict):
        summary = summarize_feature_entitlement_params(value)
    elif summary_kind == "gifted_subscriptions" and isinstance(value, list):
        summary = summarize_gifted_subscriptions(value)
    elif summary_kind == "referral_settings" and isinstance(value, dict):
        summary = summarize_referral_settings(value)
    elif summary_kind == "user_profile_flags" and isinstance(value, dict):
        summary = summarize_user_profile_flags(value)
    elif summary_kind == "dashboard_config" and isinstance(value, dict):
        summary = summarize_dashboard_config(value)
    elif summary_kind == "sidebar_data" and isinstance(value, dict):
        summary = summarize_sidebar_data(value)
    elif summary_kind == "household_member_settings" and isinstance(value, dict):
        summary = summarize_household_member_settings(value)
    elif summary_kind == "security_settings" and isinstance(value, dict):
        summary = summarize_security_settings(value)
    elif summary_kind == "notification_preferences" and isinstance(value, list):
        summary = summarize_notification_preferences(value)
    elif summary_kind == "review_summary_by_user" and isinstance(value, list):
        summary = summarize_review_summary_by_user(value)
    elif summary_kind == "business_entities_banner_profile" and isinstance(value, dict):
        summary = summarize_business_entities_banner_profile(value)
    elif summary_kind == "business_entities" and isinstance(value, list):
        summary = summarize_business_entities(value)
    elif summary_kind == "planning" and isinstance(value, dict):
        summary = summarize_planning_payload(value)
    elif summary_kind == "investments_accounts" and isinstance(value, list):
        summary = summarize_investments_accounts(value)
    elif summary_kind == "investments_dashboard" and isinstance(value, dict):
        summary = summarize_investments_dashboard(value)
    elif summary_kind == "portfolio" and isinstance(value, dict):
        summary = summarize_portfolio(value)
    elif summary_kind == "security_history" and isinstance(value, list):
        summary = summarize_security_history(value)
    elif summary_kind == "goals" and isinstance(value, list):
        summary = summarize_goals_list(value)
    elif summary_kind == "goals_with_balances" and isinstance(value, dict):
        summary = summarize_goals_with_balances(value)
    elif summary_kind == "goal_account" and isinstance(value, dict):
        summary = summarize_goal_account(value)
    elif summary_kind == "goals_dashboard" and isinstance(value, list):
        summary = summarize_goals_dashboard(value)
    elif summary_kind == "legacy_goals_migration" and isinstance(value, dict):
        summary = summarize_legacy_goals_migration(value)
    elif summary_kind == "recurring_streams" and isinstance(value, list):
        summary = summarize_recurring_streams(value)
    elif summary_kind == "aggregated_recurring" and isinstance(value, dict):
        summary = summarize_aggregated_recurring(value)
    elif summary_kind == "dashboard_upcoming_recurring" and isinstance(value, dict):
        summary = summarize_dashboard_upcoming_recurring(value)
    elif summary_kind == "recurring_paused_banner" and isinstance(value, dict):
        summary = summarize_recurring_paused_banner(value)
    elif summary_kind == "rules" and isinstance(value, list):
        summary = summarize_rules(value)
    elif summary_kind == "rule_preview" and isinstance(value, dict):
        summary = summarize_rule_preview(value)
    elif summary_kind == "cash_flow_dashboard" and isinstance(value, dict):
        summary = summarize_cash_flow_dashboard(value)
    elif summary_kind == "cash_flow_entity_aggregates" and isinstance(value, dict):
        summary = summarize_cash_flow_entity_aggregates(value)
    elif summary_kind == "cash_flow_timeframe_aggregates" and isinstance(value, dict):
        summary = summarize_cash_flow_timeframe_aggregates(value)
    elif summary_kind == "reports_data" and isinstance(value, dict):
        summary = summarize_reports_data(value)
    elif summary_kind == "transactions_list" and isinstance(value, dict):
        summary = summarize_transactions_list(value)
    elif summary_kind == "transaction_detail" and isinstance(value, dict):
        summary = summarize_transaction_detail(value)
    elif summary_kind == "transaction_filters" and isinstance(value, dict):
        summary = summarize_filters(value)
    elif summary_kind == "transaction_filters_metadata" and isinstance(value, dict):
        summary = summarize_filters_metadata(value)
    elif summary_kind == "categories" and isinstance(value, dict):
        summary = summarize_categories(value)
    elif summary_kind == "tags" and isinstance(value, list):
        summary = summarize_tags(value)
    elif summary_kind == "merchants" and isinstance(value, list):
        summary = summarize_merchants(value)
    elif summary_kind == "attachment_upload_info" and isinstance(value, dict):
        summary = summarize_attachment_upload_info(value)
    elif summary_kind == "attachment" and isinstance(value, dict):
        summary = summarize_attachment(value)
    elif summary_kind == "retail_sync" and isinstance(value, dict):
        summary = summarize_retail_sync(value)
    elif summary_kind == "retail_sync_list" and isinstance(value, dict):
        summary = summarize_retail_sync_list(value)
    elif summary_kind == "mutation" and isinstance(value, dict):
        summary = summarize_mutation_payload(value)
    print_json(summary)


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
