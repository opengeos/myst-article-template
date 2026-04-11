#!/usr/bin/env python3
"""Build the MyST article as a PDF.

Runs ``myst build --pdf`` from the repo root and verifies the expected
output file exists. Requires the ``myst`` CLI (installed via npm) and
``typst`` (used by the ``lapreprint-typst`` export template) on PATH.

Usage:
    python build_pdf.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
EXPECTED_PDF = REPO_ROOT / "article.pdf"


def _require(binary: str) -> None:
    """Exit with a clear message if a required CLI is missing.

    Args:
        binary: Name of the executable to look up on PATH.
    """
    if shutil.which(binary) is None:
        sys.exit(
            f"error: `{binary}` is not on PATH. "
            f"Install it and retry (myst via `npm i -g mystmd`, "
            f"typst from https://typst.app)."
        )


def build_pdf() -> int:
    """Invoke ``myst build --pdf`` in the repo root.

    Returns:
        The subprocess exit code from the myst CLI.
    """
    print("[build_pdf] running `myst build --pdf`...")
    result = subprocess.run(
        ["myst", "build", "--pdf"],
        cwd=REPO_ROOT,
        check=False,
    )
    return result.returncode


def main() -> int:
    """Build the article PDF and confirm the output file exists.

    Returns:
        Process exit code: 0 on success, non-zero on failure.
    """
    _require("myst")
    _require("typst")

    rc = build_pdf()
    if rc != 0:
        print(f"[build_pdf] myst build failed with exit code {rc}", file=sys.stderr)
        return rc

    if not EXPECTED_PDF.exists():
        print(
            f"[build_pdf] error: expected PDF not found at {EXPECTED_PDF}",
            file=sys.stderr,
        )
        return 1

    print(f"[build_pdf] PDF built: {EXPECTED_PDF.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
