# Relatório: ordenação adaptativa

Dupla: Samuel Ribeiro Cardoso e Pedro Augusto

Nenhum dos seis métodos ganha sempre. Cada método fixo perde feio em pelo menos
um dos quatro cenários: no melhor caso fica 15,8 vezes mais lento que o mais
rápido (híbrida no quase ordenado), e a contagem nem consegue rodar em dois
cenários. O `ordenar`, que decide sozinho, fica no máximo 1,53 vez mais lento
que o mais rápido de cada cenário. É essa diferença que mostra que ele ganha de
qualquer escolha fixa.

Os números abaixo vêm de `resultados/tabela.md` e `resultados/calibracao.md`,
que podem ser gerados de novo com os comandos do README.

## 1. Cenários e como foram medidos

| Cenário | Lista |
|---|---|
| Aleatório, chaves grandes | 10 000 valores em [0, 10¹²) |
| Faixa estreita | 10 000 valores em [0, 100) |
| Quase ordenado | 10 000 chaves grandes ordenadas, com 1% de trocas entre vizinhos (até 10 posições de distância) |
| Lista minúscula | 1000 listas diferentes de 8 valores em [0, 10⁴); o tempo é por lista |

- Máquina: Apple M4 (4 núcleos de desempenho e 6 de eficiência), macOS (Darwin 25.6.0), Python 3.14.5.
- Semente 2026: as listas e os pivôs sorteados são sempre os mesmos.
- Cada concorrente foi medido 5 vezes com `time.perf_counter_ns()`, com o coletor de lixo desligado durante a medição.
- As repetições são **intercaladas**: cada rodada mede todos os concorrentes do
  cenário uma vez, e a ordem gira de uma rodada para a outra. Vale o **menor**
  tempo das 5.

Por que intercalado e pelo mínimo: a primeira versão fazia 5 repetições
seguidas de cada método e usava a mediana. Numa das medições o `escolher` levou
0,22 ms nas duas primeiras repetições e 0,55 ms nas três últimas, com a mesma
entrada. Forçando o processo nos núcleos de eficiência (`taskpolicy -b`), o
mesmo código leva no mínimo 0,556 ms. Ou seja, o sistema tinha trocado o
processo de núcleo no meio da medição. Interferência desse tipo só atrasa, nunca
adianta, então o menor tempo é a melhor estimativa (é também o que recomenda a
documentação do módulo `timeit` do Python). Intercalar faz com que uma
interferência atinja todos os métodos, e não só o que estava no relógio. A
medição ainda confere a si mesma: se o `escolher` sozinho sair mais lento que o
`ordenar` (que o inclui), ela avisa que houve interferência.

## 2. Tabela: quatro cenários contra os seis métodos

Tempos em ms (na lista minúscula, µs por lista). Em negrito, o método fixo mais
rápido de cada cenário.

| cenário | inserção | intercalação | rápida | híbrida | contagem | base | **ordenar** |
|---|---|---|---|---|---|---|---|
| Aleatório, chaves grandes (ms) | 659,04 | 7,33 | 7,77 | 6,38 | recusou | **2,61** | 2,93 |
| Faixa estreita (ms) | 542,57 | 6,55 | 2,18 | 2,23 | **0,30** | 0,59 | 0,37 |
| Quase ordenado (ms) | **0,39** | 5,91 | 7,02 | 6,08 | recusou | 2,46 | 0,59 |
| Lista minúscula (µs) | **0,66** | 1,97 | 1,97 | 0,69 | 89,60 | 15,94 | 0,75 |

"recusou": a contagem lançou `FaixaGrandeDemais` sem alocar nada. Com valores
até 10¹² ela precisaria de 10¹² contadores.

Para comparar cenários com tempos tão diferentes, dividimos cada tempo pelo menor
tempo do cenário (1,00 = o mais rápido). A **pior razão** de um método é o
quanto ele perde no cenário que mais o prejudica:

| método | Aleatório | Faixa estreita | Quase ordenado | Minúscula | **pior razão** | média geométrica |
|---|---|---|---|---|---|---|
| inserção | 252,82 | 1822,25 | 1,00 | 1,00 | 1822,25 | 26,05 |
| intercalação | 2,81 | 21,99 | 15,32 | 2,97 | 21,99 | 7,28 |
| rápida | 2,98 | 7,31 | 18,20 | 2,97 | 18,20 | 5,86 |
| híbrida | 2,45 | 7,47 | 15,76 | 1,04 | 15,76 | 4,16 |
| contagem | ∞ | 1,00 | ∞ | 134,94 | ∞ | ∞ |
| base | 1,00 | 2,00 | 6,38 | 24,01 | 24,01 | 4,18 |
| **ordenar** | 1,12 | 1,25 | 1,53 | 1,12 | **1,53** | **1,25** |

A melhor escolha fixa por esse critério é a híbrida, que perde até 15,76 vezes.
O `ordenar` perde no máximo 1,53 vez. Rodando a medição duas vezes, a pior razão
do `ordenar` deu 1,53 nas duas, e as razões dele variaram menos de 0,1 entre as
rodadas.

## 3. Quem venceu cada cenário, e por quê

**Aleatório com chaves grandes: base (2,61 ms).** Valores abaixo de 10¹² cabem
em 40 bits, ou seja, 5 bytes. A base faz 5 passadas, e cada uma só calcula um
byte e anexa o valor a um balde, sem nenhuma comparação. Os métodos por
comparação precisam de cerca de n·log₂n ≈ 133 mil comparações, e em Python cada
uma é uma instrução interpretada. A híbrida, melhor delas, leva 6,38 ms (2,4x).
Ela vence a intercalação e a rápida pura porque termina as sublistas de até 20
elementos com inserção, que tem custo fixo menor que a recursão. A inserção faz
cerca de n²/4 = 25 milhões de deslocamentos e leva 659 ms.

**Faixa estreita: contagem (0,30 ms).** Com valores em [0, 100) bastam 100
contadores: uma passada conta e outra reconstrói a lista. A base precisa de uma
passada só (a faixa cabe num byte), mas distribuir em 256 baldes e juntar tudo
de novo custa o dobro (0,59 ms). A rápida se sai bem (2,18 ms) graças à partição
em três vias: cada partição tira de uma vez todas as cópias do pivô, e com 100
valores distintos a recursão acaba logo. Com a partição clássica em duas vias,
os repetidos levariam a O(n²).

**Quase ordenado: inserção (0,39 ms).** A inserção custa O(n + inversões).
Nessa lista há 182 descidas, e cada elemento anda em média 0,075 posição. Na
prática, é uma passada só. A base ignora a ordem que já existe (2,46 ms, 6,4x),
e os métodos por comparação também (de 5,9 a 7,0 ms, 15 a 18x).

**Lista minúscula: inserção (0,66 µs).** Com 8 elementos, o que pesa é o custo
fixo de cada método. A inserção não faz recursão e não aloca nada além da cópia.
A híbrida quase empata (0,69 µs), porque com corte 20 ela vai direto para a
inserção e só paga uma chamada a mais. A intercalação e a rápida pagam recursão
(cerca de 2 µs). A base aloca 256 baldes por passada para ordenar 8 números
(15,9 µs). A contagem aloca 10 mil contadores (89,6 µs, 135x). Ela não estoura o
limite de memória, mas mostra por que a regra da contagem compara a faixa com o
tamanho da lista, e não só com o limite.

## 4. Regras do `escolher` e de onde vieram

O `escolher` (`ordenacao/escolhedor.py`) aplica as regras nesta ordem:

```
1. n <= 24                                        -> inserção (nem olha a lista)
2. uma passada só: mínimo, máximo, descidas e quedas
3. descidas <= 0,228·n  e  quedas <= 3,38·(máx − mín)   -> inserção
4. faixa = máx − mín + 1 <= 10 milhões  e  faixa <= 2·n  -> contagem
5. n >= N_MIN_BASE[bytes de (máx − mín)]          -> base
6. senão                                          -> híbrida
```

**Descidas** são as posições com `v[i] > v[i+1]`. **Quedas** são a soma de
`v[i] − v[i+1]` nessas posições. A passada faz duas comparações por elemento na
maior parte das vezes: um novo mínimo sempre é uma descida, e um novo máximo
nunca é, então só é preciso testar o mínimo dentro do caso da descida e o máximo
fora dele.

Cada limiar saiu de uma varredura em `medicoes/calibrar.py` (tabelas completas
em `resultados/calibracao.md`):

| Limiar | Valor | De onde veio |
|---|---|---|
| `N_MINUSCULA` | 24 | Listas aleatórias de 2 a 64 elementos. A inserção vence todos até 24 (3,61 µs contra 3,73 da híbrida); com 32, a híbrida já vence (5,50 contra 6,01). |
| `FRACAO_DESCIDAS` | 0,228 | Listas com desordem local crescente. A inserção venceu em toda a varredura, até 45,7% de descidas; usamos metade disso. |
| `FATOR_QUEDAS` | 3,38 | Listas com trocas entre posições distantes. A inserção vence até quedas/amplitude = 6,76 (2,17 ms contra 2,51 da base) e perde a partir de 11,83 (3,43 contra 2,48); usamos metade de 6,76. |
| `FATOR_CONTAGEM` | 2 | Faixa k = 2n: contagem 0,93 ms contra 1,01 da base. Com k = 4n: 1,21 contra 1,02. |
| `LIMITE_CONTADORES` | 10 milhões | Não é calibrado: é um teto de memória. 10 milhões de contadores numa lista do Python ocupam cerca de 80 MB. |
| `N_MIN_BASE` | {1: 64, 2: 256, …, 5: 512, …, 12: 8192} | Base contra híbrida para chaves de 1 a 12 bytes e n de 16 a 16384. Com 5 bytes (o cenário aleatório), a base vence a partir de n = 512. Acima de 12 bytes, sempre híbrida. |
| `CORTE` (híbrida) | 20 | A curva é quase plana entre 10 e 32 (6,25 a 6,53 ms); 20 foi o menor. |

**Por que olhar as quedas, e não só as descidas.** A primeira versão olhava só
as descidas, e a calibração mostrou que isso não basta. Uma lista com 1% de
trocas entre vizinhos tem 1,82% de descidas, e a inserção leva 0,38 ms. Uma lista
com 100 trocas entre posições distantes tem quase a mesma coisa (1,94%), mas a
inserção leva 15,5 ms, 40 vezes mais. O custo da inserção depende de **quanto**
cada elemento precisa andar, não de quantos estão fora do lugar. Se as chaves
estão bem espalhadas, um elemento deslocado `d` posições cria uma queda de
cerca de `d × amplitude / n`. Então `quedas / amplitude` estima quantas posições
cada elemento anda, em média, na inserção: 0,08 no primeiro caso e 59,3 no
segundo. As descidas continuam na regra por outro motivo: um único valor
extremo (por exemplo, uma lista aleatória com um 10¹² no meio) aumenta a
amplitude e faria as quedas parecerem pequenas. Uma lista assim tem cerca de n/2
descidas e é barrada.

**Por que margem de 2x só nas regras da inserção.** Os erros não custam o mesmo.
Mandar para a inserção uma lista que não é quase ordenada custa O(n²): na seção
6, isso dá 261 vezes mais lento. Errar a contagem ou a base custa um fator
constante, cerca de 2x no pior caso medido. Por isso as regras da inserção levam
margem de segurança e as outras não.

**Por que essa ordem.** A inserção vem primeiro porque, quando a lista está
quase ordenada, ela é O(n) e não há como fazer melhor. Depois vem a contagem,
O(n + k) com k ≤ 2n, depois a base. A híbrida fica por último porque nunca é
catastrófica: O(n log n) esperado, pivô aleatório contra entradas
desfavoráveis, partição em três vias contra repetidos. A intercalação e a rápida
pura nunca são escolhidas porque a híbrida venceu as duas em todos os pontos
medidos. Elas continuam na tabela como métodos fixos.

**O aviso sobre a memória da contagem.** A regra 4 usa o mínimo e o máximo que a
passada já calculou para decidir **antes** de chamar a contagem. Além disso, a
própria contagem tem uma trava: se a faixa passar de 10 milhões, ela lança
`FaixaGrandeDemais` antes de alocar. Foi essa trava que fez a contagem fixa
recusar dois cenários na tabela, sem gastar memória.

## 5. Quanto custa rodar o `escolher`, e se compensa

| cenário | escolha | `escolher` | `ordenar` | escolher / ordenar | ordenar / melhor fixo |
|---|---|---|---|---|---|
| Aleatório, chaves grandes | base | 0,34 ms | 2,93 ms | 11,7% | 1,12 |
| Faixa estreita | contagem | 0,21 ms | 0,37 ms | 56,5% | 1,25 |
| Quase ordenado | inserção | 0,20 ms | 0,59 ms | 33,2% | 1,53 |
| Lista minúscula | inserção | 0,03 µs | 0,75 µs | 3,5% | 1,12 |

O `escolher` custa uma passada pela lista. Em 10 mil elementos, isso dá de 0,2 a
0,34 ms. Na lista aleatória ele é mais caro, porque metade dos elementos é
descida e soma uma queda. Na lista minúscula ele não percorre nada: devolve uma
resposta pronta. Antes dessa mudança ele criava uma `Escolha` nova a cada
chamada e custava 0,141 µs. Com a resposta pronta caiu para 0,026 µs, e o que o
`ordenar` paga a mais que a inserção caiu de 36% para cerca de 13%.

**Comparado com o melhor método de cada cenário, o `ordenar` perde de 12% a
53%.** É o preço de não saber o cenário com antecedência. O custo pesa mais
quando o método escolhido já é muito rápido. Na faixa estreita, a contagem com
mínimo e máximo repassados leva 0,16 ms, menos que o próprio `escolher` (0,21
ms). No quase ordenado, a passada é um terço do tempo total.

**Mesmo assim compensa, porque ninguém sabe o cenário antes.** Ficar preso a
qualquer método fixo custa, no pior cenário, entre 15,8x (híbrida) e 1822x
(inserção), e a contagem simplesmente não roda em dois cenários. O `ordenar`
nunca passa de 1,53x. Pela média geométrica das razões, dá 1,25 contra 4,16 da
melhor escolha fixa. Só vale a pena chamar um método direto quando se sabe de
antemão que os dados são sempre do mesmo tipo, por exemplo sempre de faixa
estreita.

**O aviso sobre percorrer a lista duas vezes.** Tomamos três cuidados:

1. Uma passada coleta tudo o que as regras usam.
2. O mínimo e o máximo dessa passada são repassados para a contagem e a base, que
   assim não percorrem a lista de novo. Isso economiza 0,164 ms na base (cenário
   aleatório) e 0,138 ms na contagem (faixa estreita), entre metade e dois
   terços do custo do próprio `escolher`. Sem isso, o ganho seria anulado
   exatamente como o enunciado avisa.
3. Medimos se uma passada em Python sai mesmo mais barata que várias passadas
   com funções nativas do Python, que rodam em C (`min`, `max` e a contagem de
   descidas com `map`). Na lista quase ordenada, a passada única ganha (0,197 ms
   contra 0,298). Na aleatória, perde (0,339 contra 0,268), em boa parte porque
   calcula uma coisa que as nativas não calculam: as quedas. Em Python, o que pesa é o trabalho interpretado
   por elemento, não o número de passadas. Por isso a passada foi escrita para
   fazer duas comparações por elemento na maior parte dos casos.

## 6. Um cenário em que o `escolher` erra a decisão

**Metades trocadas:** 10 mil chaves grandes já ordenadas, com a segunda metade
movida para a frente: `[5000, 5001, …, 9999, 0, 1, …, 4999]` (com chaves grandes
no lugar desses números).

O que o `escolher` vê: **uma** descida só, na emenda das metades. A queda dessa
descida é praticamente a amplitude inteira, então `quedas / amplitude = 1,0`. As
duas condições da regra 3 passam (1 ≤ 0,228·n e 1,0 ≤ 3,38), e ele escolhe a
inserção.

O que acontece de verdade: cada um dos 5000 elementos da segunda parte tem que
atravessar os 5000 da primeira, o que dá 25 milhões de deslocamentos.

| método | tempo (ms) |
|---|---|
| inserção | 647,22 |
| intercalação | 5,88 |
| rápida | 7,07 |
| híbrida | 5,82 |
| contagem | recusou |
| **base** | **2,46** |
| ordenar (escolheu inserção) | 641,55 |

O `ordenar` levou **261 vezes** o tempo da base.

Por que erra: a estimativa das quedas supõe que os elementos fora do lugar estão
**isolados**, cada um com a sua queda. Num bloco deslocado, 5000 elementos estão
fora do lugar, mas só o primeiro cria queda, porque os outros estão em ordem em
relação aos vizinhos. A contagem de descidas tem o mesmo ponto cego. O erro se
repete em qualquer lista formada por poucos blocos grandes ordenados na ordem
errada.

Como dava para corrigir (não implementamos): contar, na mesma passada, quantos
elementos ficam abaixo do maior valor visto até ali. Na lista das metades
trocadas são 5000; no cenário quase ordenado, só os poucos elementos trocados. A
passada já guarda o máximo, então isso custaria só um incremento a mais em
alguns elementos. Mantivemos as regras como foram calibradas, porque qualquer
estimativa barata sempre deixa algum caso de fora, e o enunciado pede justamente
para mostrar um.

Há também erros mais baratos, de propósito. Por causa da margem de segurança,
uma lista com 20% de trocas entre vizinhos (25,9% de descidas) vai para a base
(2,54 ms), quando a inserção levaria 0,88 ms. É um erro de 2,9x, aceito para
evitar o erro de 261x do outro lado.

## 7. Limitações

- Os limiares de desordem e da contagem foram calibrados com n = 10 000. Para
  listas muito maiores, os pontos de virada mudam. Por exemplo, a inserção
  aguenta mais deslocamentos por elemento antes de perder para um método
  O(n log n), já que log n cresce. Só a tabela da base e o limite das listas
  minúsculas foram medidos em vários tamanhos.
- Os resultados são de Python. Em C, a diferença entre comparar e calcular um
  byte seria outra, e a ordem entre base e híbrida provavelmente mudaria.
- A estimativa das quedas supõe chaves bem espalhadas na faixa. Com valores muito
  concentrados em alguns pontos, ela fica menos precisa.
