"""Assemble where-we-stand.html from its three parts, then render PDF and PNG.

Three parts, kept separate so each is editable on its own: `report.css` is the print stylesheet,
`body.html` is the prose, and `../where-we-stand.svg` is the diagram. The diagram is inlined rather
than linked because a PDF renderer given `file://` references produces a document that is only
correct on this machine, and because the published SVG and the figure in the report must be the
same bytes or they will drift.

Rendering uses headless Edge. `weasyprint` is installed here but raises on its GTK dependency, so
it is not a fallback; if Edge is missing this script says so rather than emitting a stale PDF.

    python report/build.py            # HTML + PDF + PNG
    python report/build.py --html     # HTML only
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

CSS = HERE / "report.css"
BODY = HERE / "body.html"
SVG = ROOT / "where-we-stand.svg"
HTML = HERE / "where-we-stand.html"
PDF = HERE / "where-we-stand.pdf"
PNG = ROOT / "where-we-stand.png"

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def assemble() -> str:
    body = BODY.read_text(encoding="utf-8")
    if "__SVG__" not in body:
        raise SystemExit("body.html has no __SVG__ placeholder; nothing would carry the figure")

    svg = SVG.read_text(encoding="utf-8")
    # The standalone file declares its own XML prolog and background rect; inlined in a flow
    # document neither is wanted, but the rect is load-bearing for the PNG, so only the prolog goes.
    svg = svg.replace('<?xml version="1.0" encoding="UTF-8"?>\n', "")

    return (
        '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">\n'
        "<title>Where tesoro stands</title>\n"
        "<style>\n" + CSS.read_text(encoding="utf-8") + "</style>\n"
        "</head>\n<body>\n" + body.replace("__SVG__", svg.strip()) + "\n</body></html>\n"
    )


def edge() -> str:
    for path in EDGE_CANDIDATES:
        if Path(path).exists():
            return path
    found = shutil.which("msedge")
    if found:
        return found
    raise SystemExit(
        "Microsoft Edge not found. The PDF is rendered headless by Edge; weasyprint is installed "
        "but raises on its missing GTK libraries, so there is no fallback. HTML was still written."
    )


def render(html_path: Path) -> None:
    exe = edge()
    url = html_path.resolve().as_uri()

    subprocess.run(
        [exe, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={PDF}", url],
        check=True, capture_output=True,
    )
    # 2x for a retina-legible raster; the SVG viewBox is 1200x1000.
    subprocess.run(
        [exe, "--headless", "--disable-gpu", "--force-device-scale-factor=2",
         "--window-size=1200,1000", "--default-background-color=00000000",
         f"--screenshot={PNG}", SVG.resolve().as_uri()],
        check=True, capture_output=True,
    )


def main() -> None:
    HTML.write_text(assemble(), encoding="utf-8", newline="\n")
    print(f"wrote {HTML.relative_to(ROOT)}  {HTML.stat().st_size:,} bytes")

    if "--html" in sys.argv:
        return

    render(HTML)
    for out in (PDF, PNG):
        print(f"wrote {out.relative_to(ROOT)}  {out.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
