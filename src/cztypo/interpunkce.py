"""Mezery a interpunkce: bezpečné opravy a kontroly častých chyb.

Opravy (``uprav_interpunkci``) dělají jen jednoznačné změny: uvozovky psané
jako dvě čárky, mezery uvnitř kulatých závorek a před interpunkcí, zdvojená
tečka za zkratkou, „cca.“ a nelámání dvojtečky v poměru „2 : 3“.
Doslovné citace v „uvozovkách“ se nemění.

Kontroly (``nalezy_interpunkce``) hlásí, co vyžaduje úsudek: datum bez
mezer (v názvu souboru je správně), chybějící mezeru za čárkou, mezery
u pomlčky a spojovníku, „viz.“, „tzv. „…““, titul za jménem bez čárky,
kumulaci interpunkce, minus a lomítko.

Pravidla podle IJP ÚJČ: tečka (?id=160), dvojtečka (161), uvozovky (162),
závorky (163), spojovník (164), pomlčka (165), lomítko (167), zkratky (780),
tituly (782), datum (810).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import NamedTuple

from .znacky import NBSP

_PISMENO = r"[^\W\d_]"
_CITACE = re.compile(r"(„[^“]*“)")
_TITULY_ZA = r"Ph\.D\.|Th\.D\.|CSc\.|DrSc\.|DSc\.|DiS\.|MBA|LL\.M\.|MPA"


class Nalez(NamedTuple):
    vzor: re.Pattern[str]
    popis: str
    i_v_citaci: bool = False  # hledá se i uvnitř „…“ (jinak se citace maskují)


def _mimo_citace(text: str, fn: Callable[[str], str]) -> str:
    return "".join(c if c.startswith("„") else fn(c) for c in _CITACE.split(text))


def _uvozovky_carky(text: str) -> str:
    # ,,text“ nebo ,,text" → „text“
    return re.sub(r'(?<![\w,]),,(?=\S)([^"“\n]*?)["“]', "„\\1“", text)


def _opravy(text: str) -> str:
    # mezery uvnitř závorek: ( ČR ) → (ČR)
    # jen kulaté: hranaté a složené patří syntaxi typst a markdownu („- [ ]“)
    text = re.sub(r"\( +(?=[^\s)])", "(", text)
    text = re.sub(r"(?<=[^\s(]) +\)", ")", text)
    # mezera před interpunkcí za slovem (ne „2 : 3“, ne výčet „a) , b)“)
    text = re.sub(rf"(?<={_PISMENO}) +(?=[,;:!?](?:\s|$))", "", text)
    # zdvojená tečka za zkratkou: apod.. → apod. (výpustka … zůstává)
    text = re.sub(rf"(?<={_PISMENO}\.)\.(?!\.)", "", text)
    # cca se píše bez tečky
    text = re.sub(r"\bcca\.(?=\s)", "cca", text)
    # poměr a dělení: dvojtečka s mezerami se neláme
    return re.sub(r"(?<=\d) : (?=\d)", f"{NBSP}:{NBSP}", text)


def uprav_interpunkci(text: str) -> str:
    """Opraví jednoznačné chyby mezer a interpunkce (mimo doslovné citace)."""
    return _mimo_citace(_uvozovky_carky(text), _opravy)


def nalezy_interpunkce(pomlcka_je_spojovnik: bool) -> list[Nalez]:
    """Kontroly k úsudku. Profil, který píše spojovník místo pomlčky, je nehlásí."""
    out = [
        Nalez(re.compile(r"(?<![\d.])\d{1,2}\.\d{1,2}\.(?:19|20)\d{2}(?!\d)"),
              "datum bez mezer (píše se 25. 7. 2020; v názvech souborů ponechat)"),
        Nalez(re.compile(rf"(?<={_PISMENO})[,;](?={_PISMENO})"),
              "chybí mezera za čárkou nebo středníkem"),
        Nalez(re.compile(rf"(?<={_PISMENO})[–—](?=\s)|(?<=\s)[–—](?={_PISMENO})"),
              "pomlčka bez mezery na jedné straně (mezi slovy má mezery z obou stran)"),
        Nalez(re.compile(r"(?<![\d.])\d+ [–—] \d+(?![\d.])"),
              "rozsah čísel s mezerami (píše se 15–20)"),
        Nalez(re.compile(rf"(?<={_PISMENO}) -li\b"),
              "spojovník u -li s mezerou (píše se nezazní-li)"),
        Nalez(re.compile(r"\bviz\.(?= [^\W\d_])"),
              "„viz“ bez tečky (rozkazovací způsob, ne zkratka)"),
        Nalez(re.compile(r"\btzv\. „"),
              "po „tzv.“ se uvozovky nepíší", i_v_citaci=True),
        Nalez(re.compile(rf"(?<=[a-záčďéěíňóřšťúůýž]) (?:{_TITULY_ZA})(?!\w)"),
              "titul za jménem se odděluje čárkou (Novák, Ph.D.)"),
        Nalez(re.compile(r"[?!,;:]\.(?!\.)|[?!]{3,}"),
              "kumulace interpunkce (?. !. ,.)"),
        Nalez(re.compile(r"(?:(?<=\s)|(?<=^)|(?<=\())-(?=\d+(?:,\d+)? ?(?:°|%|Kč))",
                         re.M),
              "znak minus: záporné číslo se píše se znakem − (−18 °C)"),
        Nalez(re.compile(r"(?<!\S)[^\W\d_]{1,3} / [^\W\d_]{1,3}(?!\S)"),
              "lomítko s mezerami mezi jednoslovnými výrazy (50 km/h)"),
    ]
    if not pomlcka_je_spojovnik:
        out.append(Nalez(re.compile(rf"(?<={_PISMENO}) - (?={_PISMENO})"),
                         "spojovník s mezerami (pomlčka „–“ nebo spojovník bez mezer)"))
    return out
