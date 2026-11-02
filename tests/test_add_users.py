"""Tests de comportement : getent et useradd sont simulés, aucun compte réel créé."""
import os
import errno
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "addUsers.sh"


class AddUsersTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.log = self.root / "calls"
        self.state = self.root / "users"
        self.state.write_text("alice2\n", encoding="utf-8")
        self.env = dict(os.environ, PATH=f"{self.root}:/usr/bin:/bin",
                        TEST_CALLS=str(self.log), TEST_USERS=str(self.state))
        self.command("getent", '''#!/bin/sh
test "$1" = passwd || exit 1
test "$2" = lookup_failure && exit 3
grep -Fqx -- "$2" "$TEST_USERS" && exit 0
exit 2
''')
        self.command("useradd", '''#!/bin/sh
printf '%s\\n' "$*" >> "$TEST_CALLS"
test "$1" = --create-home || exit 90
test "$2" = --shell || exit 90
test "$3" = /bin/bash || exit 90
test "$4" = -- || exit 90
test "$5" = failuser && exit 1
printf '%s\\n' "$5" >> "$TEST_USERS"
''')

    def tearDown(self):
        self.tmp.cleanup()

    def command(self, name, text):
        p = self.root / name
        p.write_text(text, encoding="utf-8")
        p.chmod(0o755)

    def invoke(self, *args, **kwargs):
        return subprocess.run(["/bin/bash", str(SCRIPT), *args],
                              env=self.env, capture_output=True, text=True, **kwargs)

    def calls(self):
        return self.log.read_text().splitlines() if self.log.exists() else []

    def test_no_arguments(self):
        self.assertEqual(self.invoke().returncode, 2)
        self.assertEqual(self.calls(), [])

    def test_help(self):
        self.assertEqual(self.invoke("--help").returncode, 0)

    def test_dry_run_is_read_only(self):
        p = self.invoke("--dry-run", "alice")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Simulation", p.stdout)
        self.assertEqual(self.calls(), [])

    def test_exact_lookup(self):
        p = self.invoke("--dry-run", "alice", "alice2")
        self.assertIn("Simulation : création de alice ", p.stdout)
        self.assertIn("Déjà présent : alice2", p.stdout)

    def test_invalid_names_reject_entire_batch(self):
        for name in ("-r", "bad name", "Alice", "a/b", "a;id", "a" * 33, ""):
            with self.subTest(name=name):
                self.assertEqual(self.invoke("--dry-run", "valid", name).returncode, 2)
                self.assertEqual(self.calls(), [])

    def test_lookup_error_is_reported(self):
        p = self.invoke("--dry-run", "lookup_failure")
        self.assertEqual(p.returncode, 1)
        self.assertIn("consultation", p.stderr)
        self.assertEqual(self.calls(), [])

    @unittest.skipUnless(os.geteuid() == 0, "Le chemin création requiert root ; commandes simulées.")
    def test_create_and_repeated_run(self):
        p = self.invoke("alice", "bob", "alice")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(len(self.calls()), 2)
        self.assertIn("--create-home --shell /bin/bash -- alice", self.calls())
        self.assertEqual(self.invoke("alice", "bob").returncode, 0)
        self.assertEqual(len(self.calls()), 2)

    @unittest.skipUnless(os.geteuid() == 0, "Le chemin création requiert root ; commandes simulées.")
    def test_creation_failure_returns_error(self):
        p = self.invoke("failuser", "bob")
        self.assertEqual(p.returncode, 1)
        self.assertIn("Échec de création", p.stderr)
        self.assertIn("Compte créé : bob", p.stdout)

    @unittest.skipUnless(os.geteuid() == 0, "Vérification du refus sans privilèges.")
    def test_non_root_cannot_create(self):
        # Le script est lisible par nobody ; le refus intervient avant les mocks.
        self.root.chmod(0o755)
        copied = self.root / "addUsers.sh"
        copied.write_text(SCRIPT.read_text(), encoding="utf-8")
        copied.chmod(0o644)
        try:
            p = subprocess.run(["/bin/bash", str(copied), "alice"], user=65534,
                               capture_output=True, text=True, env=self.env)
        except OSError as exc:
            if exc.errno in (errno.EINVAL, errno.EPERM):
                self.skipTest("Changement d'UID indisponible dans cet environnement.")
            raise
        self.assertEqual(p.returncode, 1)
        self.assertIn("droits root", p.stderr)
        self.assertEqual(self.calls(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
