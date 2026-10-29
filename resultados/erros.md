# Casos em que o escolher erra

Gerado por `python3 -m medicoes.erros` em 29/10/2026.

- Máquina: Apple M4, Darwin 25.6.0, Python 3.14.5
- n = 10000, semente 2026
- 5 repetições intercaladas; vale o menor tempo

| lista | descidas/n | quedas/amplitude | abaixo do máximo | escolha | ordenar (ms) | melhor fixo (ms) | ordenar / melhor |
|---|---|---|---|---|---|---|---|
| Quase ordenado (decisão certa, para comparar) | 0,018 | 0,08 | 464 | insercao | 0,58 | base 2,46 | 0,2 |
| Metades trocadas | 0,000 | 1,00 | 5000 | insercao | 643,94 | base 2,52 | 255,6 |
| 3 listas ordenadas concatenadas | 0,000 | 2,00 | 6664 | insercao | 420,02 | base 2,53 | 166,3 |
| Blocos de 5 em ordem decrescente | 0,200 | 1,79 | 9995 | insercao | 1276,15 | base 2,55 | 499,5 |
| Blocos de 5 embaralhados + um valor extremo no fim | 0,100 | 0,33 | 9955 | insercao | 628,11 | base 3,12 | 201,0 |

A regra da inserção exige descidas/n <= 0,228 e quedas/amplitude <= 3,38. "abaixo do máximo" é a medida que corrigiria esses erros (não usada pelo escolher).
