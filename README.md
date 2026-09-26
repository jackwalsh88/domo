# termstyle

Cyberpunk banners, status lines, meters, boxes and shell prompts for the terminal.
Pure Python standard library, no dependencies.

```text
⟦ ◎ THE GRID ◎ ⟧

═══╡ SIGNAL ONLINE ╞════════════════════
◎ UPLINK ESTABLISHED
⬡ SYNC PENDING
▰▰▰▰▱▱ UPLINK
╔═ ESPER ═════════════╗
║ ENHANCE ▸ SECTOR 04 ║
╚═════════════════════╝
╔═[ root@neotron ]═[ ~/ ]
╚══ ≫
≫ END OF LINE_
```

## Themes

`hacker` (default), `cyberpunk`, `headroom`, `tron`, `bladerunner`, `snowcrash`, `neuromancer`.

## CLI

```sh
pip install .                      # or: python -m termstyle ...
termstyle themes
termstyle -t tron demo
termstyle -t bladerunner banner "tyrell corporation" -s "more human than human"
termstyle -t cyberpunk rule "encrypted channel" -w 50
termstyle -t neuromancer status err "black ice // contact"
termstyle -t snowcrash meter 0.4 "signal"
echo "ENHANCE ▸ SECTOR 04" | termstyle box --title esper
termstyle --color always -t tron signoff
```

Colour is `auto` by default: on for a TTY, off when piped or when `NO_COLOR` is set.

### Shell prompt

```sh
# ~/.bashrc
PS1="$(termstyle -t tron ps1)"
```

## Library

```python
import termstyle as ts

print(ts.banner("the grid", "tron"))
print(ts.status("uplink established", "ok", "tron"))   # kinds: ok, warn, err, info
print(ts.meter(0.66, "uplink", "tron"))
print(ts.box(["ENHANCE ▸ SECTOR 04"], "tron", title="esper"))
print(ts.prompt("root", "neotron", "~/", "tron"))
```

Custom themes: construct `ts.Theme(...)` and pass it wherever a theme name is accepted.

## Width handling

Box borders are measured in terminal columns, not characters, so fullwidth
glyphs such as `【 】` still line up. Many geometric symbols (`◎ ▲ ▰`) are East
Asian "ambiguous" width and are counted as one column; terminals set to render
ambiguous characters as wide will misalign them.

## Tests

```sh
python -m unittest discover -s tests
```
