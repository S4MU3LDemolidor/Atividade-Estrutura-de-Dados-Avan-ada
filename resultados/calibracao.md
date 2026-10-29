# Calibração dos limiares

Gerado por `python3 -m medicoes.calibrar` em 29/10/2026.

- Máquina: Apple M4, Darwin 25.6.0, Python 3.14.5
- Repetições por medição: 5 (vale a mediana)
- Semente: 2026

## Limiares sugeridos

```python
CORTE = 24
N_MINUSCULA = 24
FRACAO_DESCIDAS = 0.228
FATOR_QUEDAS = 3.38
FATOR_CONTAGEM = 2
N_MIN_BASE = {1: 64, 2: 256, 3: 256, 4: 512, 5: 512, 6: 1024, 7: 1024, 8: 2048, 9: 2048, 10: 2048, 11: 4096, 12: 8192}
```

## CORTE da híbrida

Híbrida numa lista aleatória de 10000 chaves grandes, variando o tamanho a partir do qual a sublista vai para a inserção.

| corte | tempo (ms) |
|---|---|
| 1 | 8,24 |
| 2 | 7,91 |
| 4 | 7,27 |
| 6 | 8,75 |
| 8 | 6,85 |
| 10 | 6,46 |
| 12 | 6,47 |
| 16 | 6,44 |
| 20 | 6,55 |
| 24 | 6,41 |
| 32 | 6,51 |
| 48 | 6,78 |
| 64 | 7,29 |

Mais rápido: **CORTE = 24**. Os experimentos seguintes usam esse corte.

## N_MINUSCULA

Lotes de 1000 listas aleatórias com valores em [0, 10^6). Tempo médio por lista, em microssegundos. A contagem fica de fora: com faixa de 10^6 ela aloca um milhão de contadores para ordenar poucos elementos.

| n | insercao | intercalacao | rapida | hibrida | base | vencedor |
|---|---|---|---|---|---|---|
| 2 | 0,15 | 0,31 | 0,35 | 0,23 | 21,16 | insercao |
| 3 | 0,20 | 0,55 | 0,57 | 0,29 | 22,64 | insercao |
| 4 | 0,28 | 0,80 | 0,85 | 0,36 | 22,92 | insercao |
| 6 | 0,45 | 1,39 | 1,37 | 0,53 | 23,66 | insercao |
| 8 | 0,71 | 1,93 | 1,89 | 0,73 | 24,30 | insercao |
| 10 | 0,87 | 2,64 | 2,58 | 0,98 | 24,42 | insercao |
| 12 | 1,16 | 3,16 | 3,10 | 1,26 | 24,26 | insercao |
| 16 | 1,81 | 4,48 | 4,37 | 1,88 | 25,09 | insercao |
| 20 | 2,59 | 5,92 | 5,66 | 2,68 | 25,83 | insercao |
| 24 | 3,54 | 7,17 | 6,99 | 3,64 | 26,93 | insercao |
| 32 | 5,56 | 9,95 | 9,84 | 5,40 | 28,06 | hibrida |
| 40 | 8,64 | 13,03 | 12,64 | 7,25 | 29,73 | hibrida |
| 48 | 12,06 | 15,82 | 15,74 | 9,14 | 30,85 | hibrida |
| 64 | 20,07 | 22,14 | 21,98 | 13,26 | 34,52 | hibrida |

A inserção vence todos até **N_MINUSCULA = 24**.

## FRACAO_DESCIDAS (desordem local)

Listas quase ordenadas de 10000 chaves grandes, com uma fração crescente de trocas entre vizinhos (até 10 posições). Tempos em ms.

| trocas | descidas/n | quedas/amplitude | inserção | melhor outro | inserção vence? |
|---|---|---|---|---|---|
| 0,1% | 0,0018 | 0,01 | 0,36 | base 2,48 | sim |
| 0,5% | 0,0092 | 0,04 | 0,38 | base 2,52 | sim |
| 1,0% | 0,0182 | 0,08 | 0,40 | base 2,54 | sim |
| 2,0% | 0,0364 | 0,16 | 0,43 | base 2,49 | sim |
| 5,0% | 0,0866 | 0,41 | 0,52 | base 2,53 | sim |
| 10,0% | 0,1560 | 0,78 | 0,67 | base 2,51 | sim |
| 20,0% | 0,2587 | 1,44 | 0,91 | base 2,62 | sim |
| 50,0% | 0,4021 | 2,87 | 1,36 | base 2,63 | sim |
| 100,0% | 0,4567 | 4,47 | 1,73 | base 2,53 | sim |

Maior descidas/n com vitória da inserção: 0,4567. Com margem de 2x: **FRACAO_DESCIDAS = 0.228**.

## FATOR_QUEDAS (desordem longe)

Lista ordenada de 10000 chaves grandes com trocas entre posições sorteadas. As descidas continuam poucas, mas cada troca obriga a inserção a atravessar muitas posições. Tempos em ms.

| trocas | descidas/n | quedas/amplitude | inserção | melhor outro | inserção vence? |
|---|---|---|---|---|---|
| 1 | 0,0002 | 1,16 | 0,66 | base 2,48 | sim |
| 2 | 0,0004 | 1,71 | 0,81 | base 2,50 | sim |
| 3 | 0,0006 | 0,40 | 0,47 | base 2,50 | sim |
| 5 | 0,0010 | 2,97 | 1,17 | base 5,33 | sim |
| 8 | 0,0016 | 6,76 | 2,22 | base 2,52 | sim |
| 10 | 0,0020 | 11,83 | 3,52 | base 2,50 | não |
| 13 | 0,0026 | 11,64 | 3,43 | base 2,48 | não |
| 16 | 0,0032 | 11,69 | 3,43 | base 2,49 | não |
| 20 | 0,0040 | 13,87 | 3,99 | base 2,49 | não |
| 30 | 0,0059 | 20,25 | 5,70 | base 2,54 | não |
| 50 | 0,0098 | 30,19 | 8,43 | base 2,45 | não |
| 100 | 0,0194 | 59,31 | 15,57 | base 2,46 | não |

Maior quedas/amplitude com vitória da inserção: 6,76. Com margem de 2x: **FATOR_QUEDAS = 3.38**.

## FATOR_CONTAGEM

Listas aleatórias de 10000 valores numa faixa k = razão × n, com mínimo e máximo repassados (como o ordenar faz). Tempos em ms.

| razão k/n | k | contagem | base | híbrida | contagem vence? |
|---|---|---|---|---|---|
| 0,01 | 100 | 0,16 | 0,43 | 2,32 | sim |
| 0,10 | 1000 | 0,28 | 0,99 | 4,14 | sim |
| 0,50 | 5000 | 0,54 | 0,99 | 5,21 | sim |
| 1,00 | 10000 | 0,73 | 0,99 | 5,24 | sim |
| 2,00 | 20000 | 0,95 | 1,01 | 5,59 | sim |
| 4,00 | 40000 | 1,23 | 0,99 | 5,62 | não |
| 8,00 | 80000 | 1,73 | 1,33 | 5,48 | não |
| 16,00 | 160000 | 2,69 | 1,36 | 5,61 | não |
| 32,00 | 320000 | 4,86 | 1,36 | 5,58 | não |
| 64,00 | 640000 | 9,03 | 1,34 | 6,01 | não |
| 128,00 | 1280000 | 17,20 | 1,36 | 5,68 | não |

A contagem vence até **FATOR_CONTAGEM = 2**. Sem margem: errar aqui custa um fator constante, não O(n²).

## N_MIN_BASE

Razão tempo(base) / tempo(híbrida) para chaves com p bytes (valores em [0, 256^p)) e tamanhos n. Abaixo de 1, a base vence. Cada célula mede um lote de cerca de 16384 elementos.

| passadas | n=16 | n=32 | n=64 | n=128 | n=256 | n=512 | n=1024 | n=2048 | n=4096 | n=8192 | n=16384 | base vence a partir de |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 4,47 | 1,78 | 0,90 | 0,55 | 0,36 | 0,23 | 0,18 | 0,16 | 0,15 | 0,15 | 0,14 | 64 |
| 2 | 8,78 | 3,45 | 1,54 | 1,03 | 0,67 | 0,91 | 0,30 | 0,25 | 0,22 | 0,18 | 0,17 | 256 |
| 3 | 13,12 | 5,05 | 2,55 | 1,50 | 0,97 | 0,59 | 0,41 | 0,35 | 0,29 | 0,26 | 0,23 | 256 |
| 4 | 13,52 | 5,49 | 2,87 | 1,66 | 1,11 | 0,72 | 0,28 | 0,43 | 0,37 | 0,34 | 0,30 | 512 |
| 5 | 19,98 | 7,79 | 3,94 | 2,26 | 1,48 | 0,90 | 0,64 | 0,53 | 0,44 | 0,39 | 0,35 | 512 |
| 6 | 23,97 | 9,18 | 4,60 | 2,68 | 1,74 | 1,08 | 0,79 | 0,55 | 0,52 | 0,46 | 0,41 | 1024 |
| 7 | 27,82 | 10,84 | 5,37 | 3,06 | 1,97 | 1,23 | 0,87 | 0,71 | 0,59 | 0,52 | 0,46 | 1024 |
| 8 | 30,75 | 11,55 | 5,82 | 3,35 | 2,18 | 1,37 | 1,03 | 0,82 | 0,69 | 0,60 | 0,53 | 2048 |
| 9 | 35,64 | 13,83 | 6,90 | 4,00 | 2,57 | 1,59 | 1,18 | 0,93 | 0,78 | 0,68 | 0,62 | 2048 |
| 10 | 39,98 | 15,37 | 7,73 | 4,42 | 2,80 | 1,76 | 1,28 | 0,97 | 0,87 | 0,75 | 0,67 | 2048 |
| 11 | 42,90 | 16,80 | 8,37 | 4,75 | 3,11 | 1,91 | 1,40 | 1,13 | 0,96 | 0,83 | 0,74 | 4096 |
| 12 | 46,24 | 18,12 | 9,04 | 5,12 | 3,32 | 2,08 | 1,51 | 1,20 | 1,02 | 0,89 | 0,80 | 8192 |

**N_MIN_BASE = {1: 64, 2: 256, 3: 256, 4: 512, 5: 512, 6: 1024, 7: 1024, 8: 2048, 9: 2048, 10: 2048, 11: 4096, 12: 8192}**

## Custo de olhar a lista

`perfil(v)` (uma passada em Python: mínimo, máximo, descidas e quedas) contra três passadas com funções nativas em C (`min`, `max` e descidas com `map`, sem as quedas), em listas de 10000. Tempos em ms.

| lista | perfil (1 passada) | nativas (3 passadas) | perfil / nativas |
|---|---|---|---|
| aleatória | 0,335 | 0,272 | 1,23 |
| quase ordenada | 0,197 | 0,304 | 0,65 |

Resultado: na lista aleatória, a passada única custa 1,23x o tempo das nativas; na lista quase ordenada, a passada única custa 0,65x o tempo das nativas. Na aleatória, metade dos elementos é descida e soma uma queda, por isso a passada única fica mais cara.
