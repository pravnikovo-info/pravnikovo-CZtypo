---
name: pravnikovo-cztypo
description: >-
  Česká typografie a sazba podání v typstu / Czech typography and typesetting
  of legal filings in typst. Nezlomitelné mezery (vlnky) za jednopísmennými
  předložkami, v datech, u čísel a jednotek, titulů a zkratek; neoddělitelné
  spisové značky, čísla jednací a citace ustanovení (§ 234 odst. 4 písm. a));
  PSČ bez mezery, rodné číslo bez lomítka, IČO místo IČ; české uvozovky;
  typst šablona podání s hlavičkou advokátní kanceláře. Použij vždy, když
  píšeš, upravuješ, kontroluješ nebo sázíš český text k tisku či do PDF
  (podání, žaloba, odvolání, stížnost, smlouva, dopis, posudek, web), když
  uživatel chce „zkontrolovat typografii“, „doplnit vlnky“, „aby se nelámalo
  na konci řádku“, „vysázet podání“ nebo generuješ typst/LaTeX/DOCX z české
  předlohy, i když slovo typografie nepadne. Use for any Czech text meant for
  print or PDF: non-breaking spaces, unbreakable case numbers, Czech legal
  citations, typst filing template.
---

# pravnikovo-CZtypo

[Česky](#česky) · [English](#english)

## Česky

Pravidla české sazby jsou deterministická a model je ručně dělá nespolehlivě:
nezlomitelná mezera (U+00A0) je neviditelná, snadno se zapomene a při
přepisování textu se ztratí. Neprováděj je proto ručně, ale skriptem, který
je aplikuje vždy stejně a je otestovaný. Skript nepotřebuje instalaci ani síť
(Python 3.10+); cesty jsou relativní ke složce tohoto skillu.

```bash
python3 scripts/cztypo_cli.py vstup.md > vystup.md     # upravený text
python3 scripts/cztypo_cli.py --check vstup.md         # jen nálezy, exit 1 při nálezu
python3 scripts/cztypo_cli.py --vlnky vstup.md         # náhled: vlnky jako ~
python3 scripts/cztypo_cli.py --typst vstup.md         # typst markup těla textu
python3 scripts/cztypo_cli.py --typst --ladit vstup.md # typst se zvýrazněnými vlnkami
echo "text" | python3 scripts/cztypo_cli.py --vlnky    # ze stdin
```

### Postup u textu

1. Napiš nebo uprav obsah běžně, s obyčejnými mezerami a rovnými uvozovkami.
   Vlnky, české uvozovky a trojtečku doplní skript.
2. Prožeň text skriptem a výsledek ulož do souboru, který se bude sázet.
   `--typst` pouštěj jen na tělo textu (odstavce), nikdy na celý typst
   soubor: escapuje `#`, `*`, `_`, `[`, `]` a rozbil by kód.
3. Ukaž uživateli změny přes `--vlnky` (vlnka = `~`), jinak je nevidí.
4. Hotový text zkontroluj `--check`; nálezy oprav ve zdroji a pusť znovu.
   Citace v „uvozovkách“ se nemění a kontrola v nich nic nehlásí.

U textu, který se nebude sázet (chat, prostý e-mail, poznámky), skill
nepoužívej: vlnky tam nic nepřinesou a ztíží kopírování.

### Sazba celého podání (typst)

Složka `assets/typst/` obsahuje šablonu podání: `lib.typ` (sazba),
`identity/vzor.typ` (smyšlená kancelář, písmo vestavěné v typstu),
`identity/argumentum.typ` (skutečná kancelář, ze které šablona vznikla)
a hotový příklad `priklad/podani.typ`. Postup:

1. Zkopíruj `assets/typst/` k uživateli. Pro jeho kancelář založ identitu
   kopií `identity/vzor.typ` a vyplň údaje (zástupce v 7. pádě zapiš ručně).
2. Tělo podání napiš do Markdownu a převeď skriptem s `--typst` (po
   odstavcích), jako to dělá `priklad/podani.typ` s `priklad/telo.typ`.
3. Sázej `typst compile --root <složka-šablony> podani.typ`.

Funkce šablony a jejich parametry popisuje `references/sablona.md`; načti
ho, než začneš podání skládat.

### Profily a volby

- `ujc` (výchozí): pravidla Internetové jazykové příručky ÚJČ AV ČR
  a ČSN 01 6910.
- `kancelar` (`--profil kancelar`): navíc zvyklosti jedné advokátní
  kanceláře (tečka v tisících, telefon `+420777000000`, spojovník místo
  pomlček, kurzíva citací, kontrola „dále jen“). Jen na výslovné přání.

### Co skript dělá a proč to neměnit ručně

- Vlnka za jednopísmennými předložkami a spojkami, v datu, mezi číslem
  a jednotkou, u titulů, iniciál a zkratek, v „Praha 1“; krátké poslední
  slovo odstavce drží u předchozího.
- Neoddělitelné bloky: spisové značky, čísla jednací, čísla účtů, slova se
  spojovníkem (`Je-li`). V typstu jsou v `#box[...]` a nezlomí se vůbec;
  v prostém textu mají uvnitř vlnky (zlom na spojovníku tam ohlídat nejde).
- Zápis údajů podle právní úpravy: **PSČ bez mezery** (`11000 Praha 1`)
  a **rodné číslo bez lomítka** (datové formáty, vyhláška č. 241/2025 Sb.
  a č. 365/2014 Sb.), **IČO** místo IČ (§ 24 písm. c) zákona č. 111/2009 Sb.).
  Tvar `110 00` z příruček sem nevracej; lomítko se odstraní jen u platného
  rodného čísla.
- Obchodní firma zůstává přesně jako v obchodním rejstříku: `s.r.o.` se
  nepřepisuje na `s. r. o.` ani naopak.
- Dvoupísmenná slova (`na`, `ve`, `do`) se záměrně neváží; zhoršuje to
  zarovnání do bloku a norma to nevyžaduje.

### Časté chyby

- Ruční vkládání `&nbsp;`, `~` nebo ` `: nekonzistentní, použij skript.
- Spuštění na zdrojový kód, YAML nebo typst šablonu: pravidla jsou pro
  přirozený český text.
- Opakované prohnání upraveného textu je bezpečné, ale `--typst` jen jednou.

## English

Czech typesetting rules are deterministic, and a model applying them by hand
is unreliable: a non-breaking space (U+00A0) is invisible and easily lost.
Run the bundled script instead (Python 3.10+, no installation, no network);
paths are relative to this skill's folder. The commands are listed above.

**Text workflow:** write content normally → run the script (`--typst` only on
body paragraphs, never on a whole typst file) → show the user the changes
with `--vlnky` (`~` marks a non-breaking space) → verify with `--check`.
Do not use the skill for text that will not be typeset (chat, plain email).

**Full filings:** `assets/typst/` holds the filing template (`lib.typ`), a
fictional identity (`identity/vzor.typ`, uses a font bundled with typst), the
identity of the law firm where the template originated
(`identity/argumentum.typ`) and a worked example (`priklad/podani.typ`).
Copy the folder, create the user's identity from `vzor.typ`, convert the body
with `--typst` and compile with `typst compile --root <template-folder>`.
Read `references/sablona.md` (Czech) before composing a filing.

**What the rules do:** non-breaking spaces after one-letter prepositions and
conjunctions, in dates, between numbers and units, after titles and
abbreviations; case numbers and reference numbers as unbreakable units;
postal codes without a space, birth numbers without a slash and „IČO“ as
required by Czech law (do not “fix” them back); company names exactly as in
the commercial register; Czech quotation marks, ellipsis and the
multiplication sign.

Source, tests and details: https://github.com/pravnikovo-info/pravnikovo-CZtypo
