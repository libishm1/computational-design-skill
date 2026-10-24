import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_skills as v  # noqa: E402

GOOD_DESC = "Use this skill to test the validator on a well formed fixture with a long enough description."


def make_skill(root, name, body="# Body\n\n## Quick start\n\n1. step\n", desc=GOOD_DESC, extra=None):
    d = root / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {desc}\n---\n\n{body}", encoding="utf-8")
    for rel, content in (extra or {}).items():
        f = d / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")
    return d


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_well_formed_skill_passes(self):
        make_skill(self.root, "good-skill", body="## Quick start\n\n1. step\n\nSee `references/a.md`.\n",
                   extra={"references/a.md": "ok\n"})
        problems, count = v.run(self.root)
        self.assertEqual(problems, [])
        self.assertEqual(count, 1)

    def test_name_mismatch_fails(self):
        d = make_skill(self.root, "alpha")
        (d / "SKILL.md").write_text(f"---\nname: beta\ndescription: {GOOD_DESC}\n---\n", encoding="utf-8")
        problems, _ = v.run(self.root)
        self.assertTrue(any("expected folder name" in p for p in problems))

    def test_short_description_fails(self):
        make_skill(self.root, "short", desc="too short")
        problems, _ = v.run(self.root)
        self.assertTrue(any("description shorter" in p for p in problems))

    def test_missing_reference_fails(self):
        make_skill(self.root, "dangling", body="See `references/missing.md`.\n")
        problems, _ = v.run(self.root)
        self.assertTrue(any("referenced file missing" in p for p in problems))

    def test_missing_frontmatter_fails(self):
        d = self.root / "skills" / "nofm"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text("# no frontmatter\n", encoding="utf-8")
        problems, _ = v.run(self.root)
        self.assertTrue(any("no frontmatter" in p for p in problems))

    def test_local_path_is_flagged(self):
        make_skill(self.root, "leaky", body="Run from D:\\Projects\\private\\x\n")
        problems, _ = v.run(self.root)
        self.assertTrue(any("local drive path" in p for p in problems))

    def test_personal_name_is_flagged(self):
        make_skill(self.root, "named", body="Written for Libish.\n")
        problems, _ = v.run(self.root)
        self.assertTrue(any("personal name" in p for p in problems))

    def test_email_and_token_are_flagged(self):
        make_skill(self.root, "secretive", body="mail a.b@example.org key ghp_" + "a" * 24 + "\n")
        problems, _ = v.run(self.root)
        labels = " ".join(problems)
        self.assertIn("email address", labels)
        self.assertIn("token-like string", labels)

    def test_main_exit_codes(self):
        make_skill(self.root, "fine")
        self.assertEqual(v.main(["--root", str(self.root)]), 0)
        make_skill(self.root, "bad", body="D:\\x\n")
        self.assertEqual(v.main(["--root", str(self.root)]), 1)


class LocalModelLimitTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_missing_quick_start_fails(self):
        make_skill(self.root, "noquick", body="# Body\n\nNo quick start here.\n")
        problems, _ = v.run(self.root)
        self.assertTrue(any("Quick start" in p for p in problems))

    def test_long_skill_fails(self):
        body = "## Quick start\n\n" + "line\n" * (v.MAX_SKILL_LINES + 10)
        make_skill(self.root, "toolong", body=body)
        problems, _ = v.run(self.root)
        self.assertTrue(any("limit is" in p for p in problems))

    def test_long_reference_needs_contents(self):
        body = "## Quick start\n\nok\n"
        big = "# Ref\n\n" + "text\n" * (v.LONG_REFERENCE + 5)
        make_skill(self.root, "bigref", body=body, extra={"references/big.md": big})
        problems, _ = v.run(self.root)
        self.assertTrue(any("Contents" in p for p in problems))

    def test_long_reference_with_contents_passes(self):
        body = "## Quick start\n\nok\n"
        big = "# Ref\n\n## Contents\n\n- one\n\n" + "text\n" * (v.LONG_REFERENCE + 5)
        make_skill(self.root, "okref", body=body, extra={"references/big.md": big})
        problems, _ = v.run(self.root)
        self.assertEqual([p for p in problems if "okref" in p], [])


class ColonRuleTests(unittest.TestCase):
    def test_colon_space_in_description_fails(self):
        import tempfile as tf
        with tf.TemporaryDirectory() as d:
            root = Path(d)
            make_skill(root, "colony", desc="Use this: skill to test the colon rule with a long enough text here.")
            problems, _ = v.run(root)
            self.assertTrue(any("colon and space" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
