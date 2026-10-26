"""Znaky a řídicí značky sdílené všemi moduly."""

from __future__ import annotations

NBSP = " "
CZ_UPPER = "A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ"
CZ_LOWER = "a-záčďéěíňóřšťúůýž"

# Řídicí značky. Přežijí escapování a rozbalí se až v do_typstu();
# cisty() je odstraní pro výstup do prostého textu.
BOX0, BOX1 = "\x00", "\x01"  # neoddělitelný blok
IT0, IT1 = "\x02", "\x03"  # kurzíva
GAP0, GAP1 = "\x08", "\x0b"  # vodorovná mezera v cm
S0, S1 = "\x06", "\x07"  # interní odkládací značka
