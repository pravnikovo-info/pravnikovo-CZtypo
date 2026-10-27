#!/usr/bin/env python3
"""Zkopíruje balíček src/cstypo do skillu, aby skill běžel bez instalace.

    python3 tools/sync_skill.py          # zkopíruje
    python3 tools/sync_skill.py --check  # jen ověří shodu (CI), exit 1 při rozdílu
"""
from __future__ import annotations

import filecmp
import shutil
import sys
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
ZDROJ = KOREN / "src" / "cstypo"
CIL = KOREN / "skills" / "cstypo" / "scripts" / "cstypo"


def soubory(d: Path) -> list[str]:
    return sorted(p.name for p in d.glob("*.py"))


def shoda() -> bool:
    if not CIL.is_dir() or soubory(ZDROJ) != soubory(CIL):
        return False
    return all(filecmp.cmp(ZDROJ / f, CIL / f, shallow=False)
               for f in soubory(ZDROJ))


def main() -> int:
    if "--check" in sys.argv:
        if shoda():
            print("skill: kopie balíčku je aktuální")
            return 0
        print("skill: kopie balíčku se liší, spusťte tools/sync_skill.py")
        return 1
    if CIL.exists():
        shutil.rmtree(CIL)
    CIL.mkdir(parents=True)
    for f in soubory(ZDROJ):
        shutil.copy2(ZDROJ / f, CIL / f)
    print(f"skill: zkopírováno {len(soubory(ZDROJ))} souborů do {CIL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
