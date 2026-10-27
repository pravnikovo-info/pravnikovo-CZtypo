"""Rozpoznání rodného čísla."""

from __future__ import annotations


def je_rodne_cislo(prvni: str, druhe: str) -> bool:
    """Rozliší rodné číslo od jiných čísel tvaru 123456/2026.

    Číslo znaleckého posudku nebo evidenční číslo může mít stejný tvar a
    lomítko se mu brát nesmí. Kontroluje se měsíc (i s přičtením 20, 50
    a 70), den a u desetimístného čísla dělitelnost jedenácti, včetně
    výjimky, kdy zbytek devítimístného základu je 10 a kontrolní číslice 0.
    """
    if len(prvni) != 6 or len(druhe) not in (3, 4):
        return False
    mesic, den = int(prvni[2:4]), int(prvni[4:6])
    if not (1 <= mesic <= 12 or 21 <= mesic <= 32
            or 51 <= mesic <= 62 or 71 <= mesic <= 82):
        return False
    if not 1 <= den <= 31:
        return False
    if len(druhe) == 3:
        return True  # rodná čísla před rokem 1954 kontrolní číslici nemají
    return (int(prvni + druhe) % 11 == 0
            or (int(prvni + druhe[:3]) % 11 == 10 and druhe[3] == "0"))
