"""Symbol themes drawn from the terminal style guide."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Theme:
    name: str
    title_open: str
    title_close: str
    rule_char: str
    rule_open: str
    rule_close: str
    box: str  # key into BOX_STYLES
    marks: dict = field(default_factory=dict)  # ok / warn / err / info
    bar_full: str = "▰"
    bar_empty: str = "▱"
    prompt_char: str = "$"
    signoff: str = ""
    color: str = "0"  # ANSI SGR parameter


# corners: top-left, top-right, bottom-left, bottom-right, horizontal, vertical
BOX_STYLES = {
    "light": "┌┐└┘─│",
    "double": "╔╗╚╝═║",
    "heavy": "┏┓┗┛━┃",
}

THEMES = {
    t.name: t
    for t in (
        Theme(
            name="hacker",
            title_open="██ ", title_close=" ██",
            rule_char="─", rule_open="┤ ", rule_close=" ├",
            box="light",
            marks={"ok": "[●]", "warn": "[!]", "err": "[×]", "info": ">_"},
            bar_full="█", bar_empty="░",
            prompt_char="└──╼ $",
            signoff="↳ /dev/null",
            color="32",
        ),
        Theme(
            name="cyberpunk",
            title_open="⟦ ⬡ ", title_close=" ⟧",
            rule_char="═", rule_open="╡ ", rule_close=" ╞",
            box="double",
            marks={"ok": "◈", "warn": "⧖", "err": "↯", "info": "⊹"},
            prompt_char="⌗ >",
            signoff="⌗ NETRUNNER // OFFLINE",
            color="35",
        ),
        Theme(
            name="headroom",
            title_open="◢████ ", title_close=" ████◣",
            rule_char="═", rule_open="╞══ ", rule_close=" ══╡",
            box="double",
            marks={"ok": "◢", "warn": "▰▱", "err": "▱▱", "info": "◣"},
            prompt_char="◢ >",
            signoff="◢ ZIK ZAK ◣",
            color="96",
        ),
        Theme(
            name="tron",
            title_open="⟦ ◎ ", title_close=" ◎ ⟧",
            rule_char="═", rule_open="╡ ", rule_close=" ╞",
            box="double",
            marks={"ok": "◎", "warn": "⬡", "err": "⊞", "info": "▸▸▸"},
            prompt_char="≫",
            signoff="≫ END OF LINE_",
            color="36",
        ),
        Theme(
            name="bladerunner",
            title_open="▲ ", title_close=" ▲",
            rule_char="─", rule_open="┤ ", rule_close=" ├",
            box="light",
            marks={"ok": "◉", "warn": "△", "err": "▪", "info": "⌖"},
            prompt_char="▸",
            signoff="╎ ┆ ⋮ TEARS IN RAIN ⋮ ┆ ╎",
            color="33",
        ),
        Theme(
            name="snowcrash",
            title_open="» ", title_close=" «",
            rule_char="━", rule_open=" ", rule_close=" ",
            box="heavy",
            marks={"ok": "⟦◉⟧", "warn": "∷", "err": "↯", "info": "⧉"},
            prompt_char="λ",
            signoff="» SIGNAL DECAY «",
            color="97",
        ),
        Theme(
            name="neuromancer",
            title_open="◇ ", title_close=" ◇",
            rule_char="═", rule_open="╬ ", rule_close=" ╬",
            box="double",
            marks={"ok": "◉", "warn": "⌁", "err": "⬢", "info": "▣"},
            prompt_char="↯",
            signoff="» DEAD CHANNEL «",
            color="34",
        ),
    )
}

DEFAULT_THEME = "hacker"


def get_theme(theme):
    """Accept a Theme or a theme name."""
    if isinstance(theme, Theme):
        return theme
    try:
        return THEMES[theme]
    except KeyError:
        raise ValueError(
            f"unknown theme {theme!r}; choose from {', '.join(THEMES)}"
        ) from None
