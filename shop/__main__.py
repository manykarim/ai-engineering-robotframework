"""The shop helper: ``uv run python -m shop <command>`` (spec: workshop/shop-access).

    status          version, space, and the presets that hold in the space
    presets         the preset names the shop offers
    preset NAME     apply a preset in the current space
    reset           reset the current space: its flags, cart and runtime orders
    wait            wait until the shop answers its health check

Every request carries the space from SHOP_SPACE. Output never names individual
planted-bug flags, and ``presets`` prints no descriptions: the shop's own
descriptions say which behaviours some presets break, which is what the
workshop's bug hunt and healing triage ask participants to find out.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request

from shop.config import USER_AGENT, load

TIMEOUT = 15


class ShopError(Exception):
    pass


def request(settings, method: str, path: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode()
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT, **settings.headers()}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(settings.url + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            return json.loads(response.read() or b"{}")
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")[:300]
        raise ShopError(f"{method} {path} answered HTTP {error.code}: {detail}") from None
    except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
        reason = getattr(error, "reason", error)
        raise ShopError(f"nothing answers at {settings.url} ({reason}). Start the local shop with "
                        "`docker compose -f shop/compose.yaml up -d`, or check SHOP_URL.") from None


def presets_that_hold(presets: dict, flags: dict) -> list[str]:
    """Every preset whose settings all hold. Presets are partial and compose,
    so several can hold at once - `clean` and `stage1` both hold after a reset."""
    return [name for name, preset in presets.items()
            if all(flags.get(key) == value for key, value in preset["flags"].items())]


def cmd_status(settings) -> None:
    health = request(settings, "GET", "/health")
    status = request(settings, "GET", "/api/workshop/status")
    presets = request(settings, "GET", "/api/workshop/presets")["presets"]
    holding = presets_that_hold(presets, status.get("all_flags", {}))
    print(f"shop     {settings.url}  (version {health.get('version', '?')})")
    print(f"space    {status.get('space', settings.space or 'default')}")
    print(f"presets  {', '.join(holding) if holding else 'custom'}")


def cmd_presets(settings) -> None:
    for name in request(settings, "GET", "/api/workshop/presets")["presets"]:
        print(name)


def require_writable(settings) -> None:
    """Never write to the shared instance's default space (and send nothing)."""
    if settings.shared and not settings.space:
        raise ShopError(f"{settings.url} is the shared workshop instance and no space is set, so this would change "
                        "the baseline everyone shares. Set SHOP_SPACE to your GitHub handle in .env first.")


def cmd_preset(settings, name: str) -> None:
    require_writable(settings)
    request(settings, "POST", "/api/workshop/preset", {"preset": name})
    print(f"applied preset {name} in space {settings.space or 'default'}")


def cmd_reset(settings) -> None:
    require_writable(settings)
    result = request(settings, "POST", "/api/workshop/reset")
    print(f"reset space {result.get('space', settings.space or 'default')}: removed "
          f"{result.get('removed_flags', 0)} flag settings, {result.get('removed_cart_items', 0)} cart items "
          f"and {result.get('removed_orders', 0)} orders")


def cmd_wait(settings, timeout: float) -> None:
    deadline = time.monotonic() + timeout
    while True:
        try:
            health = request(settings, "GET", "/health")
            print(f"shop is up at {settings.url} (version {health.get('version', '?')})")
            return
        except ShopError:
            if time.monotonic() >= deadline:
                raise ShopError(f"no healthy shop at {settings.url} after {timeout:.0f} s") from None
            time.sleep(1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m shop", description="Status, presets and resets for the workshop shop.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="version, space and the presets that hold")
    sub.add_parser("presets", help="list the preset names")
    preset = sub.add_parser("preset", help="apply a preset in the current space")
    preset.add_argument("name")
    sub.add_parser("reset", help="reset the current space")
    wait = sub.add_parser("wait", help="wait until the shop answers /health")
    wait.add_argument("--timeout", type=float, default=60.0, help="seconds (default 60)")
    args = parser.parse_args(argv)

    settings = load()
    try:
        if settings.problem and settings.space:
            # An invalid space would be rejected by the shop anyway; say why first.
            raise ShopError(settings.problem)
        if args.command == "status":
            cmd_status(settings)
        elif args.command == "presets":
            cmd_presets(settings)
        elif args.command == "preset":
            cmd_preset(settings, args.name)
        elif args.command == "reset":
            cmd_reset(settings)
        elif args.command == "wait":
            cmd_wait(settings, args.timeout)
    except ShopError as error:
        print(f"shop: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
