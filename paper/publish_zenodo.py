"""Publish a new version of the paper to Zenodo with the PDF as its primary file.

Zenodo's GitHub integration archives a release as a zip of the repository and nothing else, so a
record made that way has no PDF for a reader to open or for Google Scholar to index. This script
uses Zenodo's deposit API instead: it opens a new version of the existing record, removes the files
the new version inherited, uploads the PDF first and a source zip second, applies `.zenodo.json`,
and publishes. The concept DOI (all versions) stays the same.

Turn the repository's switch OFF on Zenodo's GitHub page before using this, or every GitHub
release will also mint a zip-only version.

The token comes from the ZENODO_TOKEN environment variable and is never printed. It needs the
`deposit:write` and `deposit:actions` scopes.

    python paper/publish_zenodo.py --version paper-v0.4 --dry-run
    python paper/publish_zenodo.py --version paper-v0.4
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
API = "https://zenodo.org/api"
ANY_VERSION = 23610077  # first version; Zenodo resolves its version list from any member
PDF = HERE / "paper.pdf"


def call(method: str, url: str, token: str | None = None, body: bytes | None = None,
         content_type: str = "application/json") -> dict:
    req = urllib.request.Request(url, data=body, method=method)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    if body is not None:
        req.add_header("Content-Type", content_type)
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read()
    return json.loads(raw) if raw else {}


def latest_record_id() -> int:
    versions = call("GET", f"{API}/records/{ANY_VERSION}/versions?sort=version&size=25")
    hits = versions["hits"]["hits"]
    return max(hits, key=lambda h: h["created"])["id"]


def legacy_metadata(version: str) -> dict:
    z = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    meta = {k: z[k] for k in ("title", "upload_type", "publication_type", "description",
                              "creators", "access_right", "keywords", "related_identifiers",
                              "notes", "language") if k in z}
    meta["license"] = z.get("license", "cc-by-4.0")
    meta["version"] = version
    meta["publication_date"] = dt.date.today().isoformat()
    return meta


def source_zip(version: str) -> Path:
    out = HERE / f"research-{version}-source.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "-o", str(out), "HEAD"],
                   check=True)
    return out


def pdf_name(meta: dict, version: str) -> str:
    words = re.findall(r"[a-z0-9]+", meta["title"].lower())[:8]
    return "-".join(["de-silva-2026", *words, version]) + ".pdf"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True, help="e.g. paper-v0.4")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not PDF.exists():
        sys.exit("paper/paper.pdf is missing; run python paper/build.py first")
    meta = legacy_metadata(args.version)
    latest = latest_record_id()
    name = pdf_name(meta, args.version)
    print(f"latest record: {latest}")
    print(f"new version:   {args.version}  title: {meta['title']}")
    print(f"files:         1. {name}  ({PDF.stat().st_size:,} bytes)  2. source zip")
    if args.dry_run:
        print("dry run: nothing sent")
        return

    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        sys.exit("ZENODO_TOKEN is not set")

    draft = call("POST", f"{API}/deposit/depositions/{latest}/actions/newversion", token)
    draft = call("GET", draft["links"]["latest_draft"], token)
    dep_id, bucket = draft["id"], draft["links"]["bucket"]
    print(f"draft:         {dep_id}")

    for f in draft.get("files", []):  # inherited from the previous version
        call("DELETE", f"{API}/deposit/depositions/{dep_id}/files/{f['id']}", token)

    zip_path = source_zip(args.version)
    try:
        for path, key in ((PDF, name), (zip_path, zip_path.name)):  # PDF first: the primary file
            call("PUT", f"{bucket}/{key}", token, path.read_bytes(), "application/octet-stream")
            print(f"uploaded:      {key}")
    finally:
        zip_path.unlink(missing_ok=True)

    call("PUT", f"{API}/deposit/depositions/{dep_id}", token,
         json.dumps({"metadata": meta}).encode())
    done = call("POST", f"{API}/deposit/depositions/{dep_id}/actions/publish", token)
    print(f"published:     {done.get('doi')}  {done['links'].get('html')}")


if __name__ == "__main__":
    main()
