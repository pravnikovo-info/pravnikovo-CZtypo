import shutil
import subprocess

import pytest

from cstypo import LADENI, NBSP, do_typstu, uprav
from cstypo.cli import main


def test_cli_uprav(tmp_path, capsys):
    f = tmp_path / "a.txt"
    f.write_text("jel s kolegou", encoding="utf-8")
    assert main([str(f)]) == 0
    assert capsys.readouterr().out == f"jel s{NBSP}kolegou"


def test_cli_check(tmp_path, capsys):
    f = tmp_path / "a.txt"
    f.write_text("jel s kolegou", encoding="utf-8")
    assert main(["--check", str(f)]) == 1
    assert "jednoznaková předložka" in capsys.readouterr().out


def test_cli_typst_ladit(tmp_path, capsys):
    f = tmp_path / "a.txt"
    f.write_text("sp. zn. 4 Tdo 123/2025", encoding="utf-8")
    assert main(["--typst", "--ladit", "--profil", "kancelar", str(f)]) == 0
    out = capsys.readouterr().out
    assert out.startswith(LADENI)
    assert "#box[4 Tdo 123/2025]" in out


def test_cli_chybejici_soubor(capsys):
    assert main(["/neexistuje/soubor.txt"]) == 2


def test_cli_ladit_bez_typst():
    with pytest.raises(SystemExit):
        main(["--ladit"])


@pytest.mark.skipif(shutil.which("typst") is None, reason="typst chybí")
def test_vystup_se_zkompiluje(tmp_path):
    text = ("Obviněný jel s poškozenou dne 28. 7. 2026 do banky v Písku, kde "
            "podle § 234 odst. 4 písm. a) vybral 1 234 567 Kč. Je-li to možné, "
            "soud věc projedná pod sp. zn. 12 Nt 345/2026; č. j. "
            "ABCD-12345-67/TČ-2026-000089 (viz výše), nález I. ÚS 1234/25. "
            "Za VZOREK s.r.o. jedná Mgr. Jan Dvořák, Ph.D., tel. 777 000 000, "
            "e-mail info@example.com, v letech 1948–1989, „de facto“ ........\n"
            "18. října 2026 podle o. s. ř. a zákona č. 89/2012 Sb.")
    from cstypo import KANCELAR, UJC
    for i, p in enumerate((UJC, KANCELAR)):
        src = tmp_path / f"t{i}.typ"
        src.write_text('#set text(lang: "cs")\n' + LADENI
                       + do_typstu(uprav(text, p)), encoding="utf-8")
        r = subprocess.run(["typst", "compile", str(src)],
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
