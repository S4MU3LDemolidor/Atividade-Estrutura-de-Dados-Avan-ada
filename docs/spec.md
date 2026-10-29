# Especificação: ordenação adaptativa

## 1. Objetivo

Construir `ordenar(v)`, que chama `escolher(v)` para decidir qual dos seis
métodos do semestre usar e então executa esse método. A meta é mostrar, com
medições, que `ordenar` ganha de qualquer escolha fixa de método quando
consideramos os quatro cenários juntos.

## 2. Requisitos

| Id | Requisito |
|---|---|
| R1 | Implementar inserção, intercalação, rápida com pivô aleatório, híbrida (rápida + inserção), contagem e base. |
| R2 | `escolher(v)` olha a lista e devolve o método mais adequado, gastando pouco para isso. |
| R3 | `ordenar(v)` chama `escolher` e executa o método escolhido. |
| R4 | Medir quatro cenários: aleatório com chaves grandes, faixa estreita, quase ordenado e lista minúscula. |
| R5 | Comparar `ordenar` com cada método fixo nos mesmos cenários. |
| R6 | A contagem não pode estourar a memória: o escolhedor prevê a faixa antes de chamá-la. |
| R7 | O escolhedor percorre a lista uma única vez. |
| R8 | Testes com lista vazia, um elemento, todos iguais, já ordenada, invertida e valores negativos. |
| R9 | README explica como refazer as medições. |
| R10 | RELATORIO.md com a tabela, o vencedor de cada cenário e o porquê, as regras e a origem delas, o custo do `escolher` e um cenário em que ele erra. |

## 3. Contrato comum dos métodos

- Entrada: lista de inteiros, que pode ter negativos, repetidos ou estar vazia.
- Saída: uma **nova** lista em ordem crescente. A lista de entrada não é alterada.
- Só biblioteca padrão. `sorted()` aparece apenas nos testes, como referência.

## 4. Métodos

| Método | Arquivo | Assinatura | Observações |
|---|---|---|---|
| Inserção | `ordenacao/insercao.py` | `insercao(v)` | Também expõe `insercao_intervalo(a, ini, fim)`, que ordena `a[ini..fim]` no lugar e é usada pela híbrida. |
| Intercalação | `ordenacao/intercalacao.py` | `intercalacao(v)` | De cima para baixo, com um vetor auxiliar alocado uma vez. Estável. |
| Rápida | `ordenacao/rapida.py` | `rapida(v)` | Pivô aleatório e partição em três vias (`particionar(a, ini, fim)` devolve os limites da faixa igual ao pivô). Recursão só na parte menor; a maior fica num laço, o que limita a profundidade a O(log n). |
| Híbrida | `ordenacao/hibrida.py` | `hibrida(v, corte=CORTE)` | Mesma partição da rápida. Sublistas com até `corte` elementos vão para `insercao_intervalo`. |
| Contagem | `ordenacao/contagem.py` | `contagem(v, minimo=None, maximo=None)` | Desloca pelo mínimo. Se `maximo - minimo + 1 > LIMITE_CONTADORES` (10 milhões), lança `FaixaGrandeDemais` **antes** de alocar. |
| Base | `ordenacao/base.py` | `base(v, minimo=None, maximo=None)` | Radix LSD em base 256, deslocado pelo mínimo. Passadas = bytes de `maximo - minimo` (`passadas(faixa)`). |

Quando `minimo`/`maximo` não são informados, contagem e base calculam os dois
com `min()` e `max()`.

## 5. `escolher` e `ordenar`

### 5.1 O que o `escolher` olha

Uma única passada pela lista coleta:

- `n`: tamanho (de graça, com `len`);
- `minimo` e `maximo`;
- `descidas`: quantas posições têm `v[i] > v[i+1]`.

Um novo mínimo sempre é também uma descida, e um novo máximo nunca é. Por isso,
a cada elemento, a passada faz só duas comparações na maior parte dos casos.
Listas minúsculas nem são percorridas.

Medição prévia (Python 3.14, 10 mil elementos): uma passada em Python custou
0,21 ms, contra 0,28 ms de `min()` + `max()` + contagem de descidas com funções
nativas. A passada única é mais barata, mesmo competindo com código em C.

### 5.2 Regras, nesta ordem

1. `n < 2` ou `n <= N_MINUSCULA` → **inserção** (sem percorrer a lista).
2. `descidas <= FRACAO_DESCIDAS * n` → **inserção** (quase ordenada).
3. `k = maximo - minimo + 1`. Se `k <= LIMITE_CONTADORES` e `k <= FATOR_CONTAGEM * n` → **contagem**.
4. `p = passadas(maximo - minimo)`. Se `p` está em `N_MIN_BASE` e `n >= N_MIN_BASE[p]` → **base**.
5. Caso contrário → **híbrida**.

A regra 3 cumpre o R6: a contagem só é chamada quando a faixa já é conhecida e
cabe no limite. Além disso, a trava dentro da própria contagem protege chamadas
diretas.

`escolher(v)` devolve `Escolha(metodo, minimo, maximo)`. Na regra 1, `minimo`
e `maximo` são `None`. Nas demais, `ordenar` repassa os dois para contagem e
base, que assim não percorrem a lista de novo.

Intercalação e rápida pura nunca são escolhidas, se as medições confirmarem que
a híbrida domina as duas. Elas continuam medidas como métodos fixos.

### 5.3 De onde vêm os limiares

Todos saem de `medicoes/calibrar.py` e ficam como constantes em
`ordenacao/escolhedor.py`, com um comentário apontando o resultado da calibração.

| Limiar | Experimento |
|---|---|
| `CORTE` (híbrida) | Híbrida em lista aleatória de 10 mil com cortes de 1 a 64; fica o mais rápido. |
| `N_MINUSCULA` | Listas aleatórias de 2 a 64 elementos (em lote); maior `n` em que a inserção ainda vence todos os outros. |
| `FRACAO_DESCIDAS` | Listas quase ordenadas de 10 mil com fração crescente de trocas locais; maior `descidas/n` em que a inserção vence, dividido por 2 como margem de segurança (errar para a inserção custa O(n²)). |
| `FATOR_CONTAGEM` | Listas de 10 mil com faixa `k = r * n`, `r` de 0,01 a 64; maior `r` em que a contagem vence base e híbrida. |
| `N_MIN_BASE[p]` | Para `p` de 1 a 8 passadas e `n` de 16 a 16384; menor `n` a partir do qual a base vence a híbrida. Se ela nunca vence, `p` fica fora da tabela. |

A calibração também repete o experimento da seção 5.1 (passada única contra
passadas nativas) e grava tudo em `resultados/calibracao.md`.

## 6. Cenários de medição

Gerados em `medicoes/cenarios.py`, sempre a partir de uma semente.

| Cenário | Função | Padrão |
|---|---|---|
| Aleatório com chaves grandes | `aleatorio_chaves_grandes(n, semente)` | n = 10 000, valores em [0, 10¹²) |
| Faixa estreita | `faixa_estreita(n, semente)` | n = 10 000, valores em [0, 100) |
| Quase ordenado | `quase_ordenado(n, semente, fracao=0.01)` | n = 10 000, valores em [0, 10¹²) ordenados; depois `fracao * n` trocas, cada uma entre a posição `i` e `i + d`, com `d` de 1 a 10 |
| Lista minúscula | `minuscula(n, semente)` | n = 8, valores em [0, 10⁶) |
| Extra (caso de erro) | `metades_trocadas(n, semente)` | n = 10 000: lista ordenada de chaves grandes com a segunda metade movida para a frente |

## 7. Metodologia de medição

- `medicoes/medir.py` mede os 6 métodos e o `ordenar` em cada cenário.
- Cada medição é repetida `R` vezes (padrão 5), e o relatório usa a **mediana**.
- O tempo é medido com `time.perf_counter_ns()` e o coletor de lixo fica desligado durante a medição.
- Lista minúscula: cada repetição ordena um lote de 2000 listas diferentes, e o tempo reportado é por lista.
- A semente é fixa (padrão 2026), inclusive a do `random` usado pelos pivôs.
- Se a contagem recusar a faixa (`FaixaGrandeDemais`), a célula da tabela mostra "recusou".
- O custo do `escolher` sozinho é medido em cada cenário e comparado com o tempo do `ordenar`.
- Também se mede a contagem com e sem `minimo`/`maximo` repassados, para mostrar quanto a reutilização economiza.

### Critério de "ganhar de qualquer escolha fixa"

Para cada método `m` e cenário `c`: `razao(m, c) = tempo(m, c) / menor tempo em c`
(o menor entre os 7 concorrentes). A **pior razão** de `m` é o máximo dessa razão
nos quatro cenários; "recusou" conta como infinito. O `ordenar` ganha se a pior
razão dele for menor que a de todos os métodos fixos. A tabela também traz a
média geométrica das razões.

## 8. Cenário de erro

No cenário extra `metades_trocadas` há só uma descida, então o `escolher`
aposta na inserção. Mas metade dos elementos precisa atravessar a outra metade,
o que dá cerca de n²/4 deslocamentos. O relatório mede o tamanho do erro e
explica por que contar descidas não enxerga desordem "longe".

## 9. Testes

`python3 -m unittest discover -s testes -t .`

- `testes/test_metodos.py`: os 6 métodos e o `ordenar` passam pelos casos lista
  vazia, um elemento, todos iguais (2000 elementos), já ordenada, invertida,
  só negativos, negativos e positivos misturados, aleatórias de vários tamanhos
  (comparadas com `sorted()`) e "não altera a entrada". Também testam a trava
  da contagem, `minimo`/`maximo` repassados, base com valores acima de 64 bits
  e `passadas()`.
- `testes/test_escolhedor.py`: cada regra é testada com listas montadas a partir
  das próprias constantes (para os testes continuarem válidos após uma
  recalibração). Também verifica que o `escolher` percorre a lista só uma vez,
  que devolve mínimo e máximo corretos e que nunca escolhe contagem com faixa
  acima do limite.

## 10. Saídas

- `resultados/calibracao.md`: tabelas de cada varredura e os limiares sugeridos.
- `resultados/medicoes.csv`: todos os tempos brutos (cenário, método, repetição, segundos).
- `resultados/tabela.md`: medianas, razões, vencedores, custo do `escolher` e cenário de erro, com a máquina e a versão do Python.

## 11. Fora do escopo

Ordenar no lugar, tipos além de inteiros, paralelismo e extensões em C.
