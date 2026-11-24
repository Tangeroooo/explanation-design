import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("assembler", ROOT / "skills/explanation-design/scripts/assemble.py")
assembler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assembler)


class AssemblyTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads((ROOT / "skills/explanation-design/assets/document.json").read_text())
        self.scratch = tempfile.TemporaryDirectory()
        self.base = Path(self.scratch.name)

    def tearDown(self):
        self.scratch.cleanup()

    def invalid(self, mutate):
        doc = copy.deepcopy(self.doc)
        mutate(doc)
        with self.assertRaises(ValueError):
            assembler.validate(doc, self.base)

    def test_missing_evidence_is_rejected(self):
        self.invalid(lambda d: d["claims"][0].update(source_ids=[]))
        self.invalid(lambda d: d["claims"][0].update(source_ids=["missing"]))
        self.invalid(lambda d: d["sections"][0]["blocks"][0].update(claim_ids=["missing"]))

    def test_invalid_states_and_duplicate_ids_are_rejected(self):
        self.invalid(lambda d: d["claims"][0].update(kind="certain"))
        self.invalid(lambda d: d["sources"].append(copy.deepcopy(d["sources"][0])))

    def test_ragged_table_and_dangerous_url_are_rejected(self):
        self.invalid(lambda d: d["sections"][0]["blocks"].append({"type":"table", "headers":["a","b"], "rows":[["1"]]}))
        for url in ["javascript:alert(1)", "//host/path", "https://u:p@host/", "a\nb", "data:text/html,x"]:
            self.invalid(lambda d: d["sources"][0].update(href=url))

    def test_missing_assets_and_directory_escape_are_rejected(self):
        (self.base / "brief.md").write_text("brief")
        figure = {"type":"figure", "path":"missing.svg", "brief":"brief.md", "alt":"a", "caption":"c"}
        self.invalid(lambda d: d["sections"][0]["blocks"].append(figure))
        with tempfile.TemporaryDirectory() as other:
            external = Path(other) / "secret.svg"
            external.write_text("<svg/>")
            (self.base / "link.svg").symlink_to(external)
            figure["path"] = "link.svg"
            self.invalid(lambda d: d["sections"][0]["blocks"].append(figure))

    def test_html_is_escaped_and_code_fences_preserve_content(self):
        block = self.doc["sections"][0]["blocks"][0]
        block["text"] = "<script>alert('x')</script> | [link](javascript:x)"
        self.doc["sections"][0]["blocks"].append({"type":"code", "language":"text", "text":"```\n</code><script>x</script>"})
        assembler.assemble(self.doc, self.base, self.base / "out")
        html = (self.base / "out/index.html").read_text()
        markdown = (self.base / "out/explanation.md").read_text()
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("````text\n```", markdown)

    def test_assets_are_packaged_without_basename_collision(self):
        for folder, payload in [("a", "<svg>one</svg>"), ("b", "<svg>two</svg>")]:
            (self.base / folder).mkdir()
            (self.base / folder / "same.svg").write_text(payload)
            (self.base / folder / "brief.md").write_text("brief " + folder)
            self.doc["sections"][0]["blocks"].append({"type":"figure", "path":folder+"/same.svg", "brief":folder+"/brief.md", "alt":"content", "caption":"caption"})
        self.doc["sections"][0]["blocks"][-1]["display_width"] = 960
        out = self.base / "out"
        assembler.assemble(self.doc, self.base, out)
        first = (out / "index.html").read_bytes()
        assembler.assemble(self.doc, self.base, out)
        self.assertEqual(first, (out / "index.html").read_bytes())
        self.assertEqual(len(list((out / "assets").glob("*.svg"))), 2)
        self.assertEqual(len(list((out / "briefs").glob("*.md"))), 2)
        self.assertIn("width='960'", first.decode())

    def test_source_links_are_rebased_for_any_output_location(self):
        (self.base / "evidence.txt").write_text("evidence")
        self.doc["sources"][0]["href"] = "evidence.txt#section"
        out = self.base / "deep" / "output"
        assembler.assemble(self.doc, self.base, out)
        self.assertIn("../../evidence.txt#section", (out / "index.html").read_text())
        self.assertIn("../../evidence.txt#section", (out / "explanation.md").read_text())
        self.doc["sources"][0]["href"] = "missing.txt"
        with self.assertRaises(ValueError):
            assembler.validate(self.doc, self.base)

    def test_document_labels_follow_language_without_translating_content(self):
        (self.base / "figure.svg").write_text("<svg/>")
        (self.base / "brief.md").write_text("Brief")
        self.doc["sections"][0]["blocks"].append({"type": "figure", "path": "figure.svg", "brief": "brief.md", "alt": "Authored label", "caption": "Authored caption"})
        self.doc["claims"].append({"id": "C2", "text": "Unverified claim", "kind": "unknown", "source_ids": [], "basis": "No implementation supplied"})
        original_text = self.doc["sections"][0]["blocks"][0]["text"]
        for language, expected in [("en", "en"), ("en-US", "en"), ("ko", "ko"), ("ko-KR", "ko"), ("fr", "en")]:
            with self.subTest(language=language):
                self.doc["language"] = language
                out = self.base / language
                assembler.assemble(self.doc, self.base, out)
                page = (out / "index.html").read_text()
                markdown = (out / "explanation.md").read_text()
                labels = assembler.LABELS[expected]
                self.assertIn(f"lang='{language}'", page)
                for key in ("claims_heading", "sources_heading", "figure_brief"):
                    self.assertIn(labels[key], page)
                    self.assertIn(labels[key], markdown)
                self.assertIn(labels["figure_region"], page)
                self.assertIn(labels["scroll_hint"], page)
                self.assertIn(labels["claim_refs"], markdown)
                self.assertIn(labels["kinds"]["fact"], page)
                self.assertIn(labels["none"], page)
                self.assertIn(original_text, page)
                if expected == "en":
                    self.assertNotRegex(page, r"[가-힣]")


if __name__ == "__main__":
    unittest.main()
