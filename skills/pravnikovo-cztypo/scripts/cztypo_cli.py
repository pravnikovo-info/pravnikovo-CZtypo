#!/usr/bin/env python3
"""Spouštěč cztypo pro skill: běží bez instalace (balíček je ve složce vedle).

    python3 cztypo_cli.py soubor.md                 # upravený text na stdout
    python3 cztypo_cli.py --check soubor.md         # nálezy, exit 1 při nálezu
    python3 cztypo_cli.py --typst soubor.md         # typst markup
    python3 cztypo_cli.py --vlnky soubor.md         # nezlomitelné mezery jako ~
    python3 cztypo_cli.py --profil kancelar ...     # jiný profil pravidel
    echo "jel s kolegou" | python3 cztypo_cli.py --vlnky

--vlnky je jen pro čtení člověkem nebo modelem: ukáže, kam pravidla vložila
nezlomitelnou mezeru (U+00A0), která je jinak neviditelná. Do souboru, který
se bude sázet, patří výstup bez --vlnky.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cztypo.cli import main as cztypo_main  # noqa: E402
from cztypo.znacky import NBSP  # noqa: E402


def main(argv: list[str]) -> int:
    if "--vlnky" not in argv:
        return cztypo_main(argv)
    argv = [a for a in argv if a != "--vlnky"]
    if "--check" in argv or "--typst" in argv:
        print("--vlnky nelze kombinovat s --check ani --typst", file=sys.stderr)
        return 2
    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cztypo_main(argv)
    sys.stdout.write(buf.getvalue().replace(NBSP, "~"))
    return rc


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
