# Medições

Gerado por `python3 -m medicoes.medir` em 29/10/2026.

- Máquina: Apple M4, Darwin 25.6.0, Python 3.14.5
- n = 10000, semente 2026
- 5 repetições intercaladas entre os concorrentes; vale o menor tempo
- Tempos brutos em `resultados/medicoes.csv`

## Tempos

- **Aleatório, chaves grandes**: 10000 valores em [0, 10^12)
- **Faixa estreita**: 10000 valores em [0, 100)
- **Quase ordenado**: 10000 chaves grandes ordenadas com 1% de trocas entre vizinhos (até 10 posições)
- **Lista minúscula**: 1000 listas de 8 valores em [0, 10000)

| cenário | insercao | intercalacao | rapida | hibrida | contagem | base | ordenar | vencedor fixo | ordenar escolheu |
|---|---|---|---|---|---|---|---|---|---|
| Aleatório, chaves grandes (ms) | 659,04 | 7,33 | 7,77 | 6,38 | recusou | **2,61** | 2,93 | base | base |
| Faixa estreita (ms) | 542,57 | 6,55 | 2,18 | 2,23 | **0,30** | 0,59 | 0,37 | contagem | contagem |
| Quase ordenado (ms) | **0,39** | 5,91 | 7,02 | 6,08 | recusou | 2,46 | 0,59 | insercao | insercao |
| Lista minúscula (µs por lista) | **0,66** | 1,97 | 1,97 | 0,69 | 89,60 | 15,94 | 0,75 | insercao | insercao |

Em negrito, o método fixo mais rápido do cenário. "recusou": a contagem lançou `FaixaGrandeDemais` antes de alocar os contadores.

## Razão para o mais rápido de cada cenário

Tempo de cada concorrente dividido pelo menor tempo do cenário (1,00 = o mais rápido). A pior razão mostra quanto se perde, no pior cenário, por ficar preso àquela escolha.

| método | Aleatório, chaves grandes | Faixa estreita | Quase ordenado | Lista minúscula | pior razão | média geométrica |
|---|---|---|---|---|---|---|
| insercao | 252,82 | 1822,25 | 1,00 | 1,00 | 1822,25 | 26,05 |
| intercalacao | 2,81 | 21,99 | 15,32 | 2,97 | 21,99 | 7,28 |
| rapida | 2,98 | 7,31 | 18,20 | 2,97 | 18,20 | 5,86 |
| hibrida | 2,45 | 7,47 | 15,76 | 1,04 | 15,76 | 4,16 |
| contagem | ∞ | 1,00 | ∞ | 134,94 | ∞ | ∞ |
| base | 1,00 | 2,00 | 6,38 | 24,01 | 24,01 | 4,18 |
| ordenar | 1,12 | 1,25 | 1,53 | 1,12 | 1,53 | 1,25 |

Pior razão do `ordenar`: **1,53**. Melhor método fixo por esse critério: **hibrida**, com pior razão **15,76**. O `ordenar` ganha de qualquer escolha fixa.

## Custo do escolher

Tempo do `escolher` sozinho comparado com o `ordenar` inteiro (que inclui o `escolher`). A última coluna compara o `ordenar` com o melhor método fixo do cenário.

| cenário | escolha | escolher | método escolhido sozinho | ordenar | escolher / ordenar | ordenar / melhor fixo |
|---|---|---|---|---|---|---|
| Aleatório, chaves grandes | base | 0,34 | 2,61 | 2,93 | 11,7% | 1,12 |
| Faixa estreita | contagem | 0,21 | 0,30 | 0,37 | 56,5% | 1,25 |
| Quase ordenado | insercao | 0,20 | 0,39 | 0,59 | 33,2% | 1,53 |
| Lista minúscula | insercao | 0,03 | 0,66 | 0,75 | 3,5% | 1,12 |

Unidades como na primeira tabela (ms; µs por lista na minúscula).

## Reaproveitar mínimo e máximo

O `escolher` já calcula mínimo e máximo; o `ordenar` repassa os dois para a contagem e a base, que assim não percorrem a lista de novo. Tempos em ms.

| cenário | método | calculando | repassados | economia | custo do escolher |
|---|---|---|---|---|---|
| Aleatório, chaves grandes | base | 2,607 | 2,443 | 0,164 | 0,342 |
| Faixa estreita | contagem | 0,298 | 0,160 | 0,138 | 0,211 |

## Cenário em que o escolher erra

**Metades trocadas**: 10000 chaves grandes ordenadas com a segunda metade movida para a frente. O `escolher` escolheu **insercao**; o melhor método fixo foi **base**.

| método | tempo (ms) |
|---|---|
| insercao | 647,22 |
| intercalacao | 5,88 |
| rapida | 7,07 |
| hibrida | 5,82 |
| contagem | recusou |
| base | **2,46** |
| ordenar | 641,55 |

O `ordenar` levou 261,2x o tempo do melhor método.
