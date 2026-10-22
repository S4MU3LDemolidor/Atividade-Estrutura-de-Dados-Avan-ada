"""Ordenação por contagem.

Aloca um contador para cada valor entre o mínimo e o máximo da lista, então a
memória cresce com a faixa de valores e não com o tamanho da lista. Para não
estourar a memória, recusa faixas maiores que LIMITE_CONTADORES.
"""

LIMITE_CONTADORES = 10_000_000


class FaixaGrandeDemais(ValueError):
    """A faixa de valores da lista exigiria contadores demais."""


def contagem(v: list[int], minimo: int | None = None, maximo: int | None = None) -> list[int]:
    """Devolve uma nova lista com os elementos de v em ordem crescente.

    Aceita valores negativos (os índices são deslocados pelo mínimo). Se minimo
    e maximo já forem conhecidos, podem ser passados para não percorrer a lista
    de novo. Lança FaixaGrandeDemais se maximo - minimo + 1 passar de
    LIMITE_CONTADORES. Não altera v.
    """
    raise NotImplementedError
