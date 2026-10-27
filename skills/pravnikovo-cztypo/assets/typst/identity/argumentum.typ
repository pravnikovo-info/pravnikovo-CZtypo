// Identita AK argumentum.cz (Mgr. Jiří Slováček, Ph.D.): skutečná kancelář,
// ze které šablona vznikla. Slouží jako příklad identity s vlastním
// hlavičkovým papírem; pro vlastní kancelář použijte identity/vzor.typ.
// Identity of the law firm argumentum.cz, where the template originated.
// Use identity/vzor.typ as the starting point for your own firm.
//
// Hlavička je sazena podle hlavičkového papíru ve Wordu, ne podle dojmu:
//   "argumentum.cz"  Garamond 24 pt bold, CC0000
//   ostatní řádky    Cambria 9 pt, 808080
// Garamond a Cambria jsou komerční písma Microsoftu (jsou součástí Office)
// a nejsou přibalena. Bez nich se použijí volné náhrady EB Garamond
// a Caladea (stejné rozměry jako Cambria), případně vestavěný Libertinus.

#let argred = rgb("#CC0000")
#let argaddrgray = rgb("#808080")
#let argfootgray = rgb("#7F7F7F")
// Písma: výchozí jsou Cambria a Garamond (Microsoft Office). Bez nich
// přepněte na volné náhrady: typst compile --input pisma=volna ...
// Fonts: Cambria and Garamond by default; use --input pisma=volna for the free
// replacements Caladea and EB Garamond. Libertinus Serif is the last resort.
#let arg-volna = sys.inputs.at("pisma", default: "ms") == "volna"
#let arg-cambria = if arg-volna { ("Caladea", "Libertinus Serif") } else { ("Cambria", "Libertinus Serif") }
#let arg-garamond = if arg-volna { ("EB Garamond", "Libertinus Serif") } else { ("Garamond", "Libertinus Serif") }

#let arg-logo-block = block(width: 11cm)[
  // typst má default bottom-edge "baseline" -> dolní dotažnice přetékají
  // a řádky různých velikostí se překrývají; proto ascender/descender
  #set text(top-edge: "ascender", bottom-edge: "descender")
  #set par(leading: 0pt, spacing: 0pt, justify: false)
  #text(font: arg-garamond, size: 24pt, weight: "bold", fill: argred)[argumentum.cz]
  #v(2pt)
  #text(font: arg-cambria, size: 9pt, fill: argaddrgray)[
    Vodičkova 704/36, 11000 Praha 1 \
    +420 580 000 000, office\@argumentum.cz
  ]
  #v(6pt)
  #text(font: arg-cambria, size: 9pt, fill: argaddrgray)[
    Mgr. Jiří Slováček, Ph.D., advokát \
    ČAK 13596, IČO 70267561, IDDS: v93xu4d
  ]
]

#let arg = (
  klic: "arg",
  advokat: "Mgr. Jiří Slováček, Ph.D., advokát",
  author: "Mgr. Jiří Slováček, Ph.D., advokát, ev. č. ČAK 13596",
  // řádky pro participant[Obhájce:] v podání
  obhajce: (
    "Mgr. Jiří Slováček, Ph.D., advokát",
    "ev. č. ČAK 13596, Vodičkova 704/36, 11000 Praha 1",
    "IDDS: v93xu4d",
  ),
  // řádek zástupce v podání: #zastupce(); jméno v 7. pádě, zkontrolováno
  zastupce: (navesti: "práv. zast.:", radky: (
    [*Mgr. Jiřím Slováčkem, Ph.D., advokátem*],
    "ev. č. ČAK 13596, Vodičkova 704/36, 11000 Praha 1",
    "IDDS: v93xu4d",
  )),
  podpis: (za: "za obviněného",
           jmeno: "Mgr. Jiří Slováček, Ph.D., advokát, obhájce",
           vpravo: false),
  // Naměřeno: řádek 14,2 pt, odstavec 20,2 pt = shoda s hlavičkovým papírem.
  pismo: (font: arg-cambria, size: 11pt, leading: 0.29em, spacing: 9.2pt,
          tucne-tah: none),
  nadpis: (size: 12pt, above: 15.2pt, below: 9.2pt),
  titul: (size: 14pt, align: center, leading: 0.29em,
          above: 8pt, linka: true, pod: 7pt, za: 7pt),
  ident: (inset: 10cm, below: 10pt),
  ucastnik: (columns: (2.6cm, 0.2cm, 14.4cm), below: 6pt, label-weight: "bold"),
  // Tělo podání začíná až na druhé stránce: první `part` zlomí stránku.
  // První stránka nese adresní blok, účastníky, název a řádek o podání
  // datovou schránkou.
  telo-nova-strana: true,
  linka: argaddrgray,
  margin: (left: 1.8cm, right: 1.8cm, top: 2.9cm, bottom: 1.5cm),
  prvni-odskok: 0.9cm,
  footer-descent: 0.6cm,
  pozadi: n => if n == 1 { place(top + left, dx: 1cm, dy: 1cm, arg-logo-block) },
  // Patička „NN | AK argumentum.cz - NÁZEV". Číslo stránky i text vertikálně
  // na střed svislé linky; linka 0,4 pt jako horizontála pod nadpisem.
  paticka: (n, nazev) => {
    let num = if n < 10 { "0" + str(n) } else { str(n) }
    set text(font: arg-cambria, size: 11pt, fill: argfootgray)
    place(dx: -0.78cm, box(height: 0.45cm, align(horizon)[#num]))
    place(dx: -0.05cm, line(start: (0pt, 0pt), end: (0pt, 0.45cm),
                            stroke: 0.4pt + argfootgray))
    place(dx: 0.28cm, box(height: 0.45cm,
      align(horizon)[AK argumentum.cz - #nazev]))
  },
)

// Společné podání více advokátů (např. dva obhájci): hlavička bez spodní části
// se jménem advokáta, zůstává logo, adresa a kontakt kanceláře.
#let arg-logo-block-spolecne = block(width: 11cm)[
  #set text(top-edge: "ascender", bottom-edge: "descender")
  #set par(leading: 0pt, spacing: 0pt, justify: false)
  #text(font: arg-garamond, size: 24pt, weight: "bold", fill: argred)[argumentum.cz]
  #v(2pt)
  #text(font: arg-cambria, size: 9pt, fill: argaddrgray)[
    Vodičkova 704/36, 11000 Praha 1 \
    +420 580 000 000, office\@argumentum.cz
  ]
]

#let arg-spolecne = arg + (
  klic: "arg-spolecne",
  pozadi: n => if n == 1 { place(top + left, dx: 1cm, dy: 1cm, arg-logo-block-spolecne) },
)
