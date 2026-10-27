// pravnikovo-CZtypo: typst šablona podání / typst template for legal filings
//
// Tři vrstvy: identita × typ dokumentu × obsah. Identita (hlavička, patička,
// písmo, okraje, podpis) je PARAMETR, nikoli kopie šablony. Identity jsou
// v identity/*.typ, sazečská pravidla jsou společná a jsou zde.
// Three layers: identity × document type × content. The identity (letterhead,
// footer, font, margins, signature) is a PARAMETER, not a copy of the template.
//
//   #import "lib.typ": podani, adresat, participant, doc-title, part, sig-criminal
//   #import "identity/vzor.typ": vzor
//   #show: podani.with(identity: vzor, doc-footer: "ŽÁDOST")
//
// Kompilace / compile:  typst compile --root typst typst/priklad/podani.typ
// Vzorová identita používá písmo vestavěné v typstu; identita argumentum
// použije Cambrii a Garamond, jsou-li nainstalované, jinak volné náhrady
// Caladea a EB Garamond (viz README).

#import "identity/vzor.typ": vzor

// Identita platná v dokumentu. podani ji nastaví, pomocné prvky ji čtou.
// Výchozí je vzor, aby prvky fungovaly i mimo podani.
#let identita = state("cztypo-identita", vzor)
// Zda už začalo tělo podání, tedy první číslovaný oddíl.
#let _telo-zacalo = state("cztypo-telo-zacalo", false)

// Tučné písmo. Kde font nemá tučný řez (Century), nahrazuje ho tah obrysu,
// stejně jako umělé ztučnění ve Wordu. Typst sám tučný řez nesyntetizuje.
#let _tucne(id, body) = {
  let tah = id.pismo.at("tucne-tah", default: none)
  if tah == none {
    text(weight: "bold")[#body]
  } else {
    context text(weight: "bold", stroke: tah + text.fill)[#body]
  }
}

// Blok odsazený zleva (adresní bloky a podpisy), odsazení určuje identita
#let argident(body) = context {
  let id = identita.get()
  block(inset: (left: id.ident.inset), above: 0pt, below: id.ident.below)[
    #set par(justify: false)
    #body
  ]
}

// Adresát v adresním bloku: název orgánu tučně na prvním řádku, pod ním
// adresa, IDDS a případně e-mail. `pred` je doplňující určení nad názvem
// („na vědomí:“, „prostřednictvím“), které stojí u svého orgánu jako
// samostatný blok se stejným rozestupem shora i zdola. Po „prostřednictvím“
// se název orgánu skloňuje (genitiv).
//   #adresat([Okresní soud ve Znojmě], [náměstí Republiky 585/1], [67008 Znojmo], [IDDS: f4dabgy])
//   #adresat(pred: [na vědomí:], [Česká republika - Státní pozemkový úřad], ...)
//   #adresat(pred: [prostřednictvím], [Obvodního státního zastupitelství pro Prahu 5], ...)
#let adresat(nazev, pred: none, ..radky) = context {
  let id = identita.get()
  if pred != none { argident[#pred] }
  argident[
    #_tucne(id, nazev)
    #for r in radky.pos() [ \ #r]
  ]
}

// Dvousloupcový identifikační blok: návěští + mezera + hodnota
#let participant(label, value) = context {
  let id = identita.get()
  let u = id.ucastnik
  block(above: 0pt, below: u.below, width: 100%)[
    #grid(
      columns: u.columns,
      align: (top + left, top + left, top + left),
      if u.label-weight == "bold" { _tucne(id, label) } else [#label], [],
      block[#set par(justify: false); #value],
    )
  ]
}

// Hlavní nadpis podání; zarovnání a linku pod ním určuje identita.
#let doc-title(body) = context {
  let id = identita.get()
  let t = id.titul
  v(t.above)
  block(width: 100%)[
    #set par(justify: false, leading: t.leading)
    #align(t.align, _tucne(id, text(size: t.size)[#body]))
  ]
  if t.linka {
    v(t.pod)
    line(length: 100%, stroke: 0.4pt + id.linka)
  }
  v(t.za)
}

// Přílohy patří na PRVNÍ stranu pod název a řádek o podání datovou schránkou,
// nikdy na konec za podpis. Volat před prvním #part;
// zavolá-li se až v těle, překlad skončí chybou, aby to nešlo přehlédnout.
// Řádky začínají odrážkou, ne číslem. Položky končí
// středníkem, poslední tečkou. Označení „(P01)“ na konci položky jen při
// více než 5 přílohách; do 5 příloh se nečíslují vůbec.
#let prilohy(..polozky) = {
  context {
    if _telo-zacalo.get() {
      panic("prilohy() až za tělem podání: přílohy patří na první stranu před první #part")
    }
  }
  block(above: 14pt, width: 100%)[
    PŘÍLOHY:
    #list(marker: [–], ..polozky.pos())
  ]
}

// Číslovaná část. Mezery jsou dopočítané: hrany ascender/descender zabírají
// zhruba jeden stupeň písma, takže above 15,2 pt dá nad číslem 12 pt navíc
// nad řádkový proklad a below 9,2 pt dá pod nadpisem 6 pt navíc.
// sticky drží nadpis u následujícího bloku, takže nikdy nezůstane sám
// na konci stránky. Typst nemá penalty jako LaTeX, tohle je jeho náhrada.
#let part(num, caption: none) = {
  // Identity, jejichž tělo začíná až na druhé stránce: první
  // oddíl zlomí stránku. weak: na začátku stránky se nic nevloží.
  context {
    if (identita.get().at("telo-nova-strana", default: false)
        and not _telo-zacalo.get()) { pagebreak(weak: true) }
  }
  _telo-zacalo.update(true)
  context {
  let id = identita.get()
  let n = id.nadpis
  // Nepovinné vlastnosti identity: zarovnání nadpisu a to, zda se sází
  // číslice. Např. nadpisy tučně vlevo bez číslování (cisla: false,
  // align: left); bez nich zůstává číslice i popisek na středu.
  let al = n.at("align", default: center)
  block(above: n.above, below: n.below, width: 100%, sticky: true)[
    #set par(justify: false, leading: 0.29em, spacing: 0pt)
    #if n.at("cisla", default: true) {
      align(al, _tucne(id, text(size: n.size)[#num]))
    }
    #if caption != none and n.at("popisky", default: true) {
      align(al, _tucne(id, text(size: n.size)[#caption]))
    }
  ]
  }
}

// Vložený nadpis na jednom řádku (prohlášení, souhlasy). Římská číslice
// se k textu lepí nezlomitelnou mezerou, aby nikdy nezůstala sama.
#let part-inline(body) = context {
  let id = identita.get()
  let n = id.nadpis
  block(above: n.above, below: n.below, width: 100%, sticky: true)[
    #set par(justify: false, leading: 0.29em, spacing: 0pt)
    #_tucne(id, text(size: n.size)[#body])
  ]
}

// Navrhovaný výrok nebo petit s římsky číslovanými body. Každý bod začíná
// na novém řádku s vyvěšenou číslicí. Slitá hromada je nečitelná a orgán,
// který má podle návrhu rozhodnout, si z ní výrok nevypreparuje.
#let vyrok(..body) = context {
  let id = identita.get()
  let posledni = body.pos().len() - 1
  for (i, (cislo, telo)) in body.pos().enumerate() {
    block(above: 6pt, below: if i == posledni { 12pt } else { 0pt },
          width: 100%)[
      #grid(
        columns: (1.25cm, 1fr),
        gutter: 0pt,
        align: (top + left, top + left),
        _tucne(id, cislo),
        block[#telo],
      )
    ]
  }
}

#let podani(
  identity: vzor,
  doc-footer: "",
  doc-title-meta: none,
  author: auto,
  show-footer: true,
  bare: false,
  body,
) = {
  let id = identity
  let show-footer = if bare { false } else { show-footer }
  identita.update(if bare { id + (telo-nova-strana: false) } else { id })

  // Vlastnosti dokumentu. Bez nich se PDF v prohlížeči i ve spisové službě
  // jmenuje podle souboru a nemá autora.
  set document(
    title: if doc-title-meta != none { doc-title-meta } else { doc-footer },
    author: if author == auto { id.author } else { author },
  )

  // Hlavička, patička a logo patří identitě. Co je jen na první stránce
  // (hlavičkový papír), kreslí identita do pozadí absolutně.
  set page(
    paper: "a4",
    margin: id.margin,
    header: none,
    footer: if show-footer and id.paticka != none {
      context {
        let n = counter(page).at(here()).first()
        (id.paticka)(n, doc-footer)
      }
    } else { none },
    footer-descent: id.footer-descent,
    background: context {
      let n = counter(page).at(here()).first()
      if not bare and id.pozadi != none { (id.pozadi)(n) }
    },
  )

  // slova nedělíme
  // ascender/descender hrany: typst jinak měří mezery od cap-height a účaří,
  // takže nominálních 6 pt dá vizuálně jen ~3 pt. S těmito hranami znamená
  // mezera MEZI odstavci navíc 6 pt nad řádkový proklad. V typstu spacing
  // proklad NAHRAZUJE, nepřičítá se, takže spacing = leading + 6 pt.
  // ccmp vypnuto ZÁMĚRNĚ a pro všechny identity. Cambria regular tímto
  // pravidlem rozkládá akcentované glyfy na základ a akcent, typst akcent
  // zapíše jako samostatný glyf a každý extraktor tam vidí mezeru. Kopírovaný
  // text pak zní „neuvá dí zá koníku". Vypnutím se použije předskládaný glyf.
  set text(font: id.pismo.font, size: id.pismo.size, lang: "cs",
           hyphenate: false,
           top-edge: "ascender", bottom-edge: "descender",
           features: (ccmp: 0))
  set par(justify: true, spacing: id.pismo.spacing, leading: id.pismo.leading)

  show heading: it => block(above: id.nadpis.above, below: id.nadpis.below,
                            width: 100%)[
    #set par(justify: false, leading: 0.29em, spacing: 0pt)
    #align(center, _tucne(id, text(size: id.nadpis.size)[#it.body]))
  ]
  // *tučně* v markupu musí u fontu bez tučného řezu dostat náhradu také
  show: rest => if id.pismo.at("tucne-tah", default: none) == none { rest } else {
    show strong: it => _tucne(id, it.body)
    rest
  }

  show quote.where(block: true): it => block(inset: (left: 1.27cm), emph(it.body))
  // Odrážky začínají na úrovni textu, bez odsazení.
  set list(marker: [--], indent: 0pt, spacing: 6pt)
  set enum(indent: 0pt, spacing: 6pt)

  // Místo pro patičku, kterou má jen první stránka. Plovoucí blok
  // u spodní hrany odsune tělo jen na první stránce, další mají okraj celý.
  if not bare and id.at("rezerva-prvni", default: none) != none {
    context place(bottom, float: true, clearance: 0pt,
                  block(height: (id.rezerva-prvni)()))
  }
  if not bare { v(id.prvni-odskok) }
  body
}

// Kratší zápisy / aliases
#let doc = podani
#let arg-doc = podani

// --- Podpisové a pomocné prvky ---

// Řádky obhájce pro #participant[Obhájce:][#obhajce()] podle identity.
// Údaje advokáta tak mají jediné místo pravdy, identity/<klic>.typ.
#let obhajce() = context identita.get().obhajce.join([ \ ])

// Celý řádek zástupce: „práv. zast.:" a advokát v 7. pádě. Tvar je zapsaný
// jednou v identitě a zkontrolovaný; za běhu se nic neskloňuje.
#let zastupce() = context {
  let z = identita.get().zastupce
  participant(z.navesti, z.radky.join([ \ ]))
}

// Substituce (ex offo za kolegu): „práv. zast.:" = ustanovený obhájce
// v 7. pádě s opatřením soudu a jeho údaji, „subst. zast.:" = advokát identity
// v 7. pádě. Ne návěští „Obhájkyně:" ani „v substituci:".
//   #zastupce-subst([*JUDr. Janou Příkladnou, advokátkou*, obhájkyní
//     ustanovenou opatřením ... \ ev. č. ČAK 00000, ... \ IDDS: abcd123])
#let zastupce-subst(ustanoveny) = context {
  let z = identita.get().zastupce
  participant(z.navesti, ustanoveny)
  participant("subst. zast.:", z.radky.join([ \ ]))
}

// Místo pro ruční doplnění: prostá mezera, nikoli řada teček.
#let fillspace(w) = h(w)

// Místo k ručnímu vyplnění perem (jen ve vzorech a formulářích, nikdy
// v dokumentu k expedici): linka na účaří a nad ní volná výška pro rukopis.
// Ruční písmo je výrazně větší než strojové: výchozí výška 1,3 cm, šířka
// nejméně 4 cm pro datum, 8 cm pro jméno, celá šířka pro adresu.
//   nar. #rucne(4cm), bytem #rucne(9cm)
#let rucne(w, vyska: 1.3cm) = box(width: w, height: vyska,
  align(bottom, line(length: w, stroke: 0.5pt)))

// Podpis nesmí stát sám na stránce. Typst neumí „držet s předchozím“, proto
// se poslední odstavec textu předává podpisu jako `zaver` a sází se s ním
// v jednom nedělitelném bloku: buď zůstane celek na stránce, nebo přejde
// celý (odstavec i podpis) na další. Bez `zaver` se jen ověří, že se podpis
// za předchozí text ještě vejde; jinak překlad skončí chybou s pokynem.
#let podpis-blok(zaver, podpis, mezera) = {
  if zaver != none {
    // width: 100 %, jinak se odstavec `zaver` uvnitř bloku nesází do bloku
    // (blok bez šířky měří odstavec na přirozenou šířku)
    block(breakable: false, width: 100%)[#zaver #v(mezera) #podpis]
  } else {
    // značka na konci předchozího textu; podpis musí skončit na téže stránce
    // značka v bloku nulové výšky: samotný tag by typst přenesl na novou
    // stránku spolu s podpisem, blok zůstane tam, kde skončil text
    block(height: 0pt, above: 0pt, below: 0pt)[#metadata("podpis-pred")<cztypo-podpis-pred>]
    v(mezera)
    podpis
    context {
      let pred = query(selector(<cztypo-podpis-pred>).before(here())).last()
      assert(pred.location().page() == here().page(),
        message: "Podpis by byl sám na stránce. Předej poslední odstavec textu "
          + "podpisu: #sig-criminal(zaver: [poslední odstavec]).")
    }
  }
}

// Podpis v trestních věcech (pevná formule podle identity). Datum patří do
// adresního bloku za č. j., ne na konec textu. `zaver` je poslední odstavec
// textu, se kterým podpis drží na stránce (viz podpis-blok).
#let sig-criminal(for-whom: auto, name: auto, zaver: none) = context {
  let id = identita.get()
  let za = if for-whom == auto { id.podpis.za } else { for-whom }
  let jmeno = if name == auto { id.podpis.jmeno } else { name }
  let podpis = if id.podpis.vpravo {
    align(right)[
      #set par(justify: false)
      #if za != none [#za \ ]
      #jmeno
    ]
  } else {
    argident[
      #set par(justify: false)
      #if za != none [#za \ ]
      #jmeno
    ]
  }
  podpis-blok(zaver, podpis, 16mm)
}

// Podpis u prohlášení třetích osob: vpravo, nad jménem volné místo na podpis
#let sig-line(name: "", zaver: none) = podpis-blok(zaver, argident[
    #set par(justify: false)
    #name
  ], 18mm)

// Podpis s identifikačními a kontaktními údaji. Do záhlaví prohlášení patří
// jen to, čeho se věc týká; kdo prohlášení činí, je zřejmé z podpisu, a tam
// tedy patří i datum narození, telefon a adresa, každý na vlastním řádku.
#let sig-detail(name: "", lines: (), zaver: none) = podpis-blok(zaver, argident[
    #set par(justify: false, leading: 0.29em, spacing: 0pt)
    #name \
    #lines.join([ \ ])
  ], 18mm)

// Strojové písmo pro odkazy, hesla a identifikátory: neproporcionální
// bezpatkové, DejaVu Sans Mono je v typstu vestavěné. `kod` sází jeden
// nezalomitelný řetězec tak, aby šel z PDF zkopírovat beze změny.
#let kodfont = (font: "DejaVu Sans Mono", size: 9.5pt)
#let kod(s) = box({ show raw: set text(..kodfont); raw(s) })

// Rámeček pro důvěrné údaje (přístupové údaje k úložišti apod.): tenký rám,
// návěští DŮVĚRNÉ vpravo nahoře, celý obsah včetně návěští strojovým písmem,
// pohromadě na jedné stránce.
#let duverne(body, navesti: "DŮVĚRNÉ") = block(width: 100%, breakable: false,
  stroke: 0.5pt + black, inset: (x: 10pt, top: 8pt, bottom: 10pt))[
  #set text(..kodfont)
  #show raw: set text(..kodfont)
  #set par(justify: false, leading: 0.5em)
  #place(top + right, dy: -1pt, text(size: 8pt, weight: "bold")[#navesti])
  #body
]

// --- Redline: vyznačení změn a komentáře ---

#let delcolor = rgb("#B00000")
#let inscolor = rgb("#0B4C8C")

// Vypuštěný text
#let del(body) = text(fill: delcolor)[#strike(body)]

// Vložený text
#let ins(body) = text(fill: inscolor)[#underline(body)]

// Značka odkazující na komentář
#let cmt(n) = super(text(fill: inscolor, weight: "bold", size: 9pt)[[#n]])

// Seznam komentářů k úpravám na konci redline
#let komentare(items) = context {
  let id = identita.get()
  v(16pt)
  line(length: 100%, stroke: 0.4pt + id.linka)
  v(8pt)
  align(center, _tucne(id, text(size: id.nadpis.size)[Komentáře k úpravám]))
  v(8pt)
  for (i, it) in items.enumerate() {
    block(above: 6pt, below: 0pt, width: 100%)[
      #grid(
        columns: (1.25cm, 1fr),
        align: (top + left, top + left),
        text(fill: inscolor, weight: "bold")[[#{i + 1}]],
        it,
      )
    ]
  }
}

// Legenda redline
#let redline-legenda = block(above: 0pt, below: 10pt, width: 100%)[
  #set text(size: 10pt)
  #del[vypuštěný text] #h(0.6cm) #ins[vložený text] #h(0.6cm)
  #cmt[n] #text(fill: inscolor)[odkaz na komentář na konci dokumentu]
]
