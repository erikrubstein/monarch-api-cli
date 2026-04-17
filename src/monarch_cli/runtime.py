from __future__ import annotations

import json
from getpass import getpass
from pathlib import Path
from typing import Any

from monarch_api import MonarchClient, MonarchHTTPError, MonarchMfaRequiredError

from .style import BOLD, BLUE, CYAN, DIM, GREEN, MAGENTA, RED, YELLOW, color

SESSION_DIR = Path.home() / ".monarch-api-cli"
SESSION_PATH = SESSION_DIR / "monarch_session.json"
LEGACY_SESSION_DIR = Path.home() / ".monarch-cli"
LEGACY_SESSION_PATH = LEGACY_SESSION_DIR / "monarch_session.json"

def prompt(text: str) -> str:
    return input(color(text, BOLD, BLUE)).strip()


def ensure_session_dir() -> None:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)


def render_value(value: Any, indent: int = 0) -> str:
    spacing = "  " * indent
    next_spacing = "  " * (indent + 1)

    if isinstance(value, dict):
        if not value:
            return color("{}", DIM)
        lines = [color("{", DIM)]
        items = list(value.items())
        for index, (key, item) in enumerate(items):
            comma = "," if index < len(items) - 1 else ""
            rendered = render_value(item, indent + 1)
            lines.append(f"{next_spacing}{color(json.dumps(str(key)), BLUE)}: {rendered}{color(comma, DIM) if comma else ''}")
        lines.append(f"{spacing}{color('}', DIM)}")
        return "\n".join(lines)

    if isinstance(value, list):
        if not value:
            return color("[]", DIM)
        lines = [color("[", DIM)]
        for index, item in enumerate(value):
            comma = "," if index < len(value) - 1 else ""
            rendered = render_value(item, indent + 1)
            lines.append(f"{next_spacing}{rendered}{color(comma, DIM) if comma else ''}")
        lines.append(f"{spacing}{color(']', DIM)}")
        return "\n".join(lines)

    if isinstance(value, str):
        return color(json.dumps(value), GREEN)
    if isinstance(value, bool):
        return color("true" if value else "false", MAGENTA)
    if value is None:
        return color("null", DIM)
    return color(str(value), CYAN)


def print_json(value: Any) -> None:
    print(render_value(value))


def print_info(message: str) -> None:
    print(color(message, GREEN))


def print_warning(message: str) -> None:
    print(color(message, YELLOW))


def print_error(message: str) -> None:
    print(color(message, RED, BOLD))


def load_json_file(path: str | None) -> Any:
    if not path:
        return None
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(color(f"JSON file not found: {path}", RED, BOLD)) from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(color(f"Invalid JSON in {path}: {exc}", RED, BOLD)) from exc


def load_json_object_file(path: str | None, context: str) -> dict[str, Any] | None:
    payload = load_json_file(path)
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise SystemExit(color(f"{context} must be a JSON object.", RED, BOLD))
    return payload


def load_json_list_file(path: str | None, context: str) -> list[Any] | None:
    payload = load_json_file(path)
    if payload is None:
        return None
    if not isinstance(payload, list):
        raise SystemExit(color(f"{context} must be a JSON array.", RED, BOLD))
    return payload


def merge_payload(base: dict[str, Any] | None, overrides: dict[str, Any]) -> dict[str, Any]:
    payload = dict(base or {})
    for key, value in overrides.items():
        if value is not None:
            payload[key] = value
    return payload


def require_keys(payload: dict[str, Any], keys: list[str], context: str) -> dict[str, Any]:
    missing = [key for key in keys if payload.get(key) in (None, "")]
    if missing:
        raise SystemExit(color(f"{context} is missing required field(s): {', '.join(missing)}", RED, BOLD))
    return payload


def bool_override(true_flag: bool, false_flag: bool) -> bool | None:
    if true_flag and false_flag:
        raise SystemExit(color("Conflicting boolean flags were provided.", RED, BOLD))
    if true_flag:
        return True
    if false_flag:
        return False
    return None


def parse_id_list(value: list[str] | None) -> list[str]:
    return value or []


def interactive_login(client: MonarchClient) -> dict[str, Any]:
    username = prompt("Monarch email: ")
    password = getpass("Monarch password: ")
    totp: str | None = None

    while True:
        try:
            ensure_session_dir()
            client.auth.login(username=username, password=password, totp=totp)
            client.auth.save_session(SESSION_PATH)
            me = client.auth.get_me()
            print_info(f"Saved session to {SESSION_PATH}")
            return me
        except MonarchMfaRequiredError:
            totp = prompt("Authenticator code: ")
            if not totp:
                print_warning("A TOTP code is required.")
        except MonarchHTTPError as exc:
            print_error(f"Login failed: {exc}")
            username = prompt("Monarch email: ")
            password = getpass("Monarch password: ")
            totp = None


def ensure_authenticated(client: MonarchClient) -> dict[str, Any]:
    for path in (SESSION_PATH, LEGACY_SESSION_PATH):
        if not path.exists():
            continue
        try:
            client.auth.load_session(path)
            me = client.auth.get_me()
            if path != SESSION_PATH:
                ensure_session_dir()
                client.auth.save_session(SESSION_PATH)
            return me
        except Exception:
            path.unlink(missing_ok=True)
            print_warning(f"Saved session at {path} is missing or expired.")
    return interactive_login(client)
