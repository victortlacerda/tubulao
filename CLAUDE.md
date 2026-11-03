# Notas de trabalho: tubulao

App web estático (um único `index.html`) com a calculadora e o leitor da referência. Veja o `README.md` para o que ele faz.

## Como o `index.html` é organizado

Tudo está em um arquivo, em blocos `<script>` na ordem abaixo (cada módulo começa com um comentário `/* src/arquivo.js */`):

- `window.REFTEXT`: texto da referência por página (`toc`, `pages`, `refs`). É JSON em uma linha; o caractere `<` vai escapado como `\u003c`. Ao regravar, mantenha esse formato.
- `window.FIGPAGES`: páginas que têm figura (`f` = número do arquivo, `file`, `page` = página do texto, `figs` = número e legenda).
- `src/data.js` (tabelas), `src/core.js` (formatação, memória de cálculo, materiais), `src/eng_common.js` (áreas de barras e número de barras), `src/eng_tubulao.js` (fuste e base alargada), `src/registry.js` (páginas, campos de entrada e exemplos), `src/validation.js` (conferências) e a interface no último bloco.
- A numeração das equações segue o item do texto (`n: '16.1'` etc.). A base alargada é 16.3.

## Imagens da referência

`figs/pNNN.jpg`: NNN = página do PDF; página do texto = NNN − 4 (001 a 004 = capa e sumário, página 0). Salve em JPG, ~1241×1755 px, qualidade ~72, progressivo. O leitor lista só as páginas que existem em `REFTEXT.pages`.

## Ao mexer no código

- A página **Validação** tem de continuar toda conferida. Se mudar uma fórmula, confira o motivo antes de mexer nas tolerâncias.
- Rode `python3 tests/smoke.py` antes de cada commit (`CHROMIUM_PATH=/caminho/do/chromium` se precisar).
- Sem internet, KaTeX não carrega: as fórmulas aparecem em TeX cru, mas o texto dos resultados serve para comparar antes e depois de uma mudança.
- Mantenha a numeração dos itens igual à do texto de Bastos (2023).

## Commits

- Mensagens em português: título curto e, no corpo, o que mudou e por quê.
- Atualize o `CHANGELOG.md` no mesmo commit.
- Envie com `git push origin main`.

## Pontos de atenção

- O leitor lista só as páginas 55 a 59 e 66. As páginas 64, 65, 67 e 69 do PDF (resto da bibliografia e tabelas 1, 3 e 5) não entraram.
- A referência não traz exemplo resolvido de tubulão: a validação usa recálculo manual independente.
- O bloco de transição (16.4 e 16.5) vive no repositório `blocos-coroamento`.
