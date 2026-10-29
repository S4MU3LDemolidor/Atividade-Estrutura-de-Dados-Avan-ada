# Plano de implementação

Segue a especificação em [spec.md](spec.md). Cada tarefa é feita com testes
primeiro: escrever o teste, ver falhar, implementar, ver passar e commitar.

Comando dos testes (usado em todas as tarefas):

```bash
python3 -m unittest discover -s testes -t .
```

## Tarefa 1: Inserção

**Arquivos:** `ordenacao/insercao.py`, `testes/test_metodos.py`

1. Criar em `testes/test_metodos.py` a classe `CasosComuns`, com os testes que
   valem para todo método: vazia, um elemento, todos iguais (2000), já
   ordenada, invertida, só negativos, negativos e positivos, aleatórias de
   tamanhos 2, 10, 100 e 1000 com três sementes (comparadas com `sorted()`),
   muitos repetidos e "não altera a entrada".
2. Criar `TestInsercao(CasosComuns, unittest.TestCase)` com `metodo = staticmethod(insercao)`.
3. Rodar os testes: falham com `NotImplementedError`.
4. Implementar `insercao_intervalo(a, ini, fim)` (ordena `a[ini..fim]` no lugar)
   e `insercao(v)`, que copia `v` e chama `insercao_intervalo(a, 0, len(a) - 1)`.
5. Rodar os testes: passam.
6. Commit: `Ordenação por inserção com testes`

## Tarefa 2: Intercalação

**Arquivos:** `ordenacao/intercalacao.py`, `testes/test_metodos.py`

1. Adicionar `TestIntercalacao(CasosComuns, unittest.TestCase)`.
2. Rodar: falha.
3. Implementar de cima para baixo em intervalos `[ini, fim)`, com um único vetor
   auxiliar; `_intercalar` copia o trecho para o auxiliar e intercala de volta,
   pegando da esquerda em caso de empate (estável).
4. Rodar: passa.
5. Commit: `Ordenação por intercalação`

## Tarefa 3: Rápida com pivô aleatório

**Arquivos:** `ordenacao/rapida.py`, `testes/test_metodos.py`

1. Adicionar `TestRapida(CasosComuns, unittest.TestCase)` e um teste de
   `particionar`: depois da chamada, `a[ini..menor-1] < pivô`,
   `a[menor..maior] == pivô` e `a[maior+1..fim] > pivô`.
2. Rodar: falha.
3. Implementar `particionar(a, ini, fim)` (Dijkstra, pivô `random.randint(ini, fim)`
   levado para `a[ini]`), devolvendo `(menor, maior)`. Implementar `_ordenar`
   com recursão na parte menor e laço na maior.
4. Rodar: passa (inclusive "todos iguais" com 2000 elementos, sem estourar a recursão).
5. Commit: `Ordenação rápida com pivô aleatório e partição em três vias`

## Tarefa 4: Híbrida

**Arquivos:** `ordenacao/hibrida.py`, `testes/test_metodos.py`

1. Adicionar `TestHibrida(CasosComuns, unittest.TestCase)` e testes com
   `corte=1` e `corte=64` em listas aleatórias de 500.
2. Rodar: falha.
3. Implementar `hibrida(v, corte=CORTE)` usando `rapida.particionar` e
   `insercao.insercao_intervalo`. `CORTE = 16` provisório até a calibração.
4. Rodar: passa.
5. Commit: `Ordenação híbrida (rápida + inserção)`

## Tarefa 5: Contagem

**Arquivos:** `ordenacao/contagem.py`, `testes/test_metodos.py`

1. Adicionar `TestContagem(CasosComuns, unittest.TestCase)` e testes:
   `[0, 10**12]` lança `FaixaGrandeDemais` (tem que ser instantâneo, sem
   alocar); faixa exatamente igual a `LIMITE_CONTADORES` não lança (testar
   alterando o limite do módulo para um valor pequeno); `minimo`/`maximo`
   repassados dão o mesmo resultado.
2. Rodar: falha.
3. Implementar: calcula `min()`/`max()` se não vierem, verifica a faixa antes de
   alocar, conta deslocando pelo mínimo e reconstrói a saída.
4. Rodar: passa.
5. Commit: `Ordenação por contagem com trava de memória`

## Tarefa 6: Base

**Arquivos:** `ordenacao/base.py`, `testes/test_metodos.py`

1. Adicionar `TestBase(CasosComuns, unittest.TestCase)` e testes: valores perto
   de `2**70` e `-2**70`; `passadas(0) == 0`, `passadas(255) == 1`,
   `passadas(256) == 2`, `passadas(2**64 - 1) == 8`; `minimo`/`maximo` repassados.
2. Rodar: falha.
3. Implementar `passadas(faixa)` e o radix LSD em base 256 sobre `x - minimo`.
4. Rodar: passa.
5. Commit: `Ordenação por base (radix LSD)`

## Tarefa 7: Cenários

**Arquivos:** `medicoes/cenarios.py`, `testes/test_cenarios.py`

1. Testes: cada gerador devolve `n` elementos, é determinístico para a mesma
   semente, respeita a faixa; `quase_ordenado` tem poucas descidas;
   `metades_trocadas` tem exatamente uma descida.
2. Rodar: falha.
3. Implementar os cinco geradores com `random.Random(semente)`.
4. Rodar: passa.
5. Commit: `Geradores dos cenários de medição`

## Tarefa 8: Escolhedor

**Arquivos:** `ordenacao/escolhedor.py`, `testes/test_escolhedor.py`, `testes/test_metodos.py`

1. Testes das regras, montando listas a partir das constantes do módulo:
   - vazia, um elemento e `N_MINUSCULA` elementos → inserção, com `minimo is None`;
   - lista grande ordenada e quase ordenada → inserção;
   - faixa estreita (k pequeno, desordenada) → contagem, com mínimo e máximo corretos;
   - faixa acima de `LIMITE_CONTADORES` → nunca contagem;
   - `p` passadas com `n >= N_MIN_BASE[p]` e desordenada → base;
   - faixa de 2**100 → híbrida;
   - `escolher` itera a lista uma única vez (subclasse de `list` que conta `__iter__`).
2. Adicionar `TestOrdenar(CasosComuns, unittest.TestCase)` em `test_metodos.py`.
3. Rodar: falha.
4. Implementar a passada única, as regras da spec (seção 5.2) com limiares
   provisórios e `ordenar` com o dicionário `METODOS`.
5. Rodar: passa.
6. Commit: `Escolhedor e ordenar com limiares provisórios`

## Tarefa 9: Calibração

**Arquivos:** `medicoes/calibrar.py`, `medicoes/tempo.py`, `resultados/calibracao.md`, `ordenacao/escolhedor.py`, `ordenacao/hibrida.py`

1. Criar `medicoes/tempo.py` com `mediana_segundos(funcao, entrada, repeticoes)`
   e `mediana_lote(funcao, lote, repeticoes)` (GC desligado, `perf_counter_ns`).
   Os dois scripts de medição usam esse módulo.
2. Implementar as varreduras da spec (seção 5.3) e o experimento das passadas;
   o script grava `resultados/calibracao.md` e imprime os limiares sugeridos.
3. Rodar `python3 -m medicoes.calibrar`.
4. Commit: `Script de calibração e resultados`
5. Copiar os limiares para `escolhedor.py` e `hibrida.py`, com comentário
   apontando a calibração; rodar os testes.
6. Commit: `Limiares do escolhedor definidos pela calibração`

## Tarefa 10: Medição final

**Arquivos:** `medicoes/medir.py`, `resultados/medicoes.csv`, `resultados/tabela.md`

1. Implementar: 4 cenários × 7 concorrentes, cenário extra, custo do
   `escolher`, contagem com e sem mínimo/máximo, pior razão e média geométrica.
   Opções `--n`, `--repeticoes` e `--semente`.
2. Rodar `python3 -m medicoes.medir`.
3. Commit: `Medição final dos cenários`

## Tarefa 11: README

1. Preencher "Como rodar": testes, calibração e medição, com tempo aproximado de cada um.
2. Commit: `README: como rodar testes e refazer as medições`

## Tarefa 12: Relatório

1. Escrever as seis seções do `RELATORIO.md` a partir de `resultados/`.
2. Commit: `Relatório com resultados e análise`

## Tarefa 13: Revisão final

1. Rodar todos os testes e conferir que os números do relatório batem com `resultados/`.
2. Corrigir o que aparecer, em commits separados.
