import errno
import os
import stat
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import SimpleTestCase

from ddcz.tests.test_ui.cases import install_chromedriver


class TestInstallChromedriver(SimpleTestCase):
    def setUp(self):
        source_dir = tempfile.TemporaryDirectory()
        destination_dir = tempfile.TemporaryDirectory()
        self.addCleanup(source_dir.cleanup)
        self.addCleanup(destination_dir.cleanup)

        self.source = Path(source_dir.name) / "chromedriver"
        self.source.write_text("new driver")
        self.source.chmod(0o644)
        self.destination = Path(destination_dir.name) / "chromedriver"

    def test_installs_across_filesystems(self):
        with patch(
            "os.rename", side_effect=OSError(errno.EXDEV, "Invalid cross-device link")
        ):
            install_chromedriver(str(self.source), str(self.destination))

        self.assertEqual("new driver", self.destination.read_text())
        self.assertFalse(self.source.exists())

    def test_installed_driver_is_executable(self):
        install_chromedriver(str(self.source), str(self.destination))

        self.assertEqual(0o755, stat.S_IMODE(os.stat(self.destination).st_mode))

    def test_executable_mode_survives_cross_filesystem_copy(self):
        with patch(
            "os.rename", side_effect=OSError(errno.EXDEV, "Invalid cross-device link")
        ):
            install_chromedriver(str(self.source), str(self.destination))

        self.assertEqual(0o755, stat.S_IMODE(os.stat(self.destination).st_mode))

    def test_replaces_existing_driver(self):
        self.destination.write_text("old driver")

        install_chromedriver(str(self.source), str(self.destination))

        self.assertEqual("new driver", self.destination.read_text())

    def test_falls_back_to_sudo_without_permissions(self):
        with (
            patch("shutil.move", side_effect=PermissionError),
            patch("subprocess.run") as run,
        ):
            install_chromedriver(str(self.source), str(self.destination))

        run.assert_called_once_with(
            ["sudo", "mv", str(self.source), str(self.destination)], check=True
        )
