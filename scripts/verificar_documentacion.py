"""Verify report-local Markdown links and the unmodified source PDF."""

import hashlib
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHA256 = "b81f72f9f9c03d0c70d0dcd8934043ee67e3286bf2df98885a912e1040bbdc58"


def main() -> None:
    checked = 0
    for document in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", ".venv"} for part in document.relative_to(ROOT).parts):
            continue
        for label, target in re.findall(r"!?\[([^\]]+)\]\(([^\s)]+)\)", document.read_text(encoding="utf-8-sig")):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (document.parent / unquote(parsed.path)).resolve()
            assert destination.is_relative_to(ROOT), (document, label, target)
            assert destination.exists(), (document, label, target)
            checked += 1
    pdf = ROOT / "fuentes/TF_1ASI0657_202610_NRC_7.pdf"
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == EXPECTED_SHA256
    print(f"Report: {checked} internal links OK; original PDF checksum OK.")


if __name__ == "__main__":
    main()
