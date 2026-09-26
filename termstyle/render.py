"""Render banners, rules, boxes, status lines, meters and prompts."""

import unicodedata

from .themes import BOX_STYLES, DEFAULT_THEME, get_theme


def display_width(text):
    """Terminal column width: wide/fullwidth = 2, combining marks = 0.

    East Asian "ambiguous" characters (many geometric shapes) count as 1,
    which matches most Western terminal fonts.
    """
    total = 0
    for ch in text:
        if unicodedata.combining(ch) or unicodedata.category(ch) == "Cf":
            continue
        total += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return total


def pad(text, width):
    return text + " " * max(0, width - display_width(text))


def banner(title, theme=DEFAULT_THEME, subtitle=None):
    """⟦ ◎ TRON ◎ ⟧ with an optional indented subtitle line."""
    t = get_theme(theme)
    line = f"{t.title_open}{title.upper()}{t.title_close}"
    if subtitle:
        line += "\n" + " " * display_width(t.title_open) + subtitle.upper()
    return line


def rule(title="", theme=DEFAULT_THEME, width=40):
    """───┤ SIGNAL ONLINE ├──────────  (plain rule when title is empty)."""
    t = get_theme(theme)
    if not title:
        return t.rule_char * width
    head = t.rule_char * 3 + t.rule_open + title.upper() + t.rule_close
    return head + t.rule_char * max(0, width - display_width(head))


def box(lines, theme=DEFAULT_THEME, title=None, width=None):
    """Frame lines in the theme's box style; borders always align."""
    t = get_theme(theme)
    tl, tr, bl, br, h, v = BOX_STYLES[t.box]
    if isinstance(lines, str):
        lines = lines.splitlines()
    label = f"{h} {title.upper()} " if title else ""
    inner = max([display_width(s) + 2 for s in lines] + [display_width(label) + 1])
    if width:
        inner = max(inner, width - 2)
    top = tl + label + h * (inner - display_width(label)) + tr
    body = [f"{v} {pad(s, inner - 2)} {v}" for s in lines]
    bottom = bl + h * inner + br
    return "\n".join([top, *body, bottom])


def status(label, kind="ok", theme=DEFAULT_THEME):
    """◉ UPLINK ESTABLISHED — kind is ok, warn, err or info."""
    t = get_theme(theme)
    if kind not in t.marks:
        raise ValueError(f"unknown status kind {kind!r}; choose from {', '.join(t.marks)}")
    return f"{t.marks[kind]} {label.upper()}"


def meter(fraction, label="", theme=DEFAULT_THEME, cells=6):
    """▰▰▰▰▱▱ UPLINK — fraction is clamped to 0..1."""
    t = get_theme(theme)
    filled = round(max(0.0, min(1.0, fraction)) * cells)
    bar = t.bar_full * filled + t.bar_empty * (cells - filled)
    return f"{bar} {label.upper()}".rstrip()


def prompt(user, host, path="~", theme=DEFAULT_THEME):
    """Two-line prompt: ┌─[ user@host ]─[ path ] / └──╼ $"""
    t = get_theme(theme)
    tl, _, bl, _, h, _ = BOX_STYLES[t.box]
    char = t.prompt_char
    # Themes whose prompt already draws its own corner keep it as is.
    second = char if char[0] in "└╚┗" else f"{bl}{h}{h} {char}"
    return f"{tl}{h}[ {user}@{host} ]{h}[ {path} ]\n{second} "


def ps1(theme=DEFAULT_THEME, color=True):
    """Bash PS1 string for prompt(); colour codes wrapped in \\[ \\]."""
    text = prompt(r"\u", r"\h", r"\w", theme)
    if color:
        code = get_theme(theme).color
        text = "\n".join(
            rf"\[\e[{code}m\]{line}\[\e[0m\]" for line in text.split("\n")
        )
    return text.replace("\n", r"\n")


def signoff(theme=DEFAULT_THEME):
    return get_theme(theme).signoff


def colorize(text, theme=DEFAULT_THEME):
    code = get_theme(theme).color
    return "\n".join(f"\033[{code}m{line}\033[0m" for line in text.split("\n"))
