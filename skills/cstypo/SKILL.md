---
name: cstypo
description: >-
  Česká typografie a zápis údajů pro texty, které se budou sázet nebo odesílat:
  nezlomitelné mezery (vlnky) za jednopísmennými předložkami, v datech, u čísel
  a jednotek, titulů a zkratek; neoddělitelné spisové značky, čísla jednací
  a citace ustanovení (§ 234 odst. 4 písm. a)); PSČ bez mezery, rodné číslo bez
  lomítka, IČO místo IČ; výstup jako prostý text nebo typst. Použij vždy, když
  píšeš, upravuješ, kontroluješ nebo sázíš český text určený k tisku či PDF
  (podání, žaloba, odvolání, smlouva, dopis, posudek, web), když uživatel chce
  „zkontrolovat typografii“, „doplnit vlnky“, „nezlomitelné mezery“, „aby se
  nelámalo na konci řádku“, nebo generuješ typst/LaTeX/DOCX z české předlohy,
  i když slovo typografie nepadne. Czech typography: non-breaking spaces,
  unbreakable case numbers, Czech legal citations, typst output.
---

# cstypo: česká typografie jako kód

Pravidla české sazby jsou deterministická a model je ručně dělá nespolehlivě:
nezlomitelná mezera (U+00A0) je v textu neviditelná, snadno se zapomene a při
přepisování textu se ztratí. Proto je neprováděj ručně. Text proveď skriptem,
který pravidla aplikuje vždy stejně a je otestovaný.

Skript je ve složce skillu a nepotřebuje instalaci ani síť (Python 3.10+):

```bash
python3 scripts/cstypo_cli.py vstup.md > vystup.md     # upravený text
python3 scripts/cstypo_cli.py --check vstup.md         # jen nálezy, exit 1 při nálezu
python3 scripts/cstypo_cli.py --vlnky vstup.md         # náhled: vlnky jako ~
python3 scripts/cstypo_cli.py --typst vstup.md         # typst markup
python3 scripts/cstypo_cli.py --typst --ladit vstup.md # typst se zvýrazněnými vlnkami
echo "text" | python3 scripts/cstypo_cli.py --vlnky    # ze stdin
```

Cesty jsou relativní ke složce tohoto skillu.

## Postup

1. **Napiš nebo uprav obsah** běžně, s obyčejnými mezerami. O vlnky se
   nestarej, doplní je skript.
2. **Prožeň text skriptem** a výsledek ulož do souboru, který se bude sázet.
   Při psaní typst dokumentu použij `--typst` jen pro tělo textu (odstavce),
   ne pro celý soubor se šablonou: skript escapuje znaky `#`, `*`, `_`, `[`, `]`,
   takže by rozbil typst kód.
3. **Ukaž uživateli, co se změnilo**, pomocí `--vlnky` (vlnka = `~`). Jinak
   změny nevidí.
4. **Hotový text zkontroluj** `--check`. Nálezy oprav ve zdroji a skript
   pusť znovu. Nálezy v citovaném textu („…“) skript záměrně nehlásí, citace
   se nemění.

U textu, který se nebude sázet (chat, e-mail v prostém textu, poznámky),
skill nepoužívej: nezlomitelné mezery tam nic nepřinesou a ztíží kopírování.

## Profily

- `ujc` (výchozí): pravidla Internetové jazykové příručky ÚJČ AV ČR a ČSN 01 6910.
- `kancelar` (`--profil kancelar`): navíc zvyklosti jedné advokátní kanceláře:
  tečka v tisících (`1.234.567`), telefon `+420777000000`, spojovník místo
  pomlček, kurzíva citací, kontrola „dále jen“. Použij jen na výslovné přání.

## Co skript dělá a proč to neměnit ručně

- Vlnka za jednopísmennými předložkami a spojkami (`k`, `s`, `v`, `z`, `o`,
  `u`, `a`, `i`), v datu (`28. 7. 2026`), mezi číslem a jednotkou (`50 %`,
  `89/2012 Sb.`), u titulů (`Mgr. Jan`, `Novák, Ph.D.`), iniciál a zkratek
  (`viz`, `např.`, `§ 234 odst. 4 písm. a)`, `o. s. ř.`).
- Neoddělitelné bloky: spisové značky (`12 Nt 345/2026`, `I. ÚS 1234/25`),
  čísla jednací s pomlčkami a lomítky, čísla účtů, slova se spojovníkem (`Je-li`).
  V typstu jsou v `#box[...]` a nezlomí se vůbec. V prostém textu (DOCX, web)
  dostanou uvnitř vlnky, takže se nezlomí na mezeře; zlom na spojovníku tam
  ohlídat nejde, to umí jen typst výstup.
- Zápis údajů podle právní úpravy: **PSČ bez mezery** (`11000 Praha 1`) a
  **rodné číslo bez lomítka** (datové formáty, vyhláška č. 241/2025 Sb.
  a č. 365/2014 Sb.), **IČO** místo IČ (zákon č. 111/2009 Sb., § 24 písm. c)).
  Tvar `110 00` z jazykových příruček sem zpátky nevracej, i když vypadá
  „správněji“; lomítko se odstraní jen u platného rodného čísla.
- Obchodní firma zůstává přesně jako v obchodním rejstříku: `s.r.o.` se
  nepřepisuje na `s. r. o.` ani naopak, jen se přiváže k názvu.
- Dvoupísmenná slova (`na`, `ve`, `do`) se záměrně neváží: zhoršuje to
  zarovnání do bloku a norma to nevyžaduje.

## Časté chyby

- Ruční vkládání `&nbsp;`, `~` nebo ` ` do textu: nekonzistentní,
  použij skript.
- Spuštění na zdrojový kód, YAML nebo typst šablonu: pravidla jsou pro
  přirozený český text.
- Opakované prohnání už upraveného textu je bezpečné (výsledek se nezmění),
  ale `--typst` pouštěj jen jednou, escapování by se zdvojilo.
- V typst výstupu je `#box[...]` záměrný: drží spisovou značku pohromadě.

Zdroj, testy a podrobnosti: https://github.com/pravnikovo-info/cstypo
