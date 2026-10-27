"""Pravidla převzatá z jiných projektů (MIT, viz NOTICE.md).

- yetty/cstypo (Juda Kaleta, 2012): uvozovky, trojtečka, znak krát,
  krátké poslední slovo odstavce.
- wilx/cstypo (Václav Haisman, 2016): volba, zda vázat spojky „a“ a „i“.
"""

from __future__ import annotations

import pytest

from cztypo import NBSP, UJC, cisty, uprav


def u(text: str, profil=UJC) -> str:
    return cisty(uprav(text, profil))


@pytest.mark.parametrize(("vstup", "ocekavano"), [
    ('řekl "pojď už" a odešel', "řekl „pojď už“ a"),
    ('"Ano," odpověděl.', "„Ano,“ odpověděl."),
    # jednoduché uvozovky i apostrof
    ("slovo 'jinak' znamená", "slovo ‚jinak‘ znamená"),
    ("Pad' a chcíp'.", "Pad' a"),
    # anglické uvozovky uvnitř slova nebo bez páru zůstávají
    ('palec 5" je', 'palec 5" je'),
])
def test_uvozovky(vstup, ocekavano):
    assert ocekavano in u(vstup)


def test_uvozovky_lze_vypnout():
    assert '"pojď"' in u('řekl "pojď"', UJC.s(uvozovky=False))


@pytest.mark.parametrize(("vstup", "ocekavano"), [
    ("a tak dále...", "dále…"),
    ("Tedy... ne", "Tedy… ne"),
])
def test_trojtecka(vstup, ocekavano):
    assert ocekavano in u(vstup)


def test_dlouha_rada_tecek_neni_trojtecka():
    # řada teček je místo pro doplnění, ne výpustka
    assert "…" not in u("podpis ..........")


@pytest.mark.parametrize(("vstup", "ocekavano"), [
    ("místnost 10x20 m", f"10{NBSP}×{NBSP}20"),
    ("formát 21 x 29,7 cm", f"21{NBSP}×{NBSP}29,7"),
    ("zvětšení 3x zvýšilo", "3× zvýšilo"),
])
def test_znak_krat(vstup, ocekavano):
    assert ocekavano in u(vstup)


def test_krat_nechyta_hexadecimalni_cislo():
    assert "0x1F" in u("adresa 0x1F v paměti")


def test_kratke_posledni_slovo_odstavce():
    vstup = ("Soud rozhodl o žalobě a náklady řízení přiznal žalobci v plné "
             "výši do tří dnů.")
    assert "dnů." in u(vstup)
    assert f"tří{NBSP}dnů." in u(vstup)


def test_posledni_slovo_kratkeho_textu_se_nevaze():
    # krátký text (nadpis, buňka tabulky) nemá vdovy, nic se neváže
    assert u("Výrok I.") == "Výrok I."


def test_posledni_slovo_po_odstavcich():
    vstup = ("První odstavec je dost dlouhý na to, aby se zalomil, a končí "
             "tady.\n\nDruhý odstavec je také dost dlouhý, aby se zalomil, "
             "a končí zde.")
    vystup = u(vstup)
    assert f"končí{NBSP}tady." in vystup
    assert f"končí{NBSP}zde." in vystup


def test_spojky_a_i_lze_nevazat():
    profil = UJC.s(vazat_a_i=False)
    vystup = u("pes a kočka i myš s kocourem", profil)
    assert "a kočka" in vystup
    assert "i myš" in vystup
    assert f"s{NBSP}kocourem" in vystup


@pytest.mark.parametrize(("vstup", "ocekavano"), [
    ("sídlo Dlouhá 12, Praha 1, kde", f"Praha{NBSP}1,"),
    ("soud pro Prahu 4 rozhodl", f"Prahu{NBSP}4 rozhodl"),
    ("ulice Dlouhá 12, kde", f"Dlouhá{NBSP}12,"),
])
def test_nazev_a_cislo(vstup, ocekavano):
    assert ocekavano in u(vstup)


def test_radova_cislovka_za_nazvem_se_nevaze():
    # „Dne 5. března“ je datum, ne název s číslem
    assert f"Dne{NBSP}5." not in u("Dne 5. března 2026 soud")


def test_kontrola_respektuje_nevazane_spojky():
    from cztypo import zkontroluj
    profil = UJC.s(vazat_a_i=False)
    text = cisty(uprav("pes a kočka šla k domu a pak dál", profil))
    assert zkontroluj(text, profil) == []


def test_krat_nemeni_citaci():
    # doslovná citace (protokol, rozsudek) se nemění ani typograficky
    assert "„asi 2x pohnul“" in u("svědkyně uvedla „asi 2x pohnul“ a dál")
    assert f"10{NBSP}×{NBSP}20" in u("místnost 10x20 m, „cituji 3x“")


def test_trojtecka_nemeni_citaci():
    assert "„řekl jsem... nevím“" in u("uvedl „řekl jsem... nevím“ a odešel")
