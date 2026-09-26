"""Command-line interface: python -m termstyle <command> ..."""

import argparse
import os
import sys

from . import render
from .themes import DEFAULT_THEME, THEMES


def use_color(mode):
    if mode == "always":
        return True
    if mode == "never" or os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


def demo(theme):
    return "\n".join([
        render.banner(theme, theme),
        "",
        render.rule("signal online", theme),
        render.status("uplink established", "ok", theme),
        render.status("sync pending", "warn", theme),
        render.status("signal breach", "err", theme),
        render.status("memory fragment", "info", theme),
        render.meter(0.66, "uplink", theme),
        render.box(["ENHANCE ▸ SECTOR 04"], theme, title="esper"),
        render.prompt("root", "neotron", "~/", theme),
        render.signoff(theme),
    ])


def build_parser():
    p = argparse.ArgumentParser(prog="termstyle", description=__doc__)
    p.add_argument("-t", "--theme", default=DEFAULT_THEME, choices=THEMES)
    p.add_argument("--color", default="auto", choices=["auto", "always", "never"])
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("themes", help="list theme names")
    sub.add_parser("demo", help="show every element for the theme")

    b = sub.add_parser("banner", help="title banner")
    b.add_argument("text")
    b.add_argument("-s", "--subtitle")

    r = sub.add_parser("rule", help="horizontal rule with optional title")
    r.add_argument("text", nargs="?", default="")
    r.add_argument("-w", "--width", type=int, default=40)

    x = sub.add_parser("box", help="frame text (reads stdin when no text given)")
    x.add_argument("text", nargs="*")
    x.add_argument("--title")
    x.add_argument("-w", "--width", type=int)

    s = sub.add_parser("status", help="status line")
    s.add_argument("kind", choices=["ok", "warn", "err", "info"])
    s.add_argument("text")

    m = sub.add_parser("meter", help="segmented progress bar")
    m.add_argument("fraction", type=float)
    m.add_argument("text", nargs="?", default="")
    m.add_argument("-c", "--cells", type=int, default=6)

    sub.add_parser("ps1", help="print a bash PS1 string")
    sub.add_parser("signoff", help="theme sign-off line")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    t = args.theme
    color = use_color(args.color)

    if args.command == "themes":
        print("\n".join(THEMES))
        return 0
    if args.command == "ps1":
        print(render.ps1(t, color=args.color != "never"))
        return 0
    if args.command == "demo":
        out = demo(t)
    elif args.command == "banner":
        out = render.banner(args.text, t, args.subtitle)
    elif args.command == "rule":
        out = render.rule(args.text, t, args.width)
    elif args.command == "box":
        lines = [" ".join(args.text)] if args.text else sys.stdin.read().splitlines()
        out = render.box(lines, t, args.title, args.width)
    elif args.command == "status":
        out = render.status(args.text, args.kind, t)
    elif args.command == "meter":
        out = render.meter(args.fraction, args.text, t, args.cells)
    else:
        out = render.signoff(t)

    print(render.colorize(out, t) if color else out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
