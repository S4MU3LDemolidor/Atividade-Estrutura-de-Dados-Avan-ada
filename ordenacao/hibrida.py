"""Ordenação híbrida: rápida com pivô aleatório + inserção.

Funciona como a rápida, mas quando uma sublista fica pequena (até CORTE
elementos) ela é ordenada por inserção. O valor de CORTE sai da calibração
feita em medicoes/calibrar.py.
"""


def hibrida(v: list[int]) -> list[int]:
    """Devolve uma nova lista com os elementos de v em ordem crescente.

    Não altera v.
    """
    raise NotImplementedError
