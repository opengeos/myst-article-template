#!/usr/bin/env python3
"""Inject a "Download PDF" link into the built HTML site.

Runs after ``myst build --html`` as a deploy-time post-process. This keeps
the link out of the MyST source (and therefore out of the Typst/PDF export)
while still surfacing it on the published HTML site.

The article-theme is a React SPA: even if we insert a static element into
the server-rendered HTML, React's hydration pass wipes it out. To survive
re-renders, we instead inject a ``<script>`` tag at the end of ``<body>``
that adds the link client-side and uses a ``MutationObserver`` to
re-insert it every time React removes it.

Usage:
    python inject_pdf_link.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
HTML_DIR = REPO_ROOT / "_build" / "html"

# Client-side injection script. Re-inserts the download link whenever
# React (or any other code) strips it from the DOM. The script is
# idempotent: if the link is already present, `inject()` is a no-op.
INJECTION_SCRIPT = """
<script>
(function () {
  var LINK_HTML =
    '<div class="pdf-download-link" ' +
    'style="margin:1rem 0;font-size:1.05em;">' +
    '<a href="article.pdf" ' +
    'style="display:inline-block;padding:0.4em 0.9em;' +
    'border:1px solid currentColor;border-radius:0.4em;' +
    'text-decoration:none;color:inherit;">' +
    '<strong>\\u{1F4C4} Download PDF</strong></a></div>';

  function inject() {
    if (document.querySelector('.pdf-download-link')) return;
    var target = document.querySelector(
      '.myst-fm-block.myst-article-header-fm'
    );
    if (!target || !target.parentNode) return;
    var wrapper = document.createElement('div');
    wrapper.innerHTML = LINK_HTML;
    var node = wrapper.firstChild;
    target.parentNode.insertBefore(node, target);
  }

  function start() {
    inject();
    var observer = new MutationObserver(function () {
      if (!document.querySelector('.pdf-download-link')) inject();
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
</script>
""".strip()

BODY_END_PATTERN = re.compile(r"</body>", flags=re.IGNORECASE)


def inject_link(html: str) -> tuple[str, bool]:
    """Insert the injection script right before ``</body>``.

    Args:
        html: Raw HTML contents of a built page.

    Returns:
        A tuple of ``(new_html, changed)`` where ``changed`` is True iff
        a ``</body>`` tag was found and the script was injected.
    """
    if "pdf-download-link" in html:
        return html, False
    # Replacement is passed as a lambda so Python's regex engine does not
    # try to interpret backslash escapes (e.g. `\u{1F4C4}`) inside the
    # injected JavaScript as regex references.
    new_html, n = BODY_END_PATTERN.subn(
        lambda _match: INJECTION_SCRIPT + "</body>", html, count=1
    )
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
