"""Kontrola textu: nahlásí místa, která pravidla porušují."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .interpunkce import nalezy_interpunkce
from .profil import UJC, Profil
from .rodne_cislo import je_rodne_cislo
from .seznamy import JEDNOZNAKOVE, MAIL_RE, TEL_CZ_RE, TEL_INTL_RE, ZKRATKY
from .znacky import CZ_UPPER, NBSP

URL_RE = re.compile(r"(?:https?://|www\.)\S+")


@dataclass(frozen=True)
class Nalez:
    vzor: re.Pattern[str]
    popis: str
    jen_proza: bool = False  # v typst zdroji se nekontroluje (syntaxe)
    mimo_citace: bool = False  # v „citaci“ se ponechává originál
    mimo_telefony: bool = False  # telefonní číslo není číslo s tisíci
    mimo_adres: bool = False  # e-mail a webová adresa mají vlastní zápis


def _nalezy(profil: Profil) -> list[Nalez]:
    pismena = (JEDNOZNAKOVE if profil.vazat_a_i
               else JEDNOZNAKOVE.translate(str.maketrans("", "", "aiAI")))
    out = [
        Nalez(re.compile(rf"(?<![^\s„(\[])[{pismena}] (?=\S)"),
              "jednoznaková předložka nebo spojka s obyčejnou mezerou"),
        Nalez(re.compile(r"[…]{2,}|\.{5,}"),
              "řada teček jako místo pro doplnění"),
        Nalez(re.compile("|".join(re.escape(z) for z in
                                  ["t. č.", "č. p.", "č. e.", "č. or.",
                                   "st. p."])),
              "víceslovná zkratka s obyčejnou mezerou uvnitř"),
        Nalez(re.compile(r"\d (?:%|Kč|km|kg|EUR)(?![\w])"),
              "obyčejná mezera mezi číslem a jednotkou"),
        Nalez(re.compile("  +"), "dvojitá mezera", jen_proza=True),
        Nalez(re.compile(r"\s+[,;:!?](?!\))"), "mezera před interpunkcí",
              jen_proza=True),
        Nalez(re.compile(r'(?<![\w"])"[^"]{2,}"'),
              "anglické uvozovky (české jsou „ a “)", jen_proza=True),
        Nalez(re.compile(rf"\b(?:{'|'.join(ZKRATKY[:8])}) (?=\d)"
                         .replace("§", r"\§")),
              "zkratka odtržená od čísla obyčejnou mezerou"),
    ]
    if profil.psc_bez_mezery:
        out.append(Nalez(
            re.compile(rf"(?<!\d)\d{{3}} \d{{2}}(?=\s+[{CZ_UPPER}])"),
            "PSČ s mezerou (zapisuje se 76701, ne 767 01)"))
    if profil.ico:
        out.append(Nalez(re.compile(r"(?<![\wÁ-Ž])IČ(?=:?[ \xa0]?\d)"),
                         "zkratka „IČ“ (podle zákona č. 111/2009 Sb. „IČO“)"))
    if profil.rc_bez_lomitka:
        out.append(Nalez(re.compile(r"(?<!\d)\d{6}/\d{3,4}(?!\d)"),
                         "rodné číslo s lomítkem"))
    if profil.tisice == "tecka":
        out.append(Nalez(re.compile(rf"(?<=\d)[ {NBSP}](?=\d{{3}}(?!\d))"),
                         "tisíce oddělené mezerou (oddělovač je tečka)",
                         mimo_citace=True, mimo_telefony=True))
    else:
        out.append(Nalez(re.compile(r"(?<=\d) (?=\d{3}(?!\d))"),
                         "tisíce oddělené obyčejnou mezerou",
                         mimo_telefony=True))
    if profil.cj_vzdy_malym:
        out.append(Nalez(re.compile(r"\bČ\.\s*j\.|\bSp\.\s*zn\."),
                         "č. j. nebo sp. zn. velkým písmenem"))
    if profil.pomlcky_na_spojovnik:
        out.append(Nalez(re.compile(r"[—–]"),
                         "em dash nebo en dash (používá se spojovník)"))
    if profil.telefon_kompaktni:
        out.append(Nalez(
            re.compile(r"(?<![\d.,])[67]\d{2} \d{3} \d{3}(?![.,]?\d)"),
            "telefon s mezerami (má být +420777000000)"))
    if profil.kontrola_tel_email:
        out.append(Nalez(re.compile(r"\btel\.|\be-mail\b"),
                         "zkratka „tel.“ nebo „e-mail“"))
    if profil.interpunkce:
        out += [Nalez(n.vzor, n.popis, jen_proza=True, mimo_citace=not n.i_v_citaci,
                      mimo_adres=True)
                for n in nalezy_interpunkce(profil.pomlcky_na_spojovnik)]
    if profil.kontrola_dale_jen:
        out.append(Nalez(re.compile(r"\bdále\s+jen\b"),
                         "zavedení zkratky přes „dále jen“ "
                         "(píše se („X“) bez „dále jen“)", mimo_citace=True))
    return out


def je_typst(text: str) -> bool:
    """Pozná typst zdroj, kde jsou uvozovky součástí syntaxe."""
    return "#import" in text[:400] or "#show:" in text[:400]


def _maskuj(rx: re.Pattern[str], text: str) -> str:
    """Nahradí shody mezerami; délka textu i pozice nálezů zůstanou."""
    return rx.sub(lambda m: " " * len(m.group(0)), text)


def zkontroluj(text: str, profil: Profil = UJC) -> list[str]:
    """Vrátí seznam nálezů. Prázdný seznam znamená, že je text v pořádku."""
    maskovany = _maskuj(re.compile(r"„[^“]*“"), text)
    typst = je_typst(text)
    if typst:
        # vlastnosti dokumentu se nelámou, NBSP by tam byl jen podivný znak
        skryj = re.compile(r"(?m)^\s*(?:doc-title-meta|author|title):.*$")
        text = skryj.sub("", text)
        maskovany = skryj.sub("", maskovany)
    out = []
    for n in _nalezy(profil):
        if typst and n.jen_proza:
            continue
        zdroj = maskovany if n.mimo_citace else text
        if n.mimo_telefony:
            zdroj = _maskuj(TEL_CZ_RE, _maskuj(TEL_INTL_RE, zdroj))
        if n.mimo_adres:
            zdroj = _maskuj(URL_RE, _maskuj(MAIL_RE, zdroj))
        for m in n.vzor.finditer(zdroj):
            if (n.popis.startswith("rodné číslo")
                    and not je_rodne_cislo(*m.group(0).split("/"))):
                continue
            zac = max(0, m.start() - 30)
            vyrez = text[zac:m.end() + 30].replace("\n", " ")
            out.append(f"{n.popis}: ...{vyrez}...")
    return out
