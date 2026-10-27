"""Mezery a interpunkce: opravy a kontroly (příklady „správně / špatně“).

Pravidla podle IJP ÚJČ; seznam doplněn podle přehledu nejčastějších chyb
v odborných textech (srov. naformatuj.cz, Základní typografická pravidla).
"""

from __future__ import annotations

import pytest

from cztypo import KANCELAR, NBSP, UJC, cisty, uprav, zkontroluj


def u(text: str, profil=UJC) -> str:
    return cisty(uprav(text, profil)).replace(NBSP, " ")


@pytest.mark.parametrize(("vstup", "ocekavano"), [
    # uvozovky jako dvě čárky
    (",,Uvozovky dole“ se nepíší", "„Uvozovky dole“ se nepíší"),
    (',,text" a dál', "„text“ a dál"),
    # mezery uvnitř závorek
    ("Českou republikou ( ČR) a ( ČSSR )", "Českou republikou (ČR) a (ČSSR)"),
    ("a ( 2 ) a ( x)", "a (2) a (x)"),
    # mezera před interpunkcí za slovem
    ("možností : nikdy , výjimečně ; občas !", "možností: nikdy, výjimečně; občas!"),
    # zdvojená tečka za zkratkou na konci věty
    ("razítka apod..", "razítka apod."),
    # cca bez tečky
    ("trvat cca. 3 týdny", "trvat cca 3 týdny"),
    # poměr a dělení: dvojtečka s mezerami, které se nelámou
    ("v poměru 2:3 nebo 2 : 3", "v poměru 2:3 nebo 2 : 3"),
])
def test_opravy(vstup, ocekavano):
    assert u(vstup) == ocekavano


def test_dvojtecka_pomeru_se_nelame():
    assert f"2{NBSP}:{NBSP}3" in cisty(uprav("v poměru 2 : 3"))


@pytest.mark.parametrize("beze_zmeny", [
    "verze 1.2.3 a čas 6:24,19",          # číslo verze, čas
    "skóre 6:2 a 15 : 5 = 3",             # výsledek, dělení
    "Ph.D., atd., a. s.",                 # zkratky s tečkami
    "tři tečky… a výpustka …",            # výpustka
    "„citace ( doslovně ) apod..“",       # doslovná citace se nemění
    "seznam: a), b) a c)",
    r"\[ PODÁNO DATOVOU SCHRÁNKOU \] a #let x = { 1 }",  # syntaxe typst
    "- [ ] úkol a [#del(old) ] v typst",                   # markdown, typst
    "soubor `HL 7.10.2026 v0.04.pdf` a dne 7.10.2026",     # datum jen hlásí
])
def test_bez_zmeny(beze_zmeny):
    assert u(beze_zmeny) == beze_zmeny


@pytest.mark.parametrize(("text", "nalez"), [
    ("možnosti nikdy,výjimečně,občas", "chybí mezera za čárkou"),
    ("okolností– tedy nezazní", "pomlčka bez mezery"),
    ("v rozmezí 15 – 20 °C", "rozsah čísel s mezerami"),
    ("nezazní -li poplach", "spojovník u -li s mezerou"),
    ("Ostrava - Dubina, vědecko - výzkumný", "spojovník s mezerami"),
    ("viz. předchozí kapitola", "„viz“ bez tečky"),
    ("tzv. „překlenovací úvěr“", "po „tzv.“ se uvozovky nepíší"),
    ("Ing. Jan Novák Ph.D. uvedl", "titul za jménem se odděluje čárkou"),
    ("Je to pravda?. Ano!.", "kumulace interpunkce"),
    ("naměřili -18 °C", "znak minus"),
    ("dne 25.7.2020 podal", "datum bez mezer"),
    ("rychlost 50 km / h", "lomítko s mezerami"),
])
def test_kontroly(text, nalez):
    assert any(n.startswith(nalez) for n in zkontroluj(text)), zkontroluj(text)


def test_kancelar_pouziva_spojovnik_misto_pomlcky():
    # profil kanceláře píše spojovník s mezerami místo pomlčky: nehlásit
    nalezy = zkontroluj("rozhodl - a to správně - soud", KANCELAR)
    assert not any(n.startswith("spojovník s mezerami") for n in nalezy)


def test_vypnuti():
    p = UJC.s(interpunkce=False)
    assert u("( ČR )", p) == "( ČR )"
    assert not any(n.startswith("chybí mezera") for n in zkontroluj("a,b", p))


@pytest.mark.parametrize("bez_nalezu", [
    "Dne 25. 7. 2020 – tedy včas – podal (viz příloha) odvolání.",
    "Ing. Jan Novák, Ph.D., uvedl, že 15–20 % je 1. července – 31. srpna.",
    "Je-li to tak, platí § 2 odst. 1 písm. a), b).",
    "e-mail info@example.cz, www.example.cz/a,b",
    "č. j. KRPA-…-000072 a KRPA-12345-6/ČJ-2026, usnesení -102 a -366",
])
def test_bez_falesnych_nalezu(bez_nalezu):
    nove = ("chybí mezera", "pomlčka bez", "rozsah čísel", "spojovník",
            "„viz“", "po „tzv.“", "titul za", "kumulace", "znak minus", "lomítko")
    assert not [n for n in zkontroluj(bez_nalezu) if n.startswith(nove)]
