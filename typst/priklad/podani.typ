// Ukázkové podání se smyšlenými údaji / sample filing with made-up data.
//   python3 tools/priklad.py                       # tělo z telo.md přes cztypo
//   typst compile --root typst typst/priklad/podani.typ         # vzorová identita
//   typst compile --root typst --input identita=argumentum typst/priklad/podani.typ
//   (bez písem Office přidejte --input pisma=volna)

#import "../lib.typ": podani, adresat, participant, doc-title, part, prilohy, obhajce, sig-criminal
#import "../identity/vzor.typ": vzor

// identita argumentum se načte jen na požádání (jinak by typst hlásil
// chybějící písma Office i při sazbě vzoru)
#let id = if sys.inputs.at("identita", default: "vzor") == "argumentum" {
  import "../identity/argumentum.typ": arg
  arg
} else { vzor }

#show: podani.with(identity: id, doc-footer: "STÍŽNOST",
                   doc-title-meta: "Stížnost proti usnesení o zahájení trestního stíhání")

#adresat([Obvodní státní zastupitelství pro Prahu 1],
         [Náměstí Příkladné 1/1], [11000 Praha 1], [IDDS: abc0000])

#participant([Obviněný:], [Petr Novák, nar. 1. 1. 1990, Krátká 5, 14000 Praha 4])
#participant([Obhájce:], [#obhajce()])

#doc-title[Stížnost proti usnesení o zahájení trestního stíhání]

#prilohy([plná moc.])

#part([I.], caption: [Stížnost])

#include "telo.typ"

#sig-criminal(zaver: [V Praze dne 5. 9. 2026])
