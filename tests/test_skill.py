"""Skill musí běžet bez instalace balíčku, jen z vlastní složky."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
SKILL = KOREN / "skills" / "pravnikovo-cztypo"
SPOUSTEC = SKILL / "scripts" / "cztypo_cli.py"


def spust(*args: str, vstup: str) -> subprocess.CompletedProcess[str]:
    # -I: izolovaný režim, nainstalovaný balíček ani cwd se nenačtou
    return subprocess.run([sys.executable, "-I", str(SPOUSTEC), *args],
                          input=vstup, capture_output=True, text=True,
                          encoding="utf-8", cwd=KOREN.parent, check=False)


def test_skill_ma_frontmatter() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\nname: pravnikovo-cztypo\n")
    assert "\ndescription:" in text.split("\n---\n", 1)[0]


def test_vlnky() -> None:
    r = spust("--vlnky", vstup="jel s kolegou, IČ 12345678")
    assert r.returncode == 0
    assert r.stdout.strip() == "jel s~kolegou, IČO 12345678"


def test_check_hlasi_nalez() -> None:
    r = spust("--check", vstup="110 00 Praha 1")
    assert r.returncode == 1
    assert "PSČ" in r.stdout


def test_vystup_je_idempotentni() -> None:
    vstup = "Podle § 234 odst. 4 písm. a) pod sp. zn. 12 Nt 345/2026 dne 1. 2. 2026."
    prvni = spust(vstup=vstup).stdout
    assert spust(vstup=prvni).stdout == prvni
    assert spust("--check", vstup=prvni).returncode == 0


def test_vlnky_nejdou_s_typst() -> None:
    assert spust("--vlnky", "--typst", vstup="x").returncode == 2
