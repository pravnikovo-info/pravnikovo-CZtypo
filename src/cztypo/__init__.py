"""Česká typografická pravidla jako deterministická funkce.

    >>> from cztypo import uprav, cisty
    >>> cisty(uprav("jel s kolegou do Brna"))
    'jel s\\xa0kolegou do Brna'
"""

from __future__ import annotations

from .kontrola import zkontroluj
from .pravidla import uprav
from .profil import KANCELAR, PROFILY, UJC, Profil
from .rodne_cislo import je_rodne_cislo
from .typst import LADENI, cisty, do_typstu
from .znacky import NBSP

__version__ = "0.3.0"

__all__ = ["KANCELAR", "LADENI", "NBSP", "PROFILY", "UJC", "Profil",
           "cisty", "do_typstu", "je_rodne_cislo", "uprav", "zkontroluj",
           "__version__"]
