// Vzorová identita: smyšlená advokátní kancelář. Všechny údaje jsou vymyšlené.
// Sample identity: a fictional law firm. All data are made up.
//
// Písmo Libertinus Serif je v typstu vestavěné, vzor se tedy vysází bez
// instalace písem. Vlastní identitu založíte kopií tohoto souboru.
// Libertinus Serif ships with typst, so the sample compiles without installing
// fonts. Create your own identity by copying this file.

#let vzor-barva = rgb("#1F4E79")
#let vzor-seda = rgb("#6E6E6E")
#let vzor-pismo = ("Libertinus Serif",)

#let vzor-hlavicka = block(width: 11cm)[
  #set text(top-edge: "ascender", bottom-edge: "descender", font: vzor-pismo)
  #set par(leading: 0pt, spacing: 0pt, justify: false)
  #text(size: 22pt, weight: "bold", fill: vzor-barva)[Vzorová advokátní kancelář]
  #v(3pt)
  #text(size: 9pt, fill: vzor-seda)[
    Příkladná 1/2, 11000 Praha 1 \
    +420 000 000 000, kancelar\@example.cz
  ]
  #v(6pt)
  #text(size: 9pt, fill: vzor-seda)[
    Mgr. Jan Vzorový, advokát \
    ČAK 00000, IČO 00000000, IDDS: abc1234
  ]
]

#let vzor = (
  klic: "vzor",
  advokat: "Mgr. Jan Vzorový, advokát",
  author: "Mgr. Jan Vzorový, advokát, ev. č. ČAK 00000",
  // řádky pro #participant[Obhájce:][#obhajce()]
  obhajce: (
    "Mgr. Jan Vzorový, advokát",
    "ev. č. ČAK 00000, Příkladná 1/2, 11000 Praha 1",
    "IDDS: abc1234",
  ),
  // řádek zástupce: #zastupce(); jméno v 7. pádě, zapsané ručně
  zastupce: (navesti: "práv. zast.:", radky: (
    [*Mgr. Janem Vzorovým, advokátem*],
    "ev. č. ČAK 00000, Příkladná 1/2, 11000 Praha 1",
    "IDDS: abc1234",
  )),
  podpis: (za: "za obviněného",
           jmeno: "Mgr. Jan Vzorový, advokát, obhájce",
           vpravo: false),
  pismo: (font: vzor-pismo, size: 11pt, leading: 0.29em, spacing: 9.2pt,
          tucne-tah: none),
  nadpis: (size: 12pt, above: 15.2pt, below: 9.2pt),
  titul: (size: 14pt, align: center, leading: 0.29em,
          above: 8pt, linka: true, pod: 7pt, za: 7pt),
  ident: (inset: 10cm, below: 10pt),
  ucastnik: (columns: (2.6cm, 0.2cm, 14.4cm), below: 6pt, label-weight: "bold"),
  telo-nova-strana: false,
  linka: vzor-seda,
  margin: (left: 1.8cm, right: 1.8cm, top: 2.9cm, bottom: 1.5cm),
  prvni-odskok: 0.9cm,
  footer-descent: 0.6cm,
  pozadi: n => if n == 1 { place(top + left, dx: 1cm, dy: 1cm, vzor-hlavicka) },
  paticka: (n, nazev) => {
    let num = if n < 10 { "0" + str(n) } else { str(n) }
    set text(font: vzor-pismo, size: 10pt, fill: vzor-seda)
    place(dx: -0.78cm, box(height: 0.45cm, align(horizon)[#num]))
    place(dx: -0.05cm, line(start: (0pt, 0pt), end: (0pt, 0.45cm),
                            stroke: 0.4pt + vzor-seda))
    place(dx: 0.28cm, box(height: 0.45cm,
      align(horizon)[Vzorová AK - #nazev]))
  },
)
