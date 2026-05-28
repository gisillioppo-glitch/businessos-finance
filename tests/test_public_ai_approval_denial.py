import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.security import surface_audit


class PublicAIApprovalDenialTests(unittest.TestCase):
    def write_public_file(self, root, relative_path, content):
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_denial_check(self, root, public_dir):
        with patch.object(surface_audit, "ROOT_DIR", root), patch.object(
            surface_audit,
            "PUBLIC_DIR",
            public_dir,
        ):
            return surface_audit._check_public_ai_approval_denial()

    def test_public_ai_approval_denial_passes_for_safe_concept_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            public_dir = root / "public"
            self.write_public_file(
                public_dir,
                "index.html",
                "BusinessOS includes governance controls and approval gates.",
            )

            result = self.run_denial_check(root, public_dir)

            self.assertEqual(result["name"], "public_ai_approval_denial")
            self.assertEqual(result["status"], "passed")

    def test_public_ai_approval_denial_blocks_private_table_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            public_dir = root / "public"
            self.write_public_file(
                public_dir,
                "index.html",
                "Do not expose approval_requests to public AI.",
            )

            result = self.run_denial_check(root, public_dir)

            self.assertEqual(result["status"], "failed")
            self.assertIn("approval_requests", result["detail"])

    def test_public_ai_approval_denial_blocks_private_command_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            public_dir = root / "public"
            self.write_public_file(
                public_dir,
                "lead-intake.js",
                "approval-approve should never be callable here.",
            )

            result = self.run_denial_check(root, public_dir)

            self.assertEqual(result["status"], "failed")
            self.assertIn("approval-approve", result["detail"])


if __name__ == "__main__":
    unittest.main()
