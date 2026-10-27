"""Výchozí profil UJC: pravidla Internetové jazykové příručky ÚJČ AV ČR."""

import dataclasses

import pytest

from cztypo import KANCELAR, NBSP, UJC, Profil, cisty, do_typstu, uprav, zkontroluj
from cztypo.znacky import BOX0, BOX1, IT0


@pytest.mark.parametrize(("vstup", "ocekavano"), [
    # tisíce: vázaná mezera, ne tečka
    ("celková škoda 1 234 567 Kč", f"1{NBSP}234{NBSP}567{NBSP}Kč"),
    ("od 10 EUR do 2 000 EUR", f"2{NBSP}000{NBSP}EUR"),
    # telefon zůstává s mezerami, ale nedělí se
    ("telefon 777 000 000", f"{BOX0}777{NBSP}000{NBSP}000{BOX1}"),
    ("z čísla +420 777 000 001", f"{BOX0}+420{NBSP}777{NBSP}000{NBSP}001{BOX1}"),
    # pomlčka zůstává; s mezerami drží u předchozího slova
    ("P05 – Doklad o výši", f"P05{NBSP}– Doklad"),
    # rozsah se nedělí
    ("v letech 1948–1989", f"{BOX0}1948–1989{BOX1}"),
    # č. j. na začátku věty se nemění
    ("Č. j. uvedené výše", "Č."),
    # PSČ a rodné číslo
    ("bytem Dlouhá 1, 110 00 Praha 1", f"11000 Praha{NBSP}1"),
    ("rodné číslo 010231/0010", "0102310010"),
    ("IČ: 12345678", "IČO: 12345678"),
    ("IČ DPH SK2020123456", "IČ DPH SK2020123456"),
    # obecná pravidla jsou stejná jako v profilu kanceláře
    ("jel s poškozenou do banky", f"jel s{NBSP}poškozenou"),
    ("Pavel Černý, Ph.D., a další", f"Černý,{NBSP}Ph.D., a"),
    ("podle § 234 odst. 4", f"§{NBSP}234{NBSP}odst.{NBSP}4"),
])
def test_ujc(vstup, ocekavano):
    assert ocekavano in uprav(vstup, UJC)


def test_vychozi_profil_je_ujc():
    assert uprav("škoda 1 234 Kč") == uprav("škoda 1 234 Kč", UJC)


def test_citace_v_ujc_neni_kurzivou():
    assert IT0 not in uprav("uvedl „to není pravda“")
    assert IT0 in uprav("uvedl „to není pravda“", KANCELAR)


def test_latina_kurzivou_v_obou_profilech():
    for p in (UJC, KANCELAR):
        assert f"{IT0}de facto" in uprav("jde de facto o dar", p)


def test_psc_s_mezerou_lze_zapnout():
    p = UJC.s(psc_bez_mezery=False)
    assert f"110{NBSP}00 Praha" in uprav("Dlouhá 1, 110 00 Praha 1", p)


def test_rodne_cislo_s_lomitkem_lze_zapnout():
    p = UJC.s(rc_bez_lomitka=False)
    assert "010231/0010" in uprav("RČ 010231/0010", p)
    assert zkontroluj("RČ 010231/0010", p) == []


def test_ico_lze_vypnout():
    assert "IČ 12345678" in uprav("IČ 12345678", UJC.s(ico=False))


def test_kontrola_hlasi_ic():
    assert any(n.startswith("zkratka „IČ“") for n in zkontroluj("IČ 12345678"))


def test_profil_je_nemenny():
    with pytest.raises(dataclasses.FrozenInstanceError):
        UJC.tisice = "tecka"  # type: ignore[misc]


def test_neplatny_oddelovac_tisicu():
    with pytest.raises(ValueError):
        Profil(tisice="carka")


def test_kontrola_ujc_hlasi_tisice_s_obycejnou_mezerou():
    assert any(n.startswith("tisíce oddělené obyčejnou mezerou")
               for n in zkontroluj("škoda 1 234 567 Kč"))


def test_kontrola_ujc_nehlasi_zvyklosti_kancelare():
    text = "Podle zákona (dále jen „ZOK“) – viz tel. 777 000 000"
    assert zkontroluj(text) == []


def test_kancelar_tyto_zvyklosti_hlasi():
    text = "Podle zákona (dále jen „ZOK“) – viz tel. 777 000 000"
    popisy = [n.split(":")[0] for n in zkontroluj(text, KANCELAR)]
    assert any("dále jen" in p for p in popisy)
    assert any("dash" in p for p in popisy)
    assert any("telefon" in p for p in popisy)


def test_upraveny_text_projde_kontrolou():
    vzorek = ("Obviněný a jeho syn jel s poškozenou dne 28. 7. 2026 do banky "
              "v Písku, kde vybral 1 234 567 Kč podle § 234 odst. 4.")
    assert zkontroluj(cisty(uprav(vzorek))) == []


@pytest.mark.parametrize(("vstup", "ocekavano"), [
    ("pod sp. zn. 28 C 140/2026 dne", f"28{NBSP}C{NBSP}140/2026 dne"),
    ("nález I. ÚS 1234/25 a", f"I.{NBSP}ÚS{NBSP}1234/25 a"),
])
def test_prosty_text_drzi_spisovou_znacku(vstup, ocekavano):
    # prostý text (DOCX, web) nezná #box, mezery uvnitř bloku jsou vlnky
    assert ocekavano in cisty(uprav(vstup))


def test_tecka_za_vetou_neni_v_bloku():
    vystup = do_typstu(uprav("srov. č. j. ABCD-12345-67/TČ-2026-000089. Dále"))
    assert "#box[ABCD-12345-67/TČ-2026-000089]" in vystup
