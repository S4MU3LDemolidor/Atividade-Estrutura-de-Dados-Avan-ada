"""Ordenação rápida (quicksort) com pivô aleatório.

A partição é feita em três vias (menores, iguais e maiores que o pivô) para não
degradar quando há muitos valores repetidos. A recursão vai sempre para a parte
menor e a maior é tratada num laço, o que mantém a profundidade em O(log n).
"""


def rapida(v: list[int]) -> list[int]:
    """Devolve uma nova lista com os elementos de v em ordem crescente.

    Não altera v.
    """
    raise NotImplementedError
