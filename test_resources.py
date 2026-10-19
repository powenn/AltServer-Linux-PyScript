import io
import json
import tarfile
import tempfile
import unittest
from contextlib import ExitStack, redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

import requests

import main


class ResourceTests(unittest.TestCase):
    def setUp(self):
        self.context = ExitStack()
        self.addCleanup(self.context.close)
        self.root = Path(self.context.enter_context(tempfile.TemporaryDirectory()))
        self.context.enter_context(redirect_stdout(io.StringIO()))
        for name, value in {
            "RESOURCE_DIRECTORY": str(self.root),
            "VERSION_JSON_PATH": str(self.root / "version.json"),
            "ALTSERVER_PATH": str(self.root / "AltServer"),
            "ANISETTE_SERVER_PATH": str(self.root / "anisette-server"),
            "NETMUXD_PATH": str(self.root / "netmuxd"),
            "ALTSTORE_PATH": str(self.root / "AltStore.ipa"),
            "NETMUXD_IS_AVAILABLE": True,
            "Netmuxd_is_on": True,
            "Version_Fetched": False,
        }.items():
            self.context.enter_context(patch.object(main, name, value))

    def fetch_version(self, arch, asset_name):
        assets = ([{"name": asset_name,
                    "browser_download_url": "https://example.invalid/" + asset_name}]
                  if asset_name else [])
        responses = [
            {"apps": [{"versions": [{"version": "2.3", "downloadURL": "ipa"}]}]},
            {"tag_name": "v0.0.5"},
            {"tag_name": "v0.4.3", "assets": assets},
            {"tag_name": "2.2.0"},
            {"tag_name": "1.0.2"},
        ]
        with patch.object(main, "ARCH", arch), patch.object(
            main.requests, "get", side_effect=[Mock(json=Mock(return_value=r)) for r in responses]
        ):
            return main.FetchVersion()

    @staticmethod
    def archive(*names):
        output = io.BytesIO()
        with tarfile.open(fileobj=output, mode="w:gz") as archive:
            for name in names:
                member = tarfile.TarInfo(name)
                content = b"\x7fELFtest"
                member.size = len(content)
                archive.addfile(member, io.BytesIO(content))
        return output.getvalue()

    def test_current_and_legacy_release_assets(self):
        for arch, name in [("x86_64", "netmuxd-x86_64-unknown-linux-gnu.tar.gz"),
                           ("aarch64", "aarch64-linux-netmuxd")]:
            with self.subTest(name=name):
                self.fetch_version(arch, name)
                self.assertEqual(main.Netmuxd_URL, "https://example.invalid/" + name)
                self.assertTrue(main.NETMUXD_IS_AVAILABLE)

    def test_missing_architecture_falls_back_to_usb(self):
        self.fetch_version("armv7", "netmuxd-x86_64-unknown-linux-gnu.tar.gz")
        self.assertFalse(main.NETMUXD_IS_AVAILABLE)
        self.assertFalse(main.Netmuxd_is_on)
        self.assertEqual(main.Netmuxd_URL, "")

    def test_archive_only_writes_the_selected_executable(self):
        response = Mock(content=self.archive("../unexpected", "nested/netmuxd"))
        with patch.object(main.requests, "get", return_value=response):
            main.DownloadResource("https://example.invalid/netmuxd.tar.gz", main.NETMUXD_PATH)
        self.assertEqual(Path(main.NETMUXD_PATH).read_bytes(), b"\x7fELFtest")
        self.assertEqual([p.name for p in self.root.iterdir()], ["netmuxd"])

    def test_legacy_raw_binary(self):
        with patch.object(main.requests, "get", return_value=Mock(content=b"\x7fELFtest")):
            main.DownloadResource("https://example.invalid/x86_64-linux-netmuxd", main.NETMUXD_PATH)
        self.assertTrue(main.IsValidResource(main.NETMUXD_PATH))

    def test_http_error_preserves_existing_file(self):
        path = Path(main.ALTSERVER_PATH)
        path.write_bytes(b"\x7fELFexisting")
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("404")
        with patch.object(main.requests, "get", return_value=response):
            with self.assertRaises(requests.HTTPError):
                main.DownloadResource("https://example.invalid/AltServer", str(path))
        self.assertEqual(path.read_bytes(), b"\x7fELFexisting")

    def test_invalid_payload_and_ambiguous_archive_are_not_saved(self):
        for data in [b"Not Found", self.archive("a/netmuxd", "b/netmuxd")]:
            with self.subTest(data_type="archive" if data.startswith(b"\x1f\x8b") else "text"):
                url = "https://example.invalid/netmuxd.tar.gz" if data.startswith(b"\x1f\x8b") else "raw"
                with patch.object(main.requests, "get", return_value=Mock(content=data)):
                    with self.assertRaises(ValueError):
                        main.DownloadResource(url, main.NETMUXD_PATH)
                self.assertFalse(Path(main.NETMUXD_PATH).exists())

    def test_cached_not_found_is_replaced_before_becoming_executable(self):
        versions = self.fetch_version("x86_64", "netmuxd-x86_64-unknown-linux-gnu.tar.gz")
        Path(main.VERSION_JSON_PATH).write_text(json.dumps(versions))
        for path in [main.ALTSERVER_PATH, main.ANISETTE_SERVER_PATH]:
            Path(path).write_bytes(b"\x7fELFexisting")
        Path(main.ALTSTORE_PATH).write_bytes(b"PKexisting")
        Path(main.NETMUXD_PATH).write_bytes(b"Not Found")
        response = Mock(content=self.archive("netmuxd"))
        with patch.object(main.requests, "get", return_value=response) as get:
            main.CheckResource()
        get.assert_called_once_with(main.Netmuxd_URL, timeout=120)
        self.assertEqual(Path(main.NETMUXD_PATH).read_bytes(), b"\x7fELFtest")
        self.assertEqual(Path(main.NETMUXD_PATH).stat().st_mode & 0o777, 0o755)


if __name__ == "__main__":
    unittest.main()
