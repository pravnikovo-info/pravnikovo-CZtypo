"""Příkazová řádka: cztypo [--profil P] [--check | --typst [--ladit]] [soubor ...]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .kontrola import zkontroluj
from .pravidla import uprav
from .profil import PROFILY, Profil
from .typst import LADENI, cisty, do_typstu


def _cti(cesta: str) -> str:
    if cesta == "-":
        return sys.stdin.read()
    return Path(cesta).read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="cztypo",
        description="Česká typografie: nezlomitelné mezery a zápis údajů.")
    ap.add_argument("soubory", nargs="*", default=["-"],
                    help="vstupní soubory (výchozí stdin)")
    ap.add_argument("--profil", choices=sorted(PROFILY), default="ujc",
                    help="sada pravidel (výchozí ujc)")
    vystup = ap.add_mutually_exclusive_group()
    vystup.add_argument("--check", action="store_true",
                        help="jen nahlásit prohřešky, exit 1 při nálezu")
    vystup.add_argument("--typst", action="store_true",
                        help="výstup jako typst markup")
    ap.add_argument("--ladit", action="store_true",
                    help="s --typst: zvýraznit nezlomitelné mezery a bloky")
    ap.add_argument("--version", action="version", version=__version__)
    a = ap.parse_args(argv)
    if a.ladit and not a.typst:
        ap.error("--ladit má smysl jen s --typst")
    profil = PROFILY[a.profil]
    try:
        texty = [(c, _cti(c)) for c in a.soubory]
    except OSError as e:
        print(f"cztypo: {e}", file=sys.stderr)
        return 2
    if a.check:
        return _kontrola(texty, profil)
    for _, txt in texty:
        upraveny = uprav(txt, profil)
        if a.typst:
            sys.stdout.write((LADENI if a.ladit else "")
                             + do_typstu(upraveny))
        else:
            sys.stdout.write(cisty(upraveny))
    return 0


def _kontrola(texty: list[tuple[str, str]], profil: Profil) -> int:
    rc = 0
    for cesta, txt in texty:
        nalezy = zkontroluj(txt, profil)
        if nalezy:
            rc = 1
            print(f"{cesta}:")
            for n in nalezy:
                print("  " + n)
    if rc == 0:
        print("Typografie OK.")
    return rc
