# Calibração dos limiares

Gerado por `python3 -m medicoes.calibrar` em 29/10/2026.

- Máquina: Apple M4, Darwin 25.6.0, Python 3.14.5
- 5 repetições intercaladas entre os concorrentes de cada ponto; vale o menor tempo
- Semente: 2026

## Limiares sugeridos

```python
CORTE = 20
N_MINUSCULA = 24
FRACAO_DESCIDAS = 0.228
FATOR_QUEDAS = 3.38
FATOR_CONTAGEM = 2
N_MIN_BASE = {1: 64, 2: 256, 3: 256, 4: 512, 5: 512, 6: 1024, 7: 1024, 8: 2048, 9: 2048, 10: 4096, 11: 4096, 12: 8192}
```

## CORTE da híbrida

Híbrida numa lista aleatória de 10000 chaves grandes, variando o tamanho a partir do qual a sublista vai para a inserção.

| corte | tempo (ms) |
|---|---|
| 1 | 8,15 |
| 2 | 7,71 |
| 4 | 7,10 |
| 6 | 6,72 |
| 8 | 6,78 |
| 10 | 6,39 |
| 12 | 6,53 |
| 16 | 6,35 |
| 20 | 6,25 |
| 24 | 6,27 |
| 32 | 6,48 |
| 48 | 6,68 |
| 64 | 7,12 |

Mais rápido: **CORTE = 20**. Os experimentos seguintes usam esse corte.

## N_MINUSCULA

Lotes de 1000 listas aleatórias com valores em [0, 10000). Tempo médio por lista, em microssegundos. A contagem fica de fora: ela alocaria 10000 contadores para ordenar poucos elementos.

| n | insercao | intercalacao | rapida | hibrida | base | vencedor |
|---|---|---|---|---|---|---|
| 2 | 0,14 | 0,32 | 0,35 | 0,24 | 14,77 | insercao |
| 3 | 0,19 | 0,54 | 0,56 | 0,29 | 15,40 | insercao |
| 4 | 0,26 | 0,81 | 0,86 | 0,33 | 15,49 | insercao |
| 6 | 0,42 | 1,41 | 1,33 | 0,54 | 15,94 | insercao |
| 8 | 0,65 | 1,96 | 1,89 | 0,73 | 15,97 | insercao |
| 10 | 0,89 | 2,63 | 2,47 | 0,98 | 16,41 | insercao |
| 12 | 1,15 | 3,22 | 3,09 | 1,26 | 16,53 | insercao |
| 16 | 1,87 | 4,54 | 4,37 | 1,94 | 17,11 | insercao |
| 20 | 2,66 | 5,98 | 5,73 | 2,73 | 17,76 | insercao |
| 24 | 3,61 | 7,35 | 6,99 | 3,73 | 18,47 | insercao |
| 32 | 6,01 | 10,32 | 9,90 | 5,50 | 19,64 | hibrida |
| 40 | 8,46 | 13,42 | 12,86 | 7,33 | 20,70 | hibrida |
| 48 | 11,80 | 16,31 | 15,84 | 9,26 | 21,83 | hibrida |
| 64 | 21,16 | 22,57 | 22,23 | 13,38 | 23,94 | hibrida |

A inserção vence todos até **N_MINUSCULA = 24**.

## FRACAO_DESCIDAS (desordem local)

Listas quase ordenadas de 10000 chaves grandes, com uma fração crescente de trocas entre vizinhos (até 10 posições). Tempos em ms.

| trocas | descidas/n | quedas/amplitude | inserção | melhor outro | inserção vence? |
|---|---|---|---|---|---|
| 0,1% | 0,0018 | 0,01 | 0,37 | base 2,49 | sim |
| 0,5% | 0,0092 | 0,04 | 0,37 | base 2,58 | sim |
| 1,0% | 0,0182 | 0,08 | 0,38 | base 2,50 | sim |
| 2,0% | 0,0364 | 0,16 | 0,42 | base 2,51 | sim |
| 5,0% | 0,0866 | 0,41 | 0,51 | base 2,51 | sim |
| 10,0% | 0,1560 | 0,78 | 0,65 | base 2,56 | sim |
| 20,0% | 0,2587 | 1,44 | 0,88 | base 2,54 | sim |
| 50,0% | 0,4021 | 2,87 | 1,29 | base 2,54 | sim |
| 100,0% | 0,4567 | 4,47 | 1,70 | base 2,51 | sim |

Maior descidas/n com vitória da inserção: 0,4567. Com margem de 2x: **FRACAO_DESCIDAS = 0.228**.

## FATOR_QUEDAS (desordem longe)

Lista ordenada de 10000 chaves grandes com trocas entre posições sorteadas. As descidas continuam poucas, mas cada troca obriga a inserção a atravessar muitas posições. Tempos em ms.

| trocas | descidas/n | quedas/amplitude | inserção | melhor outro | inserção vence? |
|---|---|---|---|---|---|
| 1 | 0,0002 | 1,16 | 0,66 | base 2,50 | sim |
| 2 | 0,0004 | 1,71 | 0,81 | base 2,49 | sim |
| 3 | 0,0006 | 0,40 | 0,47 | base 2,48 | sim |
| 5 | 0,0010 | 2,97 | 1,15 | base 2,48 | sim |
| 8 | 0,0016 | 6,76 | 2,17 | base 2,51 | sim |
| 10 | 0,0020 | 11,83 | 3,43 | base 2,48 | não |
| 13 | 0,0026 | 11,64 | 3,39 | base 2,48 | não |
| 16 | 0,0032 | 11,69 | 3,41 | base 2,47 | não |
| 20 | 0,0040 | 13,87 | 3,97 | base 2,47 | não |
| 30 | 0,0059 | 20,25 | 5,59 | base 2,52 | não |
| 50 | 0,0098 | 30,19 | 8,35 | base 2,50 | não |
| 100 | 0,0194 | 59,31 | 15,51 | base 2,49 | não |

Maior quedas/amplitude com vitória da inserção: 6,76. Com margem de 2x: **FATOR_QUEDAS = 3.38**.

## FATOR_CONTAGEM

Listas aleatórias de 10000 valores numa faixa k = razão × n, com mínimo e máximo repassados (como o ordenar faz). Tempos em ms.

| razão k/n | k | contagem | base | híbrida | contagem vence? |
|---|---|---|---|---|---|
| 0,01 | 100 | 0,16 | 0,42 | 2,32 | sim |
| 0,10 | 1000 | 0,27 | 1,03 | 4,14 | sim |
| 0,50 | 5000 | 0,52 | 1,01 | 5,09 | sim |
| 1,00 | 10000 | 0,73 | 1,01 | 5,36 | sim |
| 2,00 | 20000 | 0,93 | 1,01 | 5,41 | sim |
| 4,00 | 40000 | 1,21 | 1,02 | 5,50 | não |
| 8,00 | 80000 | 1,72 | 1,33 | 5,24 | não |
| 16,00 | 160000 | 2,78 | 1,36 | 5,65 | não |
| 32,00 | 320000 | 4,53 | 1,35 | 5,45 | não |
| 64,00 | 640000 | 8,42 | 1,35 | 5,40 | não |
| 128,00 | 1280000 | 16,49 | 1,37 | 5,45 | não |

A contagem vence até **FATOR_CONTAGEM = 2**. Sem margem: errar aqui custa um fator constante, não O(n²).

## N_MIN_BASE

Razão tempo(base) / tempo(híbrida) para chaves com p bytes (valores em [0, 256^p)) e tamanhos n. Abaixo de 1, a base vence. Cada célula mede um lote de cerca de 16384 elementos.

| passadas | n=16 | n=32 | n=64 | n=128 | n=256 | n=512 | n=1024 | n=2048 | n=4096 | n=8192 | n=16384 | base vence a partir de |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 4,39 | 1,75 | 0,89 | 0,52 | 0,36 | 0,23 | 0,18 | 0,17 | 0,15 | 0,16 | 0,16 | 64 |
| 2 | 8,74 | 3,39 | 1,74 | 1,02 | 0,67 | 0,43 | 0,31 | 0,25 | 0,21 | 0,20 | 0,17 | 256 |
| 3 | 12,99 | 5,05 | 2,51 | 1,47 | 0,96 | 0,59 | 0,44 | 0,35 | 0,30 | 0,27 | 0,23 | 256 |
| 4 | 13,25 | 5,56 | 2,91 | 1,70 | 1,10 | 0,73 | 0,53 | 0,43 | 0,37 | 0,33 | 0,31 | 512 |
| 5 | 19,57 | 7,65 | 3,96 | 2,26 | 1,45 | 0,90 | 0,67 | 0,54 | 0,45 | 0,40 | 0,35 | 512 |
| 6 | 23,56 | 9,01 | 4,64 | 2,68 | 1,71 | 1,09 | 0,78 | 0,63 | 0,53 | 0,47 | 0,42 | 1024 |
| 7 | 26,96 | 10,60 | 5,40 | 3,07 | 2,00 | 1,23 | 0,88 | 0,73 | 0,61 | 0,52 | 0,48 | 1024 |
| 8 | 28,78 | 11,47 | 5,67 | 3,30 | 2,14 | 1,37 | 1,01 | 0,83 | 0,70 | 0,64 | 0,56 | 2048 |
| 9 | 34,37 | 13,57 | 6,77 | 3,98 | 2,57 | 1,62 | 1,20 | 0,94 | 0,79 | 0,69 | 0,63 | 2048 |
| 10 | 38,07 | 14,95 | 7,55 | 4,37 | 2,80 | 1,73 | 1,27 | 1,03 | 0,89 | 0,78 | 0,70 | 4096 |
| 11 | 42,30 | 16,38 | 8,12 | 4,72 | 3,16 | 1,93 | 1,40 | 1,15 | 0,96 | 0,86 | 0,73 | 4096 |
| 12 | 47,00 | 18,27 | 9,07 | 5,21 | 3,31 | 2,11 | 1,50 | 1,23 | 1,03 | 0,89 | 0,82 | 8192 |

**N_MIN_BASE = {1: 64, 2: 256, 3: 256, 4: 512, 5: 512, 6: 1024, 7: 1024, 8: 2048, 9: 2048, 10: 4096, 11: 4096, 12: 8192}**

## Custo de olhar a lista

`perfil(v)` (uma passada em Python: mínimo, máximo, descidas e quedas) contra três passadas com funções nativas em C (`min`, `max` e descidas com `map`, sem as quedas), em listas de 10000. Tempos em ms.

| lista | perfil (1 passada) | nativas (3 passadas) | perfil / nativas |
|---|---|---|---|
| aleatória | 0,339 | 0,268 | 1,26 |
| quase ordenada | 0,197 | 0,298 | 0,66 |

Resultado: na lista aleatória, a passada única custa 1,26x o tempo das nativas; na lista quase ordenada, a passada única custa 0,66x o tempo das nativas. Na aleatória, metade dos elementos é descida e soma uma queda, por isso a passada única fica mais cara.
