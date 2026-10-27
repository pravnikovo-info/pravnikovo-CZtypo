"""Úprava textu: nezlomitelné mezery, neoddělitelné bloky a zápis údajů.

Funkce ``uprav`` vrací text s řídicími značkami (viz ``znacky``). Pro typst
je rozbalí ``do_typstu``, pro prostý text je odstraní ``cisty``.
"""

from __future__ import annotations

import re

from .profil import UJC, Profil
from .rodne_cislo import je_rodne_cislo
from .seznamy import (
    FORMY,
    IDENT_RE,
    JEDNOTKY,
    JEDNOZNAKOVE,
    LATIN,
    LEADER_RE,
    MAIL_RE,
    MESICE,
    PRED_SLOVEM,
    SPOJOVNIK_RE,
    TEL_CZ_RE,
    TEL_INTL_RE,
    TITULY,
    TITULY_VICESLOVNE,
    TITULY_ZA,
    VNITRNI,
    ZKRATKY,
)
from .znacky import BOX0, BOX1, CZ_LOWER, CZ_UPPER, GAP0, GAP1, IT0, IT1, NBSP, S0, S1

ICO_RE = re.compile(r"(?<![\wÁ-Ž])IČ(?=:?[ \xa0]?\d)")
_TISICE_RE = re.compile(rf"(?<=\d)[ {NBSP}](?=\d{{3}}(?!\d))")


def _tisice(s: str, profil: Profil) -> str:
    """Oddělovač tisíců: vázaná mezera (ÚJČ), nebo tečka (profil kanceláře)."""
    nahrada = "." if profil.tisice == "tecka" else NBSP
    prev = None
    while prev != s:
        prev = s
        s = _TISICE_RE.sub(nahrada, s)
    return s


def _odloz(text: str, profil: Profil, stash: list[str]) -> str:
    """Telefony a e-maily odloží, ať na ně nesáhne pravidlo na tisíce."""
    def keep(val: str) -> str:
        stash.append(val)
        return f"{S0}{len(stash) - 1}{S1}"

    if profil.telefon_kompaktni:
        text = TEL_INTL_RE.sub(
            lambda m: keep(re.sub(rf"[ {NBSP}]", "", m.group(0))), text)
        text = TEL_CZ_RE.sub(lambda m: keep("+420" + "".join(m.groups())),
                             text)
    else:
        # ÚJČ: skupiny číslic telefonu se nedělí, mezery zůstávají
        text = TEL_INTL_RE.sub(
            lambda m: keep(m.group(0).replace(" ", NBSP)), text)
        text = TEL_CZ_RE.sub(lambda m: keep(NBSP.join(m.groups())), text)
    return MAIL_RE.sub(lambda m: keep(m.group(0)), text)


def _udaje(text: str, profil: Profil) -> str:
    """Zápis údajů: tečky, pomlčky, č. j., IČO, PSČ, rodné číslo."""
    if profil.tecky_na_mezeru:
        # řada teček není místo pro doplnění; nahradí ji prostá mezera
        text = LEADER_RE.sub(
            lambda m: GAP0
            + f"{min(5.5, max(1.8, len(m.group(0)) * 0.22)):.1f}" + GAP1,
            text)
    if profil.pomlcky_na_spojovnik:
        text = text.replace("—", "-").replace("–", "-")
    else:
        # pomlčka s mezerami zůstává na konci řádku, rozsah se nedělí
        text = re.sub(r" ([–—]) ", f"{NBSP}\\1 ", text)
        text = re.sub(r"\d+[–—]\d+", lambda m: BOX0 + m.group(0) + BOX1, text)
    if profil.cj_vzdy_malym:
        text = re.sub(r"\bČ\.\s*j\.", "č. j.", text)
        text = re.sub(r"\bSp\.\s*zn\.", "sp. zn.", text)
    if profil.ico:
        # IČO podle § 24 písm. c) zákona č. 111/2009 Sb., dříve IČ;
        # jen před číslem, DIČ a slovenské „IČ DPH“ zůstávají
        text = ICO_RE.sub("IČO", text)
    psc = rf"(?<!\d)(\d{{3}}) (\d{{2}})(?=\s+[{CZ_UPPER}])"
    if profil.psc_bez_mezery:
        text = re.sub(psc, r"\1\2", text)
    else:
        text = re.sub(psc, f"\\1{NBSP}\\2", text)
    if profil.rc_bez_lomitka:
        text = re.sub(r"(?<!\d)(\d{6})/(\d{3,4})(?!\d)",
                      lambda m: (m.group(1) + m.group(2)
                                 if je_rodne_cislo(m.group(1), m.group(2))
                                 else m.group(0)), text)
    return text


def _kurziva_a_tisice(text: str, profil: Profil) -> str:
    """Citace a latinské termíny kurzívou; tisíce mimo citace."""
    if profil.kurziva_citaci:
        # uvnitř citace se tisíce nepřepisují, cituje se originál
        parts = re.split(r"(„[^“]*“)", text)
        text = "".join(IT0 + seg + IT1 if seg.startswith("„")
                       else _tisice(seg, profil) for seg in parts)
    else:
        text = _tisice(text, profil)
    if profil.kurziva_latiny:
        for term in LATIN:
            text = re.sub(rf"\b{re.escape(term)}\b", IT0 + term + IT1, text)
    return text


def _data_a_osoby(text: str) -> str:
    """Data, právní formy, tituly, iniciály."""
    # datum se nesmí rozdělit
    text = re.sub(r"(\d{1,2})\. (\d{1,2})\. (\d{4})",
                  f"\\1.{NBSP}\\2.{NBSP}\\3", text)
    text = re.sub(rf"\b(\d{{1,2}})\. (?=(?:{'|'.join(MESICE)})\b)",
                  f"\\1.{NBSP}", text)
    # právní forma drží u názvu subjektu
    for old, new in FORMY:
        text = text.replace(", " + old, "," + NBSP + new)
        text = text.replace(" " + old, NBSP + new)
    # víceslovná hodnost nebo titul drží pohromadě i u jména
    for t in TITULY_VICESLOVNE:
        text = re.sub(rf"(?<!\w){re.escape(t)} (?=[{CZ_UPPER}])",
                      t.replace(" ", NBSP) + NBSP, text)
    tituly = "|".join(sorted(TITULY, key=len, reverse=True))
    text = re.sub(rf"(?<!\w)({tituly})\. (?=[{CZ_UPPER}])",
                  f"\\1.{NBSP}", text)
    # titul za jménem drží u jména: „Novák, Ph.D.“
    za = "|".join(re.escape(t)
                  for t in sorted(TITULY_ZA, key=len, reverse=True))
    text = re.sub(rf"(?<=\w)(,?) (?=(?:{za})(?!\w))", f"\\1{NBSP}", text)
    # zkratka drží u následujícího slova: „viz příloha“, „cca 20“
    pred = "|".join(re.escape(z) for z in PRED_SLOVEM)
    text = re.sub(rf"(?<!\w)({pred}) (?=\S)", f"\\1{NBSP}", text)
    # iniciála drží u dalšího jména
    return re.sub(rf"(?<!\S)([{CZ_UPPER}])\. (?=[{CZ_UPPER}])",
                  f"\\1.{NBSP}", text)


def _zkratky_a_cisla(text: str, profil: Profil) -> str:
    """Víceslovné zkratky, zkratky u čísla, jednotky, předložky, paragrafy."""
    # Jen celá slova, jinak by „o. z.“ chytlo i konec „do. z…“. Delší první,
    # aby „tr. zák.“ nepřebilo „tr. z.“. Stojí-li za zkratkou číslo, drží
    # i u něj: „č. p. 4137“ je jeden údaj.
    for a in sorted(VNITRNI, key=len, reverse=True):
        glued = a.replace(" ", NBSP)
        text = re.sub(rf"(?<!\w){re.escape(a)}(?!\w)", glued, text)
        text = re.sub(rf"{re.escape(glued)} (?=\d)", glued + NBSP, text)
    for a in sorted(ZKRATKY, key=len, reverse=True):
        text = text.replace(a + " ", a.replace(" ", NBSP) + NBSP)
    # číslo a jednotka nebo značka
    jednotky = "|".join(re.escape(j) for j in JEDNOTKY)
    text = re.sub(rf"(?<=\d) (?=(?:{jednotky})(?![\w]))", NBSP, text)
    # Jednoznaková předložka nebo spojka nesmí zůstat na konci řádku, ani
    # za otevírací uvozovkou nebo závorkou („k těmto záznamům“).
    pismena = (JEDNOZNAKOVE if profil.vazat_a_i
               else JEDNOZNAKOVE.translate(str.maketrans("", "", "aiAI")))
    text = re.sub(rf"(?<![^\s„(\[])([{pismena}]) (?=\S)",
                  f"\\1{NBSP}", text)
    # číslo drží u navazujícího členění: § 216 odst. 1 písm. c). Před čárkou
    # se lámat smí, jinak by výčet § 234 odst. 1, odst. 4 držel v kuse.
    return re.sub(r"(?<=[\d)])[ ]+(?=(?:odst|písm|věty|věta|bodu|bod)\b)",
                  NBSP, text)


def _prevzata(text: str, profil: Profil) -> str:
    """Uvozovky, trojtečka a znak krát (podle yetty/cstypo, MIT)."""
    if profil.trojtecka:
        text = re.sub(r"(?<!\.)\.{3}(?!\.)", "…", text)
    if profil.uvozovky:
        text = re.sub(r'(?<!["\w])"(?![ "])([^"\n]+?)(?<![ "])"(?!")',
                      "„\\1“", text)
        text = re.sub(r"(?<!['\w])'(?![ '])([^'\n]+?)(?<![ '])'(?![\w'])",
                      "‚\\1‘", text)
    if profil.krat:
        cislo = r"\d+(?:,\d+)?"
        text = re.sub(rf"(?<![\w.,])({cislo}) ?x ?({cislo})(?!\w)",
                      f"\\1{NBSP}×{NBSP}\\2", text)
        text = re.sub(r"(?<=\d)x(?=[ ,.]|$)", "×", text, flags=re.M)
    return text


def _nazev_cislo(text: str) -> str:
    """Název a číslo drží pohromadě: Praha 1, Dlouhá 12 (ÚJČ)."""
    return re.sub(
        rf"(\b[{CZ_UPPER}][{CZ_LOWER}]+) (\d{{1,3}})(?![\d/]|[.,:]\d|\.)",
        f"\\1{NBSP}\\2", text)


_RIDICI = re.compile(r"[\x00-\x0b]")


def _posledni_slovo(text: str) -> str:
    """Krátké poslední slovo odstavce nezůstane samo na řádku (yetty/cstypo).

    Platí jen pro odstavce delší než 50 znaků; nadpis nebo buňka tabulky se
    nechá být. Za krátké se počítá slovo do šesti znaků i s interpunkcí.
    """
    def odstavec(par: str) -> str:
        if len(_RIDICI.sub("", par)) <= 50:
            return par
        m = re.search(r" (\S+)(\s*)$", par)
        if m and len(_RIDICI.sub("", m.group(1))) <= 6:
            return par[:m.start()] + NBSP + par[m.start() + 1:]
        return par
    casti = re.split(r"(\n\s*\n)", text)
    return "".join(c if i % 2 else odstavec(c) for i, c in enumerate(casti))


def uprav(text: str, profil: Profil = UJC) -> str:
    """Aplikuje pravidla profilu. Vrací text s řídicími značkami."""
    stash: list[str] = []
    text = _odloz(text, profil, stash)
    text = _prevzata(text, profil)
    text = _udaje(text, profil)
    text = _kurziva_a_tisice(text, profil)
    text = _data_a_osoby(text)
    text = _zkratky_a_cisla(text, profil)
    if profil.nazev_cislo:
        text = _nazev_cislo(text)
    # Slovo se spojovníkem se nesmí lámat u spojovníku: „Je-“ a „li“ na
    # dvou řádcích vypadá jako překlep sazby.
    text = SPOJOVNIK_RE.sub(lambda m: BOX0 + m.group(0) + BOX1, text)
    # spisové značky, čísla jednací a čísla účtů se nesmí lámat
    text = IDENT_RE.sub(lambda m: BOX0 + m.group(0) + BOX1, text)
    # vrátit odložené jako neoddělitelné
    text = re.sub(rf"{S0}(\d+){S1}",
                  lambda m: BOX0 + stash[int(m.group(1))] + BOX1, text)
    return _posledni_slovo(text) if profil.posledni_slovo else text
