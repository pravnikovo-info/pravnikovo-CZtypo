# Šablona podání: funkce / Filing template: functions

Soubor `assets/typst/lib.typ`. Vše se importuje z něj, identita zvlášť:

```typst
#import "lib.typ": podani, adresat, participant, obhajce, zastupce,
  doc-title, prilohy, part, part-inline, vyrok, sig-criminal, sig-line,
  sig-detail, del, ins, cmt, komentare, redline-legenda
#import "identity/vzor.typ": vzor
#show: podani.with(identity: vzor, doc-footer: "ŽÁDOST",
                   doc-title-meta: "Žádost o nahlížení do spisu")
```

## Kostra podání (pořadí na první straně)

1. `#adresat([Název orgánu], [ulice], [PSČ obec], [IDDS: xxxxxxx])`:
   adresní blok vpravo, název tučně. `pred: [na vědomí:]` nebo
   `pred: [prostřednictvím]` (pak název v 2. pádě) nad názvem.
   Spisovou značku a datum přidej jako další řádky adresy
   (`[ke sp. zn. 1 T 24/2026]`, `[V Praze dne 5. 9. 2026]`).
2. `#participant([Obviněný:], [jméno, nar., bydliště])`: dvousloupcový
   řádek účastníka. `#participant([Obhájce:], [#obhajce()])` vloží údaje
   advokáta z identity. `#zastupce()` vloží řádek „práv. zast.:“
   s advokátem v 7. pádě (zapsaným v identitě).
3. `#doc-title[Název podání]`: nadpis s linkou.
4. `#prilohy([plná moc;], [usnesení ze dne …])`: přílohy patří na první
   stranu, před první `#part`; jinde překlad skončí chybou. Položky
   odrážkou, poslední končí tečkou; do 5 příloh bez čísel P01…
5. Tělo: `#part([I.], caption: [Skutkový stav])` a odstavce. Nadpis drží
   u následujícího textu (sticky), nezůstane sám na konci strany.
   `#part-inline[I. Prohlášení]` pro nadpis v řádku.
6. Petit nebo navrhovaný výrok: `#vyrok(([I.], [text]), ([II.], [text]))`.
7. Podpis: `#sig-criminal(zaver: [poslední odstavec textu])`. Poslední
   odstavec se předává podpisu, aby podpis nikdy nezůstal sám na stránce;
   bez `zaver` překlad ohlídá, že se podpis vejde, jinak skončí chybou.
   Prohlášení třetích osob: `#sig-line(name: [...])`, `#sig-detail(...)`.

## Další prvky

- `#fillspace(3cm)`: prázdné místo k doplnění (ne řada teček).
- `#rucne(8cm)`: linka k ručnímu vyplnění perem (jen formuláře).
- `#kod("heslo")`, `#duverne[...]`: strojové písmo a rámeček pro údaje.
- Redline (porovnání verzí): `#del[vypuštěno]`, `#ins[vloženo]`,
  `#cmt(1)` a na konci `#komentare(([důvod 1],))`; `#redline-legenda`.
- `bare: true` v `podani.with(...)`: bez hlavičky a patičky (prohlášení
  třetích osob na čistém papíře).

## Identita

Slovník v `identity/<klic>.typ`: hlavička (`pozadi`), patička (`paticka`),
písmo (`pismo.font` jako seznam s náhradami), okraje, odsazení adresního
bloku, podoba nadpisů, údaje advokáta (`obhajce`, `zastupce`, `podpis`).
Novou identitu založ kopií `vzor.typ`. Kdo je v hlavičce, je i v podpisu:
údaje advokáta se píší jen do identity.

## Písma

`vzor` používá Libertinus Serif vestavěný v typstu. `argumentum` používá
Cambrii a Garamond z Microsoft Office; bez nich `--input pisma=volna`
(Caladea a EB Garamond, volné licence OFL/Apache) nebo vestavěný Libertinus.
Komerční písma nikdy nepřibaluj.

## English summary

`podani` sets up the document for an identity; `adresat`, `participant`,
`doc-title`, `prilohy` (first page only), `part`, `vyrok` and `sig-criminal`
(pass the last paragraph as `zaver` so the signature never stands alone)
build a Czech filing. Identities live in `identity/*.typ`; copy `vzor.typ`
for a new firm. Redline helpers `del`, `ins`, `cmt`, `komentare` mark
changes between versions.
