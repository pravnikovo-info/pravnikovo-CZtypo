"""Seznamy slov, zkratek a vzory, se kterými pracují pravidla."""

from __future__ import annotations

import re

from .znacky import CZ_LOWER, CZ_UPPER, NBSP

# 1. Jednoznakové předložky a spojky nesmí zůstat na konci řádku.
# Dvouznakové (ve, se, ze, ke, na...) pravidlo nevyžaduje a jejich vázání
# zhoršuje zarovnání do bloku, proto se nevážou.
JEDNOZNAKOVE = "aikosuvzAIKOSUVZ"

# 2. Zkratky, které drží u svého čísla.
ZKRATKY = ["§", "č. j.", "sp. zn.", "ev. č.", "odst.", "písm.", "čl.", "č.",
           "bod", "sub", "str.", "odd.", "sv.", "příl.", "tj.", "tzv.", "nar.",
           "zn.", "resp.", "st.", "parc."]

# 2b. Víceslovné zkratky, které se nesmí rozpadnout uvnitř („t. č.“
# na konci řádku vypadá jako překlep).
VNITRNI = ["t. č.", "č. p.", "č. e.", "č. or.", "st. p.", "a. s. l.",
           "n. m.", "s. p.", "v. r.", "t. r.", "z. č.",
           # zkratky předpisů
           "o. s. ř.", "s. ř. s.", "z. ř. s.", "tr. ř.", "tr. zák.", "o. z.",
           "tr. z.", "zák. práce"]

# 2c. Zkratky, které drží u následujícího slova (jen celé slovo).
PRED_SLOVEM = ["viz", "např.", "cca", "popř.", "příp.", "kupř.", "obr.",
               "tab.", "kap.", "pozn.", "tzn.", "zvl.", "mj."]

# 3. Tituly a hodnosti před jménem. Za titulem musí následovat velké písmeno.
TITULY = ["Mgr", "JUDr", "Ing", "Bc", "MUDr", "PhDr", "RNDr", "MVDr", "PaedDr",
          "ThDr", "doc", "prof", "npor", "kpt", "nprap", "por", "plk",
          "MDDr", "PharmDr", "MgA", "BcA", "ThLic", "akad", "pprap", "ppor",
          "stržm", "nstržm", "prap", "šprap", "rtm", "nrtm", "mjr", "pplk",
          "genmjr", "genpor", "des", "čet", "rtn", "svob", "voj"]
TITULY_VICESLOVNE = ["pplk. gšt.", "plk. gšt.", "Ing. arch.", "dr. h. c."]

# 3b. Tituly za jménem.
TITULY_ZA = ["Ph.D.", "PhD.", "PhD", "Th.D.", "CSc.", "DrSc.", "DSc.", "DiS.",
             "MBA", "LL.M.", "MSc."]

# 4. Právní formy. Obchodní firma se píše přesně jako v obchodním rejstříku,
# pravidlo jen přiváže formu k názvu; s.r.o. se nepřevádí na s. r. o.
FORMY = [(f, f.replace(" ", NBSP)) for f in
         ["s. r. o.", "s.r.o.", "spol. s r. o.", "spol. s r.o.", "a. s.", "a.s.",
          "v. o. s.", "v.o.s.", "k. s.", "o. p. s.", "z. s.", "z. ú."]]

# 5. Jednotky a značky za číslem.
JEDNOTKY = ["%", "‰", "°C", "°", "Kč", "EUR", "USD", "CZK", "kg", "km", "cm",
            "mm", "ml", "min", "hod", "ks", "mil.", "tis.", "m²", "m2", "g",
            "t", "m", "l", "h", "Sb."]

MESICE = ["ledna", "února", "března", "dubna", "května", "června",
          "července", "srpna", "září", "října", "listopadu", "prosince"]

# 6. Latinské termíny do kurzívy.
LATIN = ["modus operandi", "modu operandi", "modem operandi", "ultima ratio",
         "in dubio pro reo", "in dubio pro libertate", "a contrario",
         "per analogiam", "de facto", "de iure", "in concreto",
         "ratio decidendi", "ex offo", "ad hoc", "de lege lata"]

# 7. Spisové značky, čísla jednací a čísla účtů se nesmí lámat.
IDENT_RE = re.compile(
    "(?:"
    # ABCD-12345-67/TČ-2026-000089, PMS-PMR-012345/2025-4
    # (tečka na konci je konec věty, do bloku nepatří)
    rf"[{CZ_UPPER}]{{2,6}}-[\w./-]*\d(?:[\w./-]*[\w/-])?"
    # 12 Nt 345/2026-14, 4 Tdo 123/2025, 2 NZT 12/2026-41
    rf"|\d{{1,3}}\s[{CZ_UPPER}][A-Za-z{CZ_LOWER}{CZ_UPPER}]{{0,4}}\s\d+"
    r"/\d{2,4}(?:-\d+)?"
    # 2 KZV-12/2026
    rf"|\d{{1,3}}\s[{CZ_UPPER}]{{2,4}}-\d+/\d{{2,4}}(?:-\d+)?"
    # VZV 23/2026-22
    rf"|[{CZ_UPPER}]{{2,4}}\s\d+/\d{{2,4}}(?:-\d+)?"
    # I. ÚS 1234/25, III. ÚS 99/17, Pl. ÚS 45/04
    rf"|(?:[IVX]{{1,4}}|Pl)\.\s?[{CZ_UPPER}]{{2}}\s?\d+/\d{{2,4}}"
    # čísla účtů 123456789/0300, 19-1234567890/0100
    r"|\d{2,}-?\d*/\d{4}"
    ")")

# Slovo tvaru písmena-písmena (Je-li, česko-slovenský). Číslice ne: ty
# pokrývá IDENT_RE a rozsahy se lámat smějí.
SPOJOVNIK_RE = re.compile(
    rf"[{CZ_LOWER}{CZ_UPPER}a-zA-Z]+-[{CZ_LOWER}{CZ_UPPER}a-zA-Z]+")

TEL_INTL_RE = re.compile(rf"\+\d{{1,3}}(?:[ {NBSP}]\d{{2,4}})+")
TEL_CZ_RE = re.compile(
    rf"(?<![\d.,])([67]\d{{2}})[ {NBSP}](\d{{3}})[ {NBSP}](\d{{3}})"
    r"(?![.,]?\d)(?!\s*(?:Kč|korun|Euro|EUR))")
MAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
LEADER_RE = re.compile(r"[…]{2,}|\.{5,}")
