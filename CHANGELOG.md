# Změny / Changelog

## 0.4.1 – 2026-10-27

- **Česky:** spisové značky notářů se nelámou: „NZ 384/2024, N 430/2024“ je
  jeden blok, stejně N, Nz, Sd, Sdu, EZ, EVZ, U (i citace sbírky
  „N 222/83 SbNU“). Profil kanceláře nově hlásí pomlčku ve větě (i jako
  „ - “), aby autor větu přeformuloval (volba `kontrola_pomlcka`).
- **English:** notarial file numbers no longer break („NZ 384/2024,
  N 430/2024“ is one unbreakable unit; also N, Nz, Sd, Sdu, EZ, EVZ, U). The
  office profile reports dashes inside sentences (option `kontrola_pomlcka`).

## 0.4.0 – 2026-10-27

- **Česky:** nový modul `interpunkce` (volba profilu `interpunkce`).
  Opravuje: uvozovky psané jako dvě čárky („,,text“), mezery uvnitř kulatých
  závorek a před interpunkcí, zdvojenou tečku za zkratkou („apod..“),
  „cca.“, nelámání dvojtečky v poměru „2 : 3“. Hlásí: datum bez mezer,
  chybějící mezeru za čárkou, pomlčku bez mezery, rozsah čísel s mezerami
  („15 – 20“), „ -li“, spojovník s mezerami (ne v profilu kanceláře),
  „viz.“, „tzv. „…““, titul za jménem bez čárky, kumulaci interpunkce,
  znak minus a lomítko s mezerami. Pravidla podle IJP ÚJČ; seznam doplněn
  podle přehledu nejčastějších chyb v odborných textech. Ověřeno na 60
  skutečných textech: žádná nechtěná změna.
- **English:** new `interpunkce` module (profile option `interpunkce`). It
  fixes double-comma quotes, spaces inside parentheses and before
  punctuation, doubled full stops after abbreviations, „cca.“ and keeps
  ratios „2 : 3“ unbroken. It reports dates without spaces, missing spaces
  after commas, dash spacing, spaced numeric ranges, „ -li“, spaced hyphens
  (not in the office profile), „viz.“, „tzv. „…““, post-nominal titles
  without a comma, stacked punctuation, minus signs and spaced slashes.
  Checked on 60 real documents with no unwanted changes.

## 0.3.1 – 2026-10-27

- **Česky:** znak krát a trojtečka se už nepoužijí uvnitř doslovné citace
  („asi 2x pohnul“ zůstane), zjištěno při přesazbě skutečného podání.
- **English:** the multiplication sign and ellipsis rules no longer touch
  verbatim quotations („…“), found while re-typesetting a real filing.

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
