# cstypo

Česká typografická pravidla jako deterministická funkce v Pythonu. Text
dostane nezlomitelné mezery (vlnky) tam, kde podle pravidel nesmí skončit
řádek, neoddělitelné bloky pro spisové značky a čísla jednací a sjednocený
zápis údajů (PSČ, rodné číslo, IČO). Výstup umí jako prostý text i jako
markup pro [typst](https://typst.app). Balíček vznikl pro sazbu podání
advokátní kanceláře, proto zvlášť dobře zná právní texty.

```bash
pip install git+https://github.com/pravnikovo-info/cstypo
```

Bez závislostí, Python 3.10+. Balíček se jmenuje `pravnikovo-cstypo`,
modul `cstypo`. Na PyPI je pod jménem `cstypo` jiný, starší projekt
([yetty/cstypo](https://github.com/yetty/cstypo)); s ním nesouvisí a oba
najednou do jednoho prostředí neinstalujte.

## Použití

### Python

```python
from cstypo import uprav, cisty, do_typstu, zkontroluj, KANCELAR

text = "Podle § 234 odst. 4 písm. a) věc projedná soud pod sp. zn. 12 Nt 345/2026."

cisty(uprav(text))        # prostý text s nezlomitelnými mezerami (U+00A0)
do_typstu(uprav(text))    # typst markup: escapování + #box[12 Nt 345/2026]
zkontroluj(text)          # seznam porušení, prázdný = v pořádku

uprav(text, KANCELAR)     # jiný profil pravidel
```

### Příkazová řádka

```bash
cstypo podani.md                        # upravený text na stdout
cstypo --check podani.md                # nahlásí porušení, exit 1
cstypo --typst podani.md > telo.typ     # typst markup
cstypo --typst --ladit podani.md        # navíc zvýrazní vlnky a bloky
cstypo --profil kancelar podani.md      # profil kanceláře
```

`--check` se hodí do pre-commit hooku nebo CI.

### Typst

```python
from cstypo import uprav, do_typstu, LADENI

telo = do_typstu(uprav(text))
dokument = '#set text(lang: "cs")\n' + telo
# ladění: LADENI + telo podbarví nezlomitelné mezery a orámuje bloky;
# zlomy řádků se tím nezmění
```

## Profily

| | `ujc` (výchozí) | `kancelar` |
|---|---|---|
| tisíce | `1 234 567` (vázaná mezera) | `1.234.567` |
| telefon | `777 000 000` (nedělí se) | `+420777000000` |
| pomlčky | zůstávají, `slovo –` drží na konci řádku, `1948–1989` se nedělí | nahrazeny spojovníkem |
| `Č. j.` na začátku věty | beze změny | `č. j.` |
| citace „…“ | beze změny | kurzívou |
| řada teček `......` | beze změny | prázdné místo |
| kontrola „dále jen“, „tel.“, „e-mail“ | ne | ano |
| PSČ, rodné číslo, IČO | viz Zápis údajů | stejně |

Profil je neměnná dataclass, jednotlivé volby se mění kopií:

```python
from cstypo import UJC
muj = UJC.s(psc_bez_mezery=False, kurziva_latiny=False)
```

## Co pravidla dělají

Obecná pravidla podle [Internetové jazykové příručky ÚJČ AV ČR](https://prirucka.ujc.cas.cz/?id=880)
a ČSN 01 6910:

- jednopísmenné předložky a spojky (`k`, `s`, `v`, `z`, `o`, `u`, `a`, `i`)
  nezůstanou na konci řádku, ani za otevírací uvozovkou či závorkou;
  dvoupísmenná slova se záměrně neváží, zhoršuje to zarovnání do bloku;
- číslo a jednotka nebo značka (`50 %`, `10 kg`, `1 000 Kč`, `89/2012 Sb.`);
- datum (`28. 7. 2026`, `14. září`), iniciály (`J. A. Komenský`);
- tituly a hodnosti před jménem (`Mgr.`, `MDDr.`, `pplk. gšt.`) i za ním
  (`Novák, Ph.D.`, `LL.M.`, `MBA`);
- zkratky u následujícího slova nebo čísla (`viz`, `např.`, `cca`, `§`,
  `odst.`, `písm.`, `č.`, `str.` …) a víceslovné zkratky, které se nesmí
  rozpadnout (`t. č.`, `č. p.`);
- slova se spojovníkem se nedělí na spojovníku (`Je-li`).

Navíc pro právní texty:

- spisové značky, čísla jednací, nálezy ÚS a čísla účtů jako neoddělitelný
  blok: `12 Nt 345/2026`, `ABCD-12345-67/TČ-2026-000089`, `I. ÚS 1234/25`,
  `19-1234567890/0100`;
- celá citace ustanovení drží pohromadě: `§ 234 odst. 4 písm. a)`;
- právní forma drží u firmy v přesném zápisu z obchodního rejstříku
  (`s.r.o.` se nepřepisuje na `s. r. o.` ani naopak);
- zkratky předpisů se nerozpadají: `o. s. ř.`, `s. ř. s.`, `z. ř. s.`,
  `tr. ř.`, `o. z.`, `zák. práce`;
- latinské termíny kurzívou (`de facto`, `in dubio pro reo` …).

### Zápis údajů

- **IČO**, ne IČ: zákon č. 111/2009 Sb., o základních registrech, § 24
  písm. c) definuje identifikační číslo osoby jako „číselný kód označovaný
  zkratkou ‚IČO‘“. `DIČ` a slovenské `IČ DPH` se nemění.
- **PSČ bez mezery** (`11000 Praha 1`) a **rodné číslo bez lomítka**
  (`0102310010`): tak je předepisují datové formáty elektronických podání,
  např. vyhláška č. 241/2025 Sb. (PSČ „pětimístné číslo“, „přesně pět
  číslic“) a vyhláška č. 365/2014 Sb. (rodné číslo „ve formátu 8752025403 …
  (bez lomítka)“), obě měnící vyhlášku č. 418/2001 Sb. Lomítko se odstraní
  jen u čísla, které je platným rodným číslem; číslo posudku `032300/2026`
  zůstane. Kdo píše podle instrukce MSp o soudních písemnostech
  (č. 12/2017-OJD-ORG/36, § 10 odst. 6 uvádí vzor `339 02 Klatovy`), vypne
  volbu `psc_bez_mezery`.

## cstypo, nebo typst balíček vlna?

[vlna](https://typst.app/universe/package/vlna) ([iamanro/typst-vlna](https://github.com/iamanro/typst-vlna))
dělá nezlomitelné mezery přímo v typstu pomocí `show` pravidel. Obojí se
překrývá v obecných pravidlech, liší se v tom, kde a jak pracují:

- **vlna** funguje na jakémkoli `.typ` dokumentu, i ručně psaném, a zachová
  skok ze sazby do zdroje. Neumí měnit zápis (PSČ, IČO, tisíce), pravidla
  pro právní identifikátory nemá a sazbu zpomalí zhruba trojnásobně.
- **cstypo** upraví text předem, takže sazbu nic nezpomaluje, umí i zápis
  údajů a kontrolu (`--check`) a jeho výstup se dá použít i mimo typst
  (DOCX, e-mail). Na ručně psaný `.typ` se nepouští; je určen pro
  generované dokumenty.

Pro ručně psaný typst dokument použijte vlnu, pro text, který generujete
programem, cstypo. Kombinovat je lze: text upravený cstypo už vlnky má.

## Vývoj

```bash
python -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
.venv/bin/ruff check .
```

Pravidla vynucuje kód a test: každá změna pravidla má svůj testovací
případ. Všechna jména, firmy a čísla v testech jsou smyšlená.

## English

`cstypo` applies Czech typographic rules (non-breaking spaces after
single-letter prepositions, between numbers and units, in dates, titles,
abbreviations, and unbreakable court case numbers and legal citations) to
plain text and emits plain text or [typst](https://typst.app) markup. It
also normalises Czech identifiers (postal codes, birth numbers, IČO) and
includes a linter (`cstypo --check`). Zero dependencies, Python 3.10+.
MIT licensed.

## Licence

MIT, © 2026 pravnikovo.info
