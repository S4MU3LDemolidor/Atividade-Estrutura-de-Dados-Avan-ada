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
```

## Requisitos

Python 3.10 ou mais novo. Usa só a biblioteca padrão, não precisa instalar nada.

## Como rodar

Em construção. Os comandos para rodar os testes e refazer as medições entram
aqui conforme cada parte for implementada.

## Relatório

Ver [RELATORIO.md](RELATORIO.md).
