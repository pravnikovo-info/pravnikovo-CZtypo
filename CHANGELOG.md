# Změny

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
