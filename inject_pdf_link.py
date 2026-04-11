#!/usr/bin/env python3
"""Inject a "Download PDF" link into the built HTML site.

Runs after ``myst build --html`` as a deploy-time post-process. This keeps
the link out of the MyST source (and therefore out of the Typst/PDF export)
while still surfacing it on the published HTML site.

The link is inserted right before the first ``<header`` tag found in
each HTML file under ``_build/html/``. That puts it above the article
header (title, authors, abstract) and crucially *outside* the theme's
``<section id="frontmatter">`` block, which otherwise hides unexpected
children via CSS. The target PDF path is ``article.pdf``, which the
deploy workflow copies to the HTML site root.

Usage:
    python inject_pdf_link.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
HTML_DIR = REPO_ROOT / "_build" / "html"

LINK_HTML = (
    '<div class="pdf-download-link" '
    'style="margin:1rem 0;padding:0.5rem 0;font-size:1.05em;">'
    '<a href="article.pdf" '
    'style="display:inline-block;padding:0.4em 0.9em;'
    "border:1px solid currentColor;border-radius:0.4em;"
    'text-decoration:none;"><strong>&#128196; Download PDF</strong></a>'
    "</div>"
)

HEADER_PATTERN = re.compile(r"<header\b", flags=re.IGNORECASE)


def inject_link(html: str) -> tuple[str, bool]:
    """Insert the download link immediately before the first ``<header>``.

    Args:
        html: Raw HTML contents of a built page.

    Returns:
        A tuple of ``(new_html, changed)`` where ``changed`` is True iff
        a ``<header>`` was found and the link was injected.
    """
    new_html, n = HEADER_PATTERN.subn(LINK_HTML + r"<header", html, count=1)
    return new_html, n > 0


def main() -> int:
    """Walk the built HTML tree and inject the link into every page.

    Returns:
        Process exit code: 0 on success, 1 if the HTML directory is missing.
    """
    if not HTML_DIR.is_dir():
        print(
            f"[inject-pdf-link] error: {HTML_DIR} does not exist; "
            "run `myst build --html` first.",
            file=sys.stderr,
        )
        return 1

    touched = 0
    for html_file in HTML_DIR.rglob("*.html"):
        original = html_file.read_text(encoding="utf-8")
        updated, changed = inject_link(original)
        if changed:
            html_file.write_text(updated, encoding="utf-8")
            touched += 1
            print(f"[inject-pdf-link] {html_file.relative_to(REPO_ROOT)}")

    print(f"[inject-pdf-link] injected link into {touched} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
