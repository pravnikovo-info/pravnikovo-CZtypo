#!/usr/bin/env python3
"""Zkopíruje balíček src/cztypo a typst šablonu do skillu (běží bez instalace).

    python3 tools/sync_skill.py          # zkopíruje
    python3 tools/sync_skill.py --check  # jen ověří shodu (CI), exit 1 při rozdílu
"""
from __future__ import annotations

import filecmp
import shutil
import sys
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
ZDROJ = KOREN / "src" / "cztypo"
CIL = KOREN / "skills" / "pravnikovo-cztypo" / "scripts" / "cztypo"
TYPST_ZDROJ = KOREN / "typst"
TYPST_CIL = KOREN / "skills" / "pravnikovo-cztypo" / "assets" / "typst"


def soubory(d: Path) -> list[str]:
    return sorted(p.name for p in d.glob("*.py"))


def typst_soubory(d: Path) -> list[str]:
    return sorted(str(p.relative_to(d)) for p in d.rglob("*")
                  if p.is_file() and p.suffix in (".typ", ".md")
                  and "test" not in p.relative_to(d).parts)


def shoda() -> bool:
    if not CIL.is_dir() or soubory(ZDROJ) != soubory(CIL):
        return False
    if not TYPST_CIL.is_dir() or typst_soubory(TYPST_ZDROJ) != typst_soubory(TYPST_CIL):
        return False
    return (all(filecmp.cmp(ZDROJ / f, CIL / f, shallow=False)
                for f in soubory(ZDROJ))
            and all(filecmp.cmp(TYPST_ZDROJ / f, TYPST_CIL / f, shallow=False)
                    for f in typst_soubory(TYPST_ZDROJ)))


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
    if TYPST_CIL.exists():
        shutil.rmtree(TYPST_CIL)
    for f in typst_soubory(TYPST_ZDROJ):
        (TYPST_CIL / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TYPST_ZDROJ / f, TYPST_CIL / f)
    print(f"skill: zkopírováno {len(soubory(ZDROJ))} modulů a "
          f"{len(typst_soubory(TYPST_ZDROJ))} souborů šablony")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
