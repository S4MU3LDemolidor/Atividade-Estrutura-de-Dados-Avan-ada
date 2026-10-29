# Ordenação adaptativa

Trabalho de Estrutura de Dados. Nenhum método de ordenação ganha sempre, então a
ideia é construir um `ordenar(v)` que olha a lista, decide sozinho qual método
usar e, nas medições, se sai melhor que qualquer escolha fixa.

## Dupla

- Samuel Ribeiro Cardoso
- Pedro Augusto

## Métodos

| Método | Arquivo |
|---|---|
| Inserção | `ordenacao/insercao.py` |
| Intercalação (merge sort) | `ordenacao/intercalacao.py` |
| Rápida com pivô aleatório | `ordenacao/rapida.py` |
| Híbrida (rápida + inserção) | `ordenacao/hibrida.py` |
| Contagem | `ordenacao/contagem.py` |
| Base (radix LSD) | `ordenacao/base.py` |

O escolhedor (`escolher` e `ordenar`) fica em `ordenacao/escolhedor.py`.

## Estrutura

```
ordenacao/   métodos de ordenação e o escolhedor
medicoes/    geração dos cenários, calibração dos limiares e medição final
resultados/  tabelas e CSVs gerados pelas medições
testes/      testes automatizados (unittest)
docs/        especificação (spec.md) e plano de implementação (plano.md)
```

O projeto foi feito orientado por especificação: primeiro `docs/spec.md`,
depois `docs/plano.md`, e só então o código, sempre com o teste escrito antes da
implementação. O histórico de commits segue essa ordem.

## Requisitos

Python 3.10 ou mais novo. Usa só a biblioteca padrão, não precisa instalar nada.
Todos os comandos abaixo são rodados na pasta do projeto.

## Como rodar

### Testes

```bash
python3 -m unittest discover -s testes -t .
```

São 125 testes e levam menos de 1 segundo. Os seis métodos e o `ordenar` passam
pelos mesmos casos: lista vazia, um elemento, todos iguais, já ordenada,
invertida, valores negativos, muitos repetidos e listas aleatórias comparadas
com `sorted()`. Há também testes de cada regra do `escolher`.

### Usar o `ordenar`

```python
from ordenacao.escolhedor import escolher, ordenar

ordenar([5, -1, 3, 3])             # [-1, 3, 3, 5]
escolher(list(range(1000))).metodo  # 'insercao'
```

### Refazer as medições

São dois passos. A calibração vem antes porque é ela que define os limiares
usados pelo `escolher`.

**1. Calibração (cerca de 25 segundos)**

```bash
python3 -m medicoes.calibrar
```

Grava as varreduras em `resultados/calibracao.md` e imprime os limiares
sugeridos. Se algum mudar, copie o valor para `ordenacao/escolhedor.py` (ou
`CORTE` em `ordenacao/hibrida.py`) e rode os testes de novo.

**2. Medição final (cerca de 15 segundos)**

```bash
python3 -m medicoes.medir
```

Mede os quatro cenários contra os seis métodos e o `ordenar`, e também o custo
do `escolher` e o cenário em que ele erra. Grava as tabelas em
`resultados/tabela.md` e todos os tempos brutos em `resultados/medicoes.csv`.
As opções `--n` (padrão 10000), `--repeticoes` (padrão 5) e `--semente` (padrão
2026) mudam o tamanho das listas, o número de repetições e a semente. Com a
mesma semente as listas geradas são sempre as mesmas.

### Dicas para medir

- Os tempos absolutos dependem da máquina. O que deve se repetir em outra
  máquina são as razões entre os métodos e quem vence cada cenário.
- Feche programas pesados antes de medir. Cada medição é repetida de forma
  intercalada entre os métodos, e vale o menor tempo, o que já protege contra
  interferências passageiras.
- Se `resultados/tabela.md` começar com um aviso de **Atenção**, houve
  interferência (por exemplo, o sistema trocou o processo de núcleo). Basta
  rodar de novo.

## Relatório

Ver [RELATORIO.md](RELATORIO.md).
