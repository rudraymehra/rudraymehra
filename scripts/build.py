"""Build entry point: portrait + GitHub stats -> generated/*.svg.

Usage:
    python scripts/build.py [--config config.json] [--offline]
                            [--theme dark|light|both] [--out-dir generated]

Exit codes: 0 on success (including degraded/offline stat fetches);
nonzero only for broken config or a missing portrait, so CI surfaces
real bugs but never fails because of network weather.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import load_config
from generate_ascii import generate_ascii
from generate_svg import render_svg
from github_stats import collect_stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the profile terminal SVGs")
    parser.add_argument("--config", default="config.json", help="path to config.json")
    parser.add_argument(
        "--offline", action="store_true", help="skip the network, reuse cached stats"
    )
    parser.add_argument("--theme", choices=["dark", "light", "both"], default="both")
    parser.add_argument("--out-dir", default="generated")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    base_dir = Path(args.config).resolve().parent
    out_dir = base_dir / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    stats = collect_stats(config, token, out_dir, offline=args.offline)
    if stats.partial:
        print("note: stats are partial (cache/offline fallback)", file=sys.stderr)

    themes = ["dark", "light"] if args.theme == "both" else [args.theme]
    for theme in themes:
        ascii_rows = generate_ascii(config.ascii, theme, base_dir)
        svg = render_svg(ascii_rows, stats, config, theme)
        target = out_dir / f"{theme}_mode.svg"
        target.write_text(svg, encoding="utf-8")
        print(f"wrote {target.relative_to(base_dir)} ({len(svg):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
