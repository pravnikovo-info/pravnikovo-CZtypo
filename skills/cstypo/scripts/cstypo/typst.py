"""Výstup do typstu a do prostého textu."""

from __future__ import annotations

import re

from .znacky import BOX0, BOX1, GAP0, GAP1, IT0, IT1, NBSP

_ESCAPE = (("\\", "\\\\"), ("#", "\\#"), ("$", "\\$"), ("@", "\\@"),
           ("*", "\\*"), ("_", "\\_"), ("<", "\\<"), (">", "\\>"),
           ("[", "\\["), ("]", "\\]"))

# Ladicí režim sazby: vloží se do hlavičky typst dokumentu. Nezlomitelné
# mezery podbarví, neoddělitelné bloky orámuje. Zlomy řádků nemění, obojí
# jen kreslí.
LADENI = ('#show "\\u{a0}": highlight.with(fill: rgb("#bde"))\n'
          "#show box: set box(stroke: 0.4pt + red)\n")


def do_typstu(text: str) -> str:
    """Escapuje pro typst a rozbalí řídicí značky na typst markup."""
    for a, b in _ESCAPE:
        text = text.replace(a, b)
    # Vložený výraz (#box[...], #h(...)) by typst prodloužil o bezprostředně
    # následující znak: středník pohltí jako konec výrazu, závorku čte jako
    # volání („expected function, found content“) a tečku s písmenem jako
    # přístup k poli. Proto se tyto znaky escapují.
    text = re.sub(rf"([{BOX1}{GAP1}]);", r"\1\\;", text)
    text = re.sub(rf"([{BOX1}{GAP1}])\(", r"\1\\(", text)
    text = re.sub(rf"([{BOX1}{GAP1}])\.(?=[^\W\d_])", r"\1\\.", text)
    # „18. října 2026“ na začátku řádku by typst vysázel jako položku
    # číslovaného seznamu (číslo, tečka, mezera i nezlomitelná).
    text = re.sub(rf"(?m)^([ \t]*)(\d+)\.(?=[ \t{NBSP}])", r"\1\2\\.", text)
    text = (text.replace(BOX0, "#box[").replace(BOX1, "]")
                .replace(IT0, "_").replace(IT1, "_"))
    return re.sub(rf"{GAP0}([\d.]+){GAP1}", r"#h(\1cm)", text)


def cisty(text: str) -> str:
    """Vrátí text bez řídicích značek (pro DOCX, e-mail, kontrolu)."""
    # Prostý text nezná #box: mezery uvnitř bloku se změní na nezlomitelné,
    # aby spisová značka držela pohromadě i v DOCX nebo na webu.
    text = re.sub(rf"{BOX0}([^{BOX1}]*){BOX1}",
                  lambda m: BOX0 + m.group(1).replace(" ", NBSP) + BOX1, text)
    for ch in (BOX0, BOX1, IT0, IT1):
        text = text.replace(ch, "")
    return re.sub(rf"{GAP0}([\d.]+){GAP1}", lambda m: " " * 12, text)
