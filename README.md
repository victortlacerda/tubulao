# Tubulão a céu aberto

Calculadora e referência de **tubulão a céu aberto** (fuste e base alargada), em um único arquivo `index.html`, baseada no item 16 das notas de aula *Blocos de Fundação* do Prof. Dr. Paulo Sérgio dos Santos Bastos (UNESP – Bauru/SP).

Cada calculadora gera uma memória de cálculo passo a passo, com as equações do texto, esboço, exemplos e verificações.

## Como usar

Abra o `index.html` no navegador. Não precisa instalar nada nem subir servidor.

As equações usam KaTeX e as fontes vêm do Google Fonts, carregados da internet: sem conexão o cálculo funciona, mas as fórmulas aparecem como texto TeX.

Para publicar como site, ative o GitHub Pages em *Settings → Pages* (branch `main`, pasta `/ (root)`). Os caminhos de `figs/` são relativos e funcionam sem ajuste.

## O que o app tem

| Item do texto | Página do app |
|---|---|
| 16.1 a 16.3 | Fuste e armaduras: diâmetro do fuste de concreto simples, armadura longitudinal e estribos |
| 16.3 | Base alargada: base circular ou falsa elipse, β = 60°, hb ≤ 2 m |

Além das calculadoras:

- **Referência bibliográfica:** como citar, sumário, busca no texto e leitor página a página, com o texto e a imagem da página completa (clique para ampliar).
- **Fórmulas:** as equações usadas, com o item do texto.
- **Figuras da referência:** os desenhos das páginas 55 a 59.
- **Validação:** a referência não traz exemplo resolvido de tubulão. O app recalcula três casos (fuste, base circular e base em falsa elipse) e compara com um recálculo manual independente, feito direto com as fórmulas (14 resultados).

## Estrutura do repositório

```
index.html        app completo: HTML, CSS, JavaScript e dados
figs/pNNN.jpg     páginas da referência; NNN = página do PDF (página do texto = NNN − 4)
tests/smoke.py    teste de fumaça (menu, validação e imagens do leitor)
CHANGELOG.md      histórico das mudanças
CLAUDE.md         notas de trabalho para quem for mexer no código
```

`figs/` tem as páginas 55 a 59 e 66 (arquivos `p059` a `p063` e `p070`). O reader lista só as páginas usadas nos cálculos; as demais páginas do texto não estão aqui.

## Repositório relacionado

[victortlacerda/blocos-coroamento](https://github.com/victortlacerda/blocos-coroamento): blocos sobre estacas, CEB-70, momentos e o **bloco de transição** (itens 16.4 e 16.5), que antes fazia parte deste app.

## Como atualizar

1. Edite o `index.html` (ele é o app inteiro: ver `CLAUDE.md` para a organização interna).
2. Rode `python3 tests/smoke.py` (precisa de `pip install playwright` e `playwright install chromium`). A página Validação tem de continuar toda conferida.
3. Anote a mudança no `CHANGELOG.md`.
4. Faça o commit e envie: `git add -A && git commit -m "..." && git push`.

## Fonte e créditos

Texto-base:

> BASTOS, P. S. S. *Blocos de Fundação*. Notas de aula da disciplina 2133 – Estruturas de Concreto III. Bauru/SP: Departamento de Engenharia Civil e Ambiental, Universidade Estadual Paulista (UNESP), out. 2023.

Página do autor: <https://wwwp.feb.unesp.br/pbastos>. O texto segue a NBR 6118/2023 e a NBR 6122/2021.

Os direitos do texto e das figuras pertencem ao autor e à UNESP. As imagens de `figs/` são páginas dessas notas de aula, reproduzidas para consulta junto às fórmulas.

O app é uma ferramenta de apoio ao estudo e ao pré-dimensionamento: o projeto final deve ser conferido por engenheiro responsável.
