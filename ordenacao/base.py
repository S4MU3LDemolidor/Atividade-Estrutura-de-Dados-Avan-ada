"""Ordenação por base (radix sort LSD) em base 256.

Os valores são deslocados pelo mínimo para que todos fiquem não negativos.
O número de passadas é a quantidade de bytes necessária para representar
maximo - minimo.
"""


def base(v: list[int], minimo: int | None = None, maximo: int | None = None) -> list[int]:
    """Devolve uma nova lista com os elementos de v em ordem crescente.

    Aceita valores negativos. Se minimo e maximo já forem conhecidos, podem ser
    passados para não percorrer a lista de novo. Não altera v.
    """
    raise NotImplementedError
