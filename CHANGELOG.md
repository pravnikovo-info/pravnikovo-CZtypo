# Změny / Changelog

## 0.3.0 – 2026-10-27

**Česky**
- Nový název **pravnikovo-CZtypo** (modul a příkaz `cztypo`, skill
  `pravnikovo-cztypo`). Název „cstypo“ patří projektům yetty/cstypo
  a wilx/cstypo.
- Typst šablona podání (`typst/`): identita jako parametr, vzorová identita
  s vestavěným písmem, identita argumentum.cz, příklad a testy v CI.
- Skill obsahuje i šablonu a návod k sazbě celého podání.
- Převzatá pravidla (MIT, viz NOTICE.md): české uvozovky, trojtečka, znak
  krát, krátké poslední slovo odstavce (yetty/cstypo); volba vázání spojek
  „a“ a „i“ (wilx/cstypo). Nově se váže i „Praha 1“, „Dlouhá 12“.
- Dokumentace dvojjazyčně; dokumentace a příklady i pod CC BY 4.0.

**English**
- New name **pravnikovo-CZtypo** (module and command `cztypo`, skill
  `pravnikovo-cztypo`); “cstypo” belongs to yetty/cstypo and wilx/cstypo.
- Typst filing template (`typst/`) with identities, an example and CI tests.
- The skill now bundles the template and explains full filings.
- Adopted rules (MIT, see NOTICE.md): Czech quotes, ellipsis,
  multiplication sign, short last word of a paragraph; switch for binding
  “a” and “i”. Also binds “Praha 1”, “Dlouhá 12”.
- Bilingual documentation; docs and examples also under CC BY 4.0.

## 0.2.0 – 2026-10-27

- Skill pro AI asistenty (`skills/cstypo`, formát Agent Skills): Claude Code,
  Claude.ai, Claude API, OpenAI Codex. Běží bez instalace; spouštěč umí
  `--vlnky` (náhled nezlomitelných mezer jako `~`). Testovací úlohy v `evals/`.
- Prostý text (`cisty`): mezery uvnitř spisových značek a čísel jednacích jsou
  nezlomitelné, značka drží pohromadě i v DOCX nebo na webu.
- Tečka za větou už nepadá do bloku čísla jednacího.

## 0.1.0 – 2026-10-27

První veřejná verze.

- Pravidla ÚJČ: jednopísmenné předložky a spojky, číslo a jednotka, data,
  iniciály, tituly před jménem i za ním, zkratky u slova a u čísla,
  víceslovné zkratky, slova se spojovníkem.
- Právní texty: spisové značky, čísla jednací, nálezy ÚS a čísla účtů jako
  neoddělitelný blok, citace ustanovení, právní formy, zkratky předpisů.
- Zápis údajů: IČO, PSČ bez mezery, rodné číslo bez lomítka.
- Profily `ujc` (výchozí) a `kancelar`.
- Výstup pro typst (`do_typstu`, ladicí režim `LADENI`) a prostý text.
- Kontrola (`zkontroluj`, `cstypo --check`).
