"""Profily: které úpravy se provádějí.

Výchozí profil ``UJC`` se drží Internetové jazykové příručky ÚJČ AV ČR
(https://prirucka.ujc.cas.cz/?id=880) a ČSN 01 6910. Navíc zapisuje PSČ
bez mezery, rodné číslo bez lomítka a zkratku IČO místo dřívějšího IČ
(viz README, oddíl Zápis údajů). Každé z toho lze vypnout.

Profil ``KANCELAR`` přidává domácí zvyklosti advokátní kanceláře, ze které
balíček vznikl: tečku jako oddělovač tisíců, telefon ve tvaru +420777000000,
spojovník místo pomlček, kurzívu citací a přísnější kontrolu.
"""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Profil:
    """Nastavení úprav. Neměnný; změnu udělá ``dataclasses.replace``."""

    # zápis údajů
    psc_bez_mezery: bool = True  # 110 00 -> 11000
    rc_bez_lomitka: bool = True  # 010231/0010 -> 0102310010 (jen platné RČ)
    ico: bool = True  # IČ 12345678 -> IČO 12345678 (§ 24 písm. c) z. 111/2009 Sb.)
    tisice: str = "mezera"  # "mezera" = vázaná mezera, "tecka" = 1.234.567
    telefon_kompaktni: bool = False  # 777 000 000 -> +420777000000
    # sazba
    pomlcky_na_spojovnik: bool = False  # – a — nahradí spojovníkem
    kurziva_citaci: bool = False  # text v „uvozovkách“ kurzívou
    kurziva_latiny: bool = True  # de facto, ad hoc ... kurzívou
    cj_vzdy_malym: bool = False  # Č. j. -> č. j. i na začátku věty
    tecky_na_mezeru: bool = False  # ........ (místo pro doplnění) -> mezera
    # kontrola
    kontrola_dale_jen: bool = False  # hlásí zavedení zkratky „dále jen“
    kontrola_tel_email: bool = False  # hlásí zkratky „tel.“ a „e-mail“

    def s(self, **zmeny: object) -> Profil:
        """Vrátí kopii profilu se změněnými hodnotami."""
        return replace(self, **zmeny)

    def __post_init__(self) -> None:
        if self.tisice not in ("mezera", "tecka"):
            raise ValueError("tisice musí být 'mezera' nebo 'tecka'")


UJC = Profil()

KANCELAR = Profil(
    tisice="tecka",
    telefon_kompaktni=True,
    pomlcky_na_spojovnik=True,
    kurziva_citaci=True,
    cj_vzdy_malym=True,
    tecky_na_mezeru=True,
    kontrola_dale_jen=True,
    kontrola_tel_email=True,
)

PROFILY = {"ujc": UJC, "kancelar": KANCELAR}
