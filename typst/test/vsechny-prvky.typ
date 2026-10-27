// Kouřový test: všechny prvky šablony v jednom dokumentu (CI ho sází).
#import "../lib.typ": podani, adresat, participant, obhajce, zastupce, zastupce-subst, doc-title, prilohy, part, part-inline, vyrok, sig-criminal, sig-line, sig-detail, fillspace, rucne, kod, duverne, del, ins, cmt, komentare, redline-legenda
#import "../identity/vzor.typ": vzor
#show: podani.with(identity: vzor, doc-footer: "TEST", doc-title-meta: "Test prvků")

#redline-legenda
#adresat(pred: [na vědomí:], [Obvodní soud pro Prahu 1], [Příkladná 1], [11000 Praha 1], [ke sp. zn. #box[1 T 24/2026]])
#participant([Obviněný:], [Petr Novák])
#participant([Obhájce:], [#obhajce()])
#zastupce()
#zastupce-subst([*JUDr. Janou Příkladnou, advokátkou*])
#doc-title[Test všech prvků]
#prilohy([plná moc;], [usnesení.])
#part([I.], caption: [Oddíl])
Text s #del[vypuštěným] #ins[vloženým] textem #cmt(1). Místo #fillspace(2cm) a #rucne(4cm). #kod("a1b2")
#part-inline[II. Vložený nadpis]
#vyrok(([I.], [První bod.]), ([II.], [Druhý bod.]))
#duverne[heslo: x]
#komentare(([důvod změny],))
#sig-criminal(zaver: [Poslední odstavec.])
#sig-line(name: [Jan Svědek])
#sig-detail(name: [Jana Svědková], lines: ([nar. 1. 1. 1990],))
