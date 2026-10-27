#!/usr/bin/env python3
"""Vyrobí typst/priklad/telo.typ z telo.md přes cztypo (ukázka spolupráce).

    python3 tools/priklad.py && typst compile typst/priklad/podani.typ
"""
from __future__ import annotations

import sys
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOREN / "src"))

from cztypo import do_typstu, uprav  # noqa: E402

PRIKLAD = KOREN / "typst" / "priklad"


def main() -> int:
    odstavce = (PRIKLAD / "telo.md").read_text(encoding="utf-8").split("\n\n")
    telo = "\n\n".join(do_typstu(uprav(o.strip())) for o in odstavce if o.strip())
    (PRIKLAD / "telo.typ").write_text(
        "// Vygenerováno z telo.md nástrojem tools/priklad.py, ručně neupravovat.\n"
        + telo + "\n", encoding="utf-8")
    print(f"zapsáno {PRIKLAD / 'telo.typ'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
