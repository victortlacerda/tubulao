#!/usr/bin/env python3
"""Gera os prints de docs/prints/ usados no README.

Uso (na raiz do repositório):
    mkdir -p /tmp/prints-npm && cd /tmp/prints-npm && npm init -y && \
      npm i katex@0.16.9 @fontsource/ibm-plex-sans @fontsource/ibm-plex-sans-condensed @fontsource/ibm-plex-mono
    cd <repositório> && PRINTS_NPM=/tmp/prints-npm/node_modules python3 tools/prints.py

Precisa de playwright e pillow (pip install playwright pillow). Use CHROMIUM_PATH se o
Chromium não estiver no caminho padrão. KaTeX e as fontes IBM Plex vêm do npm e substituem
os CDNs só durante a captura, então os prints saem iguais aos do app com internet.
"""
import io, os, pathlib, sys
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
NP = pathlib.Path(os.environ.get('PRINTS_NPM', '/tmp/prints-npm/node_modules'))
CHROMIUM = os.environ.get('CHROMIUM_PATH')  # None = Chromium do Playwright

# calc: página da 1ª e 2ª imagens; page: página do texto no leitor (texto limpo + figura);
# extra: (arquivo, página) de uma segunda calculadora
CFG = {
    'sapatas': dict(calc='iso-iguais', page=12, extra=('05-excentrica', 'excentrica')),
    'blocos-coroamento': dict(calc='quatro', page=13, extra=('05-transicao', 'transicao')),
    'tubulao': dict(calc='fuste', page=55, extra=('05-base-alargada', 'base')),
}[ROOT.name]

def fonts_css():
    out = []
    for fam, pkg in [('IBM Plex Sans', 'ibm-plex-sans'), ('IBM Plex Sans Condensed', 'ibm-plex-sans-condensed'), ('IBM Plex Mono', 'ibm-plex-mono')]:
        for w in (400, 500, 600):
            if (NP / '@fontsource' / pkg / 'files' / f'{pkg}-latin-{w}-normal.woff2').exists():
                out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(https://fonts.gstatic.com/local/{pkg}-{w}.woff2) format('woff2')}}")
    return '\n'.join(out)

def route(r):
    u = r.request.url
    if 'katex.min.js' in u:
        r.fulfill(body=(NP / 'katex/dist/katex.min.js').read_bytes(), content_type='application/javascript')
    elif 'fonts.googleapis.com' in u:
        r.fulfill(body=fonts_css(), content_type='text/css')
    elif 'fonts.gstatic.com/local/' in u:
        n = u.rsplit('/', 1)[1].split('.')[0]; pkg, w = n.rsplit('-', 1)
        r.fulfill(path=str(NP / '@fontsource' / pkg / 'files' / f'{pkg}-latin-{w}-normal.woff2'), content_type='font/woff2')
    elif u.startswith('file://'):
        r.continue_()
    else:
        r.abort()

def save(pg, path):
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
    im.save(path, 'JPEG', quality=86, optimize=True, progressive=True)
    print('ok', path.relative_to(ROOT))

def main():
    out = ROOT / 'docs' / 'prints'; out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(**({'executable_path': CHROMIUM} if CHROMIUM else {}))
        def page(h):
            ctx = br.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1.5)
            ctx.route('**/*', route); pg = ctx.new_page()
            pg.goto(f'file://{ROOT}/index.html#{h}'); pg.wait_for_timeout(1200); return pg
        pg = page(CFG['calc']); save(pg, out / '01-calculadora.jpg')
        pg.evaluate("()=>{const s=[...document.querySelectorAll('svg')].find(s=>s.getBoundingClientRect().width>400); if(s) s.scrollIntoView({block:'center'});}")
        pg.wait_for_timeout(500); save(pg, out / '02-esboco-memoria.jpg')
        pg = page('refbib'); n = CFG['page']
        pg.evaluate(f"()=>{{const i=document.querySelector('#refpg');i.value={n};i.dispatchEvent(new Event('change'));document.querySelector('#reader').scrollIntoView({{block:'start'}});}}")
        pg.wait_for_timeout(800); save(pg, out / '03-referencia.jpg')
        pg = page('valid'); pg.evaluate("[...document.querySelectorAll('details.vex')].slice(0,2).forEach(d=>d.open=true)")
        pg.wait_for_timeout(300); save(pg, out / '04-validacao.jpg')
        name, h = CFG['extra']; pg = page(h); save(pg, out / f'{name}.jpg')

if __name__ == '__main__':
    main()
