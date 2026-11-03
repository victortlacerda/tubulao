#!/usr/bin/env python3
"""Teste de fumaça do app (index.html).

Confere, sem editar nada:
  1. cada item do menu abre sem erro de JavaScript e mostra conteúdo;
  2. a página Validação está toda conferida (alerta verde);
  3. o leitor da referência percorre todas as páginas e cada imagem de figs/ carrega.

Uso:
  pip install playwright && playwright install chromium
  python3 tests/smoke.py

Se o Chromium estiver em outro lugar, informe com CHROMIUM_PATH=/caminho/do/chromium.
A internet só é necessária para KaTeX e fontes; falhas dessas requisições são ignoradas.
"""
import os
import pathlib
import sys

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
URL = (RAIZ / "index.html").as_uri()


def main():
    falhas = []
    erros_js = []
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        pg = nav.new_page(viewport={"width": 1280, "height": 900})
        pg.on("pageerror", lambda e: erros_js.append(str(e)))

        pg.goto(URL)
        pg.wait_for_selector("#nav .ni")
        destinos = pg.eval_on_selector_all("#nav .ni", "els => els.map(e => [e.getAttribute('href'), e.innerText.replace(/\\n/g, ' ')])")

        # 1) cada item do menu
        for href, nome in destinos:
            pg.goto(URL + href)
            pg.reload()
            pg.wait_for_timeout(400)
            texto = pg.inner_text("#main")
            ok = len(texto.strip()) > 100
            print(("ok   " if ok else "FALHA"), "menu:", nome)
            if not ok:
                falhas.append("página vazia: " + nome)
            if href == "#valid":
                if not pg.query_selector(".alert-ok"):
                    falhas.append("Validação com resultados que não conferem: " + pg.inner_text(".alert"))
                print("      ", pg.inner_text(".alert").replace("\n", " "))

        # 2) leitor da referência: todas as páginas e imagens
        pg.goto(URL + "#refbib")
        pg.reload()
        pg.wait_for_selector("#refpg")
        pg.fill("#refpg", pg.get_attribute("#refpg", "min"))
        pg.dispatch_event("#refpg", "change")
        vistas = []
        while True:
            atual = pg.input_value("#refpg")
            if atual in vistas:
                break
            vistas.append(atual)
            pg.wait_for_timeout(80)
            for src, carregou in pg.eval_on_selector_all(
                ".refimg img", "els => els.map(i => { i.scrollIntoView(); return [i.getAttribute('src'), i.complete && i.naturalWidth > 0]; })"
            ):
                if not carregou:
                    pg.wait_for_timeout(400)
                    carregou = pg.evaluate("s => { const i = document.querySelector('.refimg img[src=\"' + s + '\"]'); return !!i && i.complete && i.naturalWidth > 0; }", src)
                if not carregou:
                    falhas.append(f"imagem não carrega na página {atual}: {src}")
            pg.click("text=Próxima ›")
        print(f"ok    leitor: {len(vistas)} páginas percorridas")
        nav.close()

    for e in erros_js:
        falhas.append("erro de JavaScript: " + e)
    if falhas:
        print("\nFALHAS:")
        for f in falhas:
            print(" -", f)
        sys.exit(1)
    print("\nTudo certo.")


if __name__ == "__main__":
    main()
