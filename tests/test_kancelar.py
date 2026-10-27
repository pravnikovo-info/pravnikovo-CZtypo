"""Pravidla v profilu KANCELAR (převzaté regresní testy původní verze).

Všechna jména, firmy, čísla a značky jsou smyšlené.
"""

import pytest

from cztypo import KANCELAR, NBSP, cisty, do_typstu, uprav, zkontroluj
from cztypo.znacky import BOX0, BOX1

TESTY = [
    # jednoznakové předložky a spojky
    ("jel s poškozenou do banky", f"jel s{NBSP}poškozenou"),
    ("obviněný a jeho syn", f"obviněný a{NBSP}jeho"),
    ("předal je v Praze", f"je v{NBSP}Praze"),
    ("odkaz k ustanovení", f"odkaz k{NBSP}ustanovení"),
    ("bez ohledu o tom", f"ohledu o{NBSP}tom"),
    ("A to i přes výzvu", f"i{NBSP}přes"),
    # zápis údajů
    ("bytem Dlouhá 1, 110 00 Praha 1", f"11000 Praha{NBSP}1"),
    ("celková škoda 1 234 567 Kč", "1.234.567"),
    # 31. února: tvarově platné rodné číslo, které nemůže patřit nikomu
    ("rodné číslo 010231/0010", "0102310010"),
    # číslo znaleckého posudku stejného tvaru není rodné číslo
    ("znalecký posudek č. 032300/2026", "032300/2026"),
    # telefony
    ("telefonní číslo 777 000 000", "+420777000000"),
    ("z čísla +420 777 000 001", "+420777000001"),
    # zkratky a čísla
    ("Č. j. ABCD-1/TČ-2026-1", f"č.{NBSP}j."),
    # celá citace paragrafu drží pohromadě, i mezi číslem a slovem „odst.“
    ("podle § 234 odst. 4", f"§{NBSP}234{NBSP}odst.{NBSP}4"),
    ("podle § 234 odst. 1, odst. 4 písm. a)",
     f"§{NBSP}234{NBSP}odst.{NBSP}1, odst.{NBSP}4{NBSP}písm.{NBSP}a)"),
    ("Je-li to možné", f"{BOX0}Je-li{BOX1} to možné"),
    ("t. č. ve Vazební věznici", f"t.{NBSP}č.{NBSP}ve Vazební věznici"),
    ("rodinný dům č. p. 4137", f"rodinný dům č.{NBSP}p.{NBSP}4137"),
    ("na parcele st. 6479", f"na parcele st.{NBSP}6479"),
    ("že „k těmto záznamům", f"že „k{NBSP}těmto záznamům"),
    ("dne 28. 7. 2026", f"28.{NBSP}7.{NBSP}2026"),
    ("V Praze dne 14. září 2026", f"14.{NBSP}září"),
    # jednotky
    ("vylákal 700 000 000 Kč", "700.000.000"),
    ("od 10 EUR do 2 000 EUR", f"2.000{NBSP}EUR"),
    ("podíl 100 % základního kapitálu", f"100{NBSP}%"),
    ("najel 6 000 km", f"6.000{NBSP}km"),
    # právní formy, tituly, iniciály
    ("Banky Příkladné, a. s.", f"Příkladné,{NBSP}a.{NBSP}s."),
    # obchodní firma beze změny zápisu, jen forma drží u názvu
    ("VZOREK s.r.o.", f"VZOREK{NBSP}s.r.o."),
    ("PŘÍKLAD s.r.o., IČO 12345678", f"PŘÍKLAD{NBSP}s.r.o., IČO"),
    ("společnost UKÁZKA a.s. jako", f"UKÁZKA{NBSP}a.s. jako"),
    ("AB-SERVIS PLUS s.r.o.", "AB-SERVIS" + BOX1 + f" PLUS{NBSP}s.r.o."),
    ("Mgr. Jan Dvořák", f"Mgr.{NBSP}Jan"),
    ("nprap. Jan Novák", f"nprap.{NBSP}Jan"),
    ("J. A. Komenský", f"J.{NBSP}A.{NBSP}Komenský"),
    # další tituly a hodnosti před jménem
    ("MDDr. Jana Nová", f"MDDr.{NBSP}Jana"),
    ("PharmDr. Petr Malý", f"PharmDr.{NBSP}Petr"),
    ("MgA. Eva Tichá", f"MgA.{NBSP}Eva"),
    ("stržm. Karel Bílý", f"stržm.{NBSP}Karel"),
    ("pprap. Jan Novák", f"pprap.{NBSP}Jan"),
    ("pplk. gšt. Karel Svoboda", f"pplk.{NBSP}gšt.{NBSP}Karel"),
    # tituly za jménem drží u jména
    ("Pavel Černý, Ph.D., a další", f"Černý,{NBSP}Ph.D., a"),
    ("Jan Novák, CSc. uvedl", f"Novák,{NBSP}CSc. uvedl"),
    ("Petr Malý, LL.M., jako", f"Malý,{NBSP}LL.M., jako"),
    ("Eva Nová MBA podepsala", f"Nová{NBSP}MBA podepsala"),
    ("Jana Malá, DiS., vypověděla", f"Malá,{NBSP}DiS., vypověděla"),
    # zkratky, které drží u následujícího slova
    ("viz příloha P05", f"viz{NBSP}příloha"),
    ("např. svědek Novák", f"např.{NBSP}svědek"),
    ("bylo zde cca 20 osob", f"cca{NBSP}20"),
    ("popř. jiný orgán", f"popř.{NBSP}jiný"),
    ("viz obr. 3 a tab. 2", f"obr.{NBSP}3 a{NBSP}tab.{NBSP}2"),
    # jen celé slovo: „revize“ obsahuje „viz“, ale není to zkratka
    ("revize posudku", "revize posudku"),
    # zkratky předpisů se nerozpadají
    ("podle § 2910 o. z. platí", f"o.{NBSP}z. platí"),
    ("podle § 173 tr. ř. a dále", f"tr.{NBSP}ř. a"),
    ("ve smyslu o. s. ř. je", f"o.{NBSP}s.{NBSP}ř. je"),
    ("podle s. ř. s. a z. ř. s.",
     f"s.{NBSP}ř.{NBSP}s. a{NBSP}z.{NBSP}ř.{NBSP}s."),
    ("podle § 52 zák. práce", f"zák.{NBSP}práce"),
    # číslo předpisu drží u „Sb.“
    ("zákona č. 89/2012 Sb., občanský", f"89/2012{BOX1}{NBSP}Sb."),
    # pomlčky
    ("P05 – Doklad o výši", "P05 - Doklad"),
    # IČO podle právní úpravy, dříve IČ; DIČ a slovenské IČ DPH zůstávají
    ("společnost, IČ: 12345678, se sídlem", "IČO: 12345678"),
    ("IČ 12345678", "IČO 12345678"),
    ("DIČ CZ12345678", "DIČ CZ12345678"),
    ("IČ DPH SK2020123456", "IČ DPH SK2020123456"),
]

TESTY_BOX = [
    ("sp. zn. 12 Nt 345/2026", "12 Nt 345/2026"),
    ("č. j. ABCD-12345-67/TČ-2026-000089", "ABCD-12345-67/TČ-2026-000089"),
    ("nález sp. zn. I. ÚS 1234/25", f"I.{NBSP}ÚS 1234/25"),
    ("pod sp. zn. 2 KZV-12/2026", "2 KZV-12/2026"),
    ("č. j. VZV 5/2026-3", "VZV 5/2026-3"),
    ("na účet č. 123456789/0300", "123456789/0300"),
    ("usnesení 4 Tdo 123/2025", "4 Tdo 123/2025"),
]

TESTY_TYPST = [
    # středník za #box[...] typst pohltí jako konec výrazu
    ("věc 12 Nt 345/2026; dále", "#box[12 Nt 345/2026]\\; dále"),
    # tečka s písmenem za #box[...] by byla přístupem k poli
    ("usnesení 4 Tdo 123/2025.Dále", "#box[4 Tdo 123/2025]\\.Dále"),
    # závorka za #box[...] by byla voláním a sazba by spadla
    ("věc 4 Tdo 123/2025(viz výše)", "#box[4 Tdo 123/2025]\\(viz"),
    # číslo s tečkou na začátku řádku není položka číslovaného seznamu
    ("18. října 2026", f"18\\.{NBSP}října"),
    ("11. Žalobce v dovolání uvedl", "11\\. Žalobce"),
    ("první řádek\n2. druhý řádek", "\n2\\. druhý"),
    # uprostřed řádku se nic neescapuje
    ("dne 18. října 2026", f"dne 18.{NBSP}října"),
]

TESTY_NALEZ = [
    ("podle občanského zákoníku (dále jen „OZ“) platí",
     "zavedení zkratky přes „dále jen“"),
    ("zákon č. 99/1963 Sb., občanský soudní řád, dále jen „o. s. ř.“",
     "zavedení zkratky přes „dále jen“"),
]


@pytest.mark.parametrize(("vstup", "ocekavano"), TESTY)
def test_uprav(vstup, ocekavano):
    assert ocekavano in uprav(vstup, KANCELAR)


@pytest.mark.parametrize(("vstup", "uvnitr"), TESTY_BOX)
def test_neoddelitelny_blok(vstup, uvnitr):
    assert f"#box[{uvnitr}]" in do_typstu(uprav(vstup, KANCELAR))


@pytest.mark.parametrize(("vstup", "uryvek"), TESTY_TYPST)
def test_typst_escapovani(vstup, uryvek):
    assert uryvek in do_typstu(uprav(vstup, KANCELAR))


@pytest.mark.parametrize(("vstup", "popis"), TESTY_NALEZ)
def test_kontrola_hlasi(vstup, popis):
    assert any(n.startswith(popis) for n in zkontroluj(vstup, KANCELAR))


def test_kontrola_upraveneho_textu_je_cista():
    vzorek = ("Obviněný a jeho syn jel s poškozenou dne 28. 7. 2026 do banky "
              "v Písku, kde vybral 1 234 567 Kč, a to podle § 234 odst. 4 "
              "trestního zákoníku ve věci sp. zn. 12 Nt 345/2026.")
    assert zkontroluj(cisty(uprav(vzorek, KANCELAR)), KANCELAR) == []


@pytest.mark.parametrize(("vstup", "box"), [
    ("sp. zn. NZ 384/2024, N 430/2024 ze dne", "#box[NZ 384/2024, N 430/2024]"),
    ("notářský zápis NZ 12/2026 ze dne", "#box[NZ 12/2026]"),
    ("rejstřík N 15/2026 a Nz 7/2025", "#box[N 15/2026]"),
    ("komisař Sd 5/2024", "#box[Sd 5/2024]"),
])
def test_notarske_spisove_znacky(vstup, box):
    assert box in do_typstu(uprav(vstup, KANCELAR))


def test_kancelar_hlasi_pomlcku_ve_vete():
    n = zkontroluj("Dlužník o splátkách - došlo k dohodě - nevěděl.", KANCELAR)
    assert any(x.startswith("pomlčka ve větě") for x in n)
    n2 = zkontroluj("Je-li to tak, platí 15–20 % a Praha-Smíchov.", KANCELAR)
    assert not any(x.startswith("pomlčka ve větě") for x in n2)
