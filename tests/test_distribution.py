"""Packaging and fixture checks; these do not grade a teaching agent."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def load_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


manage = load_file("baby_manage", ROOT / "scripts" / "manage.py")
fixture = ROOT / "tests" / "projects" / "03-reading-debug" / "fixture"
server_module = load_file("baby_fixture", fixture / "server.py")


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="baby-tutor-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)

    def test_install_complete_and_repeatable(self):
        destination = manage.install(str(self.root))
        self.assertEqual(manage.files_under(destination), manage.files_under(manage.SKILL))
        self.assertEqual(manage.install(str(self.root)), destination)

    def test_install_preserves_different_existing_skill(self):
        destination = self.root / ".agents" / "skills" / manage.NAME
        destination.mkdir(parents=True)
        saved = destination / "SKILL.md"
        saved.write_text("my custom skill", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "nothing overwritten"):
            manage.install(str(self.root))
        self.assertEqual(saved.read_text(), "my custom skill")

    def test_install_requires_existing_project(self):
        missing = self.root / "not-created"
        with self.assertRaisesRegex(ValueError, "already exist"):
            manage.install(str(missing))
        self.assertFalse(missing.exists())

    def test_prepare_blank_projects_with_task_and_skill(self):
        for number in ("1", "2"):
            destination = manage.prepare(number, self.root / f"项目 {number}")
            self.assertEqual({p.name for p in destination.iterdir()}, {".agents", "TASK.md"})
            self.assertIn("$baby-coding-tutor", (destination / "TASK.md").read_text())
            self.assertEqual(manage.files_under(destination / ".agents" / "skills" / manage.NAME),
                             manage.files_under(manage.SKILL))

    def test_prepare_debug_fixture_and_refuse_overwrite(self):
        destination = manage.prepare("3", self.root / "debug")
        for relative, content in manage.files_under(fixture).items():
            self.assertEqual((destination / relative).read_bytes(), content)
        (destination / "app.js").write_text("student work", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "nothing overwritten"):
            manage.prepare("3", destination)
        self.assertEqual((destination / "app.js").read_text(), "student work")

    def test_archive_single_root_and_exact_skill_contents(self):
        destination = manage.package(self.root / "skill.zip")
        with ZipFile(destination) as archive:
            self.assertEqual({p.split("/")[0] for p in archive.namelist()}, {manage.NAME})
            actual = {p.removeprefix(manage.NAME + "/"): archive.read(p) for p in archive.namelist()}
        self.assertEqual(actual, manage.files_under(manage.SKILL))
        self.assertEqual(manage.package(destination), destination)

    def test_archive_does_not_replace_other_zip(self):
        destination = self.root / "custom.zip"
        with ZipFile(destination, "w") as archive:
            archive.writestr("keep.txt", "other work")
        original = destination.read_bytes()
        with self.assertRaisesRegex(ValueError, "differs"):
            manage.package(destination)
        self.assertEqual(destination.read_bytes(), original)

    def test_invalid_archive_is_preserved_with_clear_error(self):
        destination = self.root / "invalid.zip"
        destination.write_bytes(b"not a zip")
        with self.assertRaisesRegex(ValueError, "Cannot compare"):
            manage.package(destination)
        self.assertEqual(destination.read_bytes(), b"not a zip")


class FixtureHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class QuietHandler(server_module.Handler):
            def log_message(self, *_):
                pass
        cls.server = server_module.ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_page_and_script_are_really_served(self):
        with urlopen(self.base, timeout=2) as response:
            self.assertEqual(response.status, 200)
            self.assertIn("加载笔记", response.read().decode())
        with urlopen(self.base + "/app.js", timeout=2) as response:
            self.assertIn("await response.json()", response.read().decode())

    def test_original_frontend_request_receives_non_json_404(self):
        source = (fixture / "app.js").read_text()
        endpoint = re.search(r'const endpoint = "([^"]+)";', source).group(1)
        with self.assertRaises(HTTPError) as raised:
            urlopen(self.base + endpoint, timeout=2)
        error = raised.exception
        try:
            self.assertEqual(error.code, 404)
            self.assertIn("text/html", error.headers["Content-Type"])
            body = error.read().decode()
        finally:
            error.close()
        with self.assertRaises(json.JSONDecodeError):
            json.loads(body)

    def test_available_api_returns_real_notes(self):
        with urlopen(self.base + "/api/notes", timeout=2) as response:
            self.assertEqual(response.status, 200)
            self.assertIn("application/json", response.headers["Content-Type"])
            notes = json.load(response)
        self.assertEqual([n["title"] for n in notes], ["算法导论", "网页开发笔记"])


if __name__ == "__main__":
    unittest.main()
