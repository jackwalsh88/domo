import contextlib
import io
import unittest

import termstyle as ts
from termstyle.__main__ import main


class DisplayWidthTest(unittest.TestCase):
    def test_ascii(self):
        self.assertEqual(ts.display_width("NEXUS-6"), 7)

    def test_fullwidth_brackets_count_double(self):
        self.assertEqual(ts.display_width("【 】"), 5)

    def test_combining_marks_are_zero_width(self):
        self.assertEqual(ts.display_width("é"), 1)


class RenderTest(unittest.TestCase):
    def test_every_theme_renders_every_element(self):
        for name in ts.THEMES:
            with self.subTest(theme=name):
                self.assertIn("GRID", ts.banner("grid", name))
                self.assertEqual(ts.display_width(ts.rule("x", name, 30)), 30)
                for kind in ("ok", "warn", "err", "info"):
                    self.assertTrue(ts.status("x", kind, name).endswith(" X"))
                self.assertTrue(ts.prompt("u", "h", "~", name).endswith(" "))
                self.assertTrue(ts.signoff(name))

    def test_box_borders_align_with_wide_characters(self):
        # The style guide's ESPER box was off by one; wide glyphs make it worse.
        for name in ts.THEMES:
            with self.subTest(theme=name):
                out = ts.box(["【 NEXUS-6 】", "short"], name, title="esper")
                widths = {ts.display_width(line) for line in out.splitlines()}
                self.assertEqual(len(widths), 1, out)

    def test_box_respects_minimum_width(self):
        out = ts.box(["a"], "tron", width=20)
        self.assertEqual(ts.display_width(out.splitlines()[0]), 20)

    def test_meter_clamps(self):
        self.assertEqual(ts.meter(2, "", "tron", cells=4), "▰▰▰▰")
        self.assertEqual(ts.meter(-1, "", "tron", cells=4), "▱▱▱▱")
        self.assertEqual(ts.meter(0.5, "uplink", "tron", cells=4), "▰▰▱▱ UPLINK")

    def test_ps1_escapes_color_and_newline(self):
        out = ts.ps1("tron")
        self.assertNotIn("\n", out)
        self.assertIn(r"\[\e[36m\]", out)
        self.assertIn(r"\u@\h", out)

    def test_unknown_names_raise(self):
        with self.assertRaises(ValueError):
            ts.banner("x", "matrix")
        with self.assertRaises(ValueError):
            ts.status("x", "fatal", "tron")


class CliTest(unittest.TestCase):
    def run_cli(self, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(main(list(argv)), 0)
        return buf.getvalue()

    def test_banner(self):
        self.assertEqual(self.run_cli("-t", "tron", "banner", "the grid"), "⟦ ◎ THE GRID ◎ ⟧\n")

    def test_color_always(self):
        self.assertIn("\033[36m", self.run_cli("-t", "tron", "--color", "always", "signoff"))

    def test_demo_all_themes(self):
        for name in ts.THEMES:
            self.assertIn(ts.signoff(name), self.run_cli("-t", name, "demo"))


if __name__ == "__main__":
    unittest.main()
