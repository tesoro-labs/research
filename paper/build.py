"""Render draft.md to paper.html and paper.pdf.

`draft.md` stays the source of truth; the HTML and PDF are outputs for readers who will not open a
Markdown file, and for the Zenodo release that mints the DOI. Pandoc converts the Markdown and
headless Edge prints it, the same renderer `report/build.py` uses, for the same reason: weasyprint
is installed here but raises on its GTK dependency, so if Edge or pandoc is missing this script
says so rather than leaving a stale PDF in place.

    python paper/build.py            # HTML + PDF
    python paper/build.py --html     # HTML only
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

SOURCE = HERE / "draft.md"
CSS = HERE / "paper.css"
HTML = HERE / "paper.html"
PDF = HERE / "paper.pdf"

TITLE = "Which control decided? Required attribution in pre-execution payment governance"

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def tool(name: str, candidates: list[str] | None = None) -> str:
    for path in candidates or []:
        if Path(path).exists():
            return path
    found = shutil.which(name)
    if found:
        return found
    raise SystemExit(f"{name} not found; it is required to build the paper. Nothing was written.")


def to_html() -> None:
    # The CSS is embedded rather than linked so the HTML renders identically wherever it is
    # opened, and so the PDF does not depend on a file:// path that exists only on this machine.
    subprocess.run(
        # Math extensions off: the prose quotes dollar amounts, and "$24.24 million ... $0.32"
        # otherwise renders as one italic TeX formula.
        [tool("pandoc"), str(SOURCE), "--from", "gfm-tex_math_dollars-tex_math_gfm",
         "--to", "html5", "--standalone",
         "--metadata", f"title={TITLE}", "--metadata", "pagetitle=" + TITLE,
         "--css", str(CSS), "--embed-resources", "--output", str(HTML)],
        check=True, capture_output=True,
    )


def to_pdf() -> None:
    subprocess.run(
        [tool("msedge", EDGE_CANDIDATES), "--headless", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={PDF}", HTML.resolve().as_uri()],
        check=True, capture_output=True,
    )


def main() -> None:
    to_html()
    print(f"wrote {HTML.relative_to(ROOT)}  {HTML.stat().st_size:,} bytes")
    if "--html" in sys.argv:
        return
    to_pdf()
    print(f"wrote {PDF.relative_to(ROOT)}  {PDF.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
