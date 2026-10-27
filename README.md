# pravnikovo-CZtypo

**Česká typografie a sazba podání jako kód** · **Czech typography and legal typesetting as code**

[Česky](#česky) · [English](#english) · [pravnikovo.info](https://pravnikovo.info)

---

## Česky

pravnikovo-CZtypo má tři části, které fungují samostatně i spolu:

1. **Python balíček `cztypo`**: česká typografická pravidla jako deterministická
   funkce. Doplní nezlomitelné mezery (vlnky) tam, kde nesmí skončit řádek,
   udělá ze spisových značek a čísel jednacích neoddělitelné bloky a sjednotí
   zápis údajů (PSČ, rodné číslo, IČO). Výstup jako prostý text nebo typst.
2. **Typst šablona podání** (`typst/`): hlavička kanceláře jako parametr
   (identita), adresní blok, účastníci, číslované oddíly, petit, podpis,
   který nikdy nezůstane sám na stránce, a vyznačení změn mezi verzemi.
3. **Skill pro AI asistenty** (`skills/pravnikovo-cztypo/`): Claude i OpenAI
   Codex podle něj sami poznají, kdy pravidla použít, a místo ručního
   vkládání mezer zavolají skript.

Vzniklo v advokátní kanceláři argumentum.cz pro sazbu skutečných podání,
proto zvlášť dobře zná právní texty.

### Instalace

```bash
pip install git+https://github.com/pravnikovo-info/pravnikovo-CZtypo
```

Bez závislostí, Python 3.10+. Balíček `pravnikovo-CZtypo`, modul a příkaz
`cztypo`.

### Python

```python
from cztypo import uprav, cisty, do_typstu, zkontroluj, KANCELAR

text = 'Podle § 234 odst. 4 písm. a) věc projedná soud pod sp. zn. 12 Nt 345/2026.'

cisty(uprav(text))        # prostý text s nezlomitelnými mezerami (U+00A0)
do_typstu(uprav(text))    # typst markup: escapování + #box[12 Nt 345/2026]
zkontroluj(text)          # seznam porušení, prázdný = v pořádku
uprav(text, KANCELAR)     # jiný profil pravidel
```

### Příkazová řádka

```bash
cztypo podani.md                        # upravený text na stdout
cztypo --check podani.md                # nahlásí porušení, exit 1
cztypo --typst podani.md > telo.typ     # typst markup
cztypo --typst --ladit podani.md        # navíc zvýrazní vlnky a bloky
cztypo --profil kancelar podani.md      # profil kanceláře
```

### Typst šablona podání

```bash
python3 tools/priklad.py                                  # tělo z Markdownu přes cztypo
typst compile --root typst typst/priklad/podani.typ       # vzorová identita
typst compile --root typst --input identita=argumentum typst/priklad/podani.typ
```

```typst
#import "lib.typ": podani, adresat, participant, obhajce, doc-title, prilohy, part, sig-criminal
#import "identity/vzor.typ": vzor
#show: podani.with(identity: vzor, doc-footer: "STÍŽNOST")

#adresat([Obvodní státní zastupitelství pro Prahu 1], [Náměstí Příkladné 1/1], [11000 Praha 1])
#participant([Obhájce:], [#obhajce()])
#doc-title[Stížnost proti usnesení o zahájení trestního stíhání]
#prilohy([plná moc.])
#part([I.], caption: [Stížnost])
#include "telo.typ"
#sig-criminal(zaver: [V Praze dne 5. 9. 2026])
```

- **Identity:** `identity/vzor.typ` je smyšlená kancelář s písmem vestavěným
  v typstu (vysází se bez instalace). `identity/argumentum.typ` je skutečná
  kancelář, ze které šablona vznikla; pro vlastní kancelář zkopírujte vzor.
- **Písma:** identita argumentum používá Cambrii a Garamond z Microsoft
  Office. Ta jsou komerční a nepřibalujeme je; bez nich přidejte
  `--input pisma=volna` (volné náhrady Caladea a EB Garamond).
- Přehled všech funkcí: [`skills/pravnikovo-cztypo/references/sablona.md`](skills/pravnikovo-cztypo/references/sablona.md).

### Skill pro AI asistenty

Složka [`skills/pravnikovo-cztypo`](skills/pravnikovo-cztypo) je skill
v otevřeném formátu [Agent Skills](https://agentskills.io). Obsahuje vlastní
kopii balíčku i šablony, takže nepotřebuje instalaci ani internet.

| Kde | Jak nainstalovat |
|---|---|
| Claude Code | `cp -r skills/pravnikovo-cztypo ~/.claude/skills/` (nebo `.claude/skills/` v projektu) |
| Claude.ai, Claude Desktop | zabalit (níže) a nahrát v Nastavení → Capabilities → Skills; vyžaduje spouštění kódu |
| Claude API | nahrát složku přes Skills API |
| OpenAI Codex | `cp -r skills/pravnikovo-cztypo ~/.codex/skills/` |

```bash
cd skills && zip -r pravnikovo-cztypo.zip pravnikovo-cztypo -x 'pravnikovo-cztypo/evals/*'
```

Skill je ověřený na testovacích úlohách ve `skills/pravnikovo-cztypo/evals/`
(s ním a bez něj).

### Profily

| | `ujc` (výchozí) | `kancelar` |
|---|---|---|
| tisíce | `1 234 567` (vázaná mezera) | `1.234.567` |
| telefon | `777 000 000` (nedělí se) | `+420777000000` |
| pomlčky | zůstávají, `slovo –` drží na konci řádku, `1948–1989` se nedělí | nahrazeny spojovníkem |
| uvozovky, trojtečka, znak krát | `„…“`, `…`, `10 × 20` | stejně |
| citace „…“ | beze změny | kurzívou |
| kontrola „dále jen“, „tel.“, „e-mail“ | ne | ano |

Každou volbu lze měnit zvlášť: `UJC.s(vazat_a_i=False, uvozovky=False)`.

### Co pravidla dělají

Podle [Internetové jazykové příručky ÚJČ AV ČR](https://prirucka.ujc.cas.cz/?id=880)
a ČSN 01 6910:

- jednopísmenné předložky a spojky nezůstanou na konci řádku; dvoupísmenná
  slova se záměrně neváží (zhoršuje to zarovnání do bloku);
- číslo a jednotka (`50 %`, `1 000 Kč`, `89/2012 Sb.`), datum, iniciály,
  tituly před jménem i za ním, zkratky, „Praha 1“;
- české uvozovky, trojtečka, znak krát, krátké poslední slovo odstavce;
- slova se spojovníkem se nedělí na spojovníku (`Je-li`);
- mezery a interpunkce: opraví `,,uvozovky“`, `( ČR )`, `apod..`, `cca.`
  a mezeru před čárkou; nahlásí datum bez mezer, `viz.`, `tzv. „…“`, mezery
  u pomlčky a spojovníku, rozsah `15 – 20`, titul za jménem bez čárky aj.
  (volba `interpunkce`).

Pro právní texty navíc:

- spisové značky, čísla jednací, nálezy ÚS a čísla účtů jako neoddělitelný
  blok (`12 Nt 345/2026`, `I. ÚS 1234/25`, `ABCD-12345-67/TČ-2026-000089`);
- celá citace ustanovení drží pohromadě: `§ 234 odst. 4 písm. a)`;
- zkratky předpisů se nerozpadají: `o. s. ř.`, `tr. ř.`, `o. z.`;
- obchodní firma zůstává přesně jako v obchodním rejstříku (`s.r.o.`).

### Zápis údajů

- **IČO**, ne IČ: zákon č. 111/2009 Sb., o základních registrech, § 24
  písm. c) („číselný kód označovaný zkratkou ‚IČO‘“).
- **PSČ bez mezery** (`11000 Praha 1`) a **rodné číslo bez lomítka**: tak je
  předepisují datové formáty, např. vyhláška č. 241/2025 Sb. (PSČ „přesně pět
  číslic“) a vyhláška č. 365/2014 Sb. (rodné číslo „bez lomítka“). Vyhláška je
  obecně závazný předpis a má přednost před interními akty. Lomítko se
  odstraní jen u platného rodného čísla. Volbami `psc_bez_mezery`
  a `rc_bez_lomitka` lze úpravu vypnout.

### Příbuzné projekty

- [wilx/cstypo](https://github.com/wilx/cstypo) (Václav Haisman): česká
  typografie pro LuaLaTeX, balíček v CTAN. Pro LaTeX doporučujeme jeho.
- [yetty/cstypo](https://github.com/yetty/cstypo) (Juda Kaleta): starší
  Python balíček, z něhož jsme převzali několik pravidel (viz [NOTICE.md](NOTICE.md)).
- [vlna](https://typst.app/universe/package/vlna) (iamanro): nezlomitelné
  mezery přímo v typstu přes `show` pravidla. Hodí se pro ručně psaný typst;
  cztypo pro text, který generujete programem, a pro zápis údajů.

### Vývoj

```bash
python -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/pytest && .venv/bin/ruff check .
python3 tools/sync_skill.py        # po změně src/ nebo typst/ aktualizuje skill
```

Každá změna pravidla má svůj testovací případ. Všechna jména, firmy a čísla
v testech a příkladech jsou smyšlená.

### Licence

Kód MIT, © 2026 pravnikovo.info ([LICENSE](LICENSE)). Dokumentace a příklady
také pod CC BY 4.0. Převzatý kód a poděkování: [NOTICE.md](NOTICE.md).
Písma Microsoft Office nejsou součástí balíčku.

---

## English

pravnikovo-CZtypo has three parts that work on their own or together:

1. **Python package `cztypo`**: Czech typographic rules as a deterministic
   function. It inserts non-breaking spaces where a line must not end, turns
   court case numbers and reference numbers into unbreakable units and
   normalises identifiers (postal code, birth number, IČO). Output as plain
   text or typst markup.
2. **Typst filing template** (`typst/`): the law firm letterhead as a
   parameter (identity), address block, parties, numbered sections, petition,
   a signature that never stands alone on a page, and redline markup between
   versions.
3. **Skill for AI assistants** (`skills/pravnikovo-cztypo/`): Claude and
   OpenAI Codex recognise when to apply the rules and call the script instead
   of inserting spaces by hand.

It was built at the law firm argumentum.cz for typesetting real court
filings, so it handles legal texts particularly well.

### Installation

```bash
pip install git+https://github.com/pravnikovo-info/pravnikovo-CZtypo
```

No dependencies, Python 3.10+. Distribution `pravnikovo-CZtypo`, module and
command `cztypo`. Usage examples for Python, the command line and the typst
template are in the Czech section above; the code is the same.

### Typst template

`identity/vzor.typ` is a fictional firm that uses a font bundled with typst,
so it compiles without installing anything. `identity/argumentum.typ` is the
real firm where the template originated; copy `vzor.typ` for your own firm.
The argumentum identity uses Cambria and Garamond from Microsoft Office,
which are proprietary and not included; pass `--input pisma=volna` to use the
free replacements Caladea and EB Garamond.

### Skill for AI assistants

[`skills/pravnikovo-cztypo`](skills/pravnikovo-cztypo) follows the open
[Agent Skills](https://agentskills.io) format and bundles its own copy of the
package and template (no installation, no network). Install it by copying the
folder to `~/.claude/skills/` (Claude Code), `~/.codex/skills/` (OpenAI
Codex), or by uploading the zipped folder in Claude.ai / Claude Desktop
(Settings → Capabilities → Skills) or through the Claude Skills API.

### What the rules do

Following the Czech Language Institute guide (ÚJČ AV ČR) and ČSN 01 6910:
non-breaking spaces after one-letter prepositions and conjunctions, in dates,
between numbers and units, after titles and abbreviations; Czech quotation
marks, ellipsis, multiplication sign; a short last word of a paragraph kept
with the previous one; spacing and punctuation fixes (double-comma quotes,
spaces inside parentheses, doubled full stops) and checks (dates without
spaces, dash and hyphen spacing, „viz.“, titles without a comma, etc.).
For legal texts: unbreakable case numbers, reference
numbers and Constitutional Court citations, whole statutory citations
(`§ 234 odst. 4 písm. a)`) kept together, statute abbreviations, company
names exactly as registered. Postal codes are written without a space, birth
numbers without a slash and „IČO“ instead of „IČ“, as Czech regulations
require (Act No. 111/2009 Coll., Decrees No. 241/2025 and 365/2014 Coll.).
Profiles: `ujc` (default) and `kancelar` (house style of one law firm).

### Related projects

[wilx/cstypo](https://github.com/wilx/cstypo) (Czech typography for
LuaLaTeX, on CTAN; recommended for LaTeX), [yetty/cstypo](https://github.com/yetty/cstypo)
(older Python package; several rules adopted, see [NOTICE.md](NOTICE.md)),
[vlna](https://typst.app/universe/package/vlna) (non-breaking spaces inside
typst via show rules; good for hand-written typst).

### License

Code MIT, © 2026 pravnikovo.info ([LICENSE](LICENSE)). Documentation and
examples also under CC BY 4.0. Third-party code and acknowledgements:
[NOTICE.md](NOTICE.md). Microsoft Office fonts are not included.
