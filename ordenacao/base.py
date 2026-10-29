"""Ordenação por base (radix sort LSD) em base 256.

Os valores são deslocados pelo mínimo para que todos fiquem não negativos.
O número de passadas é a quantidade de bytes necessária para representar
maximo - minimo.
"""

BITS_POR_DIGITO = 8
BALDES = 1 << BITS_POR_DIGITO  # 256
MASCARA = BALDES - 1


def passadas(faixa: int) -> int:
    """Quantas passadas a base faz para uma faixa maximo - minimo."""
    return (faixa.bit_length() + BITS_POR_DIGITO - 1) // BITS_POR_DIGITO


def base(v: list[int], minimo: int | None = None, maximo: int | None = None) -> list[int]:
    """Devolve uma nova lista com os elementos de v em ordem crescente.

    Aceita valores negativos. Se minimo e maximo já forem conhecidos, podem ser
    passados para não percorrer a lista de novo; eles precisam ser o mínimo e o
    máximo verdadeiros de v, senão o resultado sai fora de ordem. Não altera v.
    """
    if not v:
        return []
    if minimo is None or maximo is None:
        minimo, maximo = min(v), max(v)

    a = [x - minimo for x in v]
    deslocamento = 0
    for _ in range(passadas(maximo - minimo)):
        baldes = [[] for _ in range(BALDES)]
        for x in a:
            baldes[(x >> deslocamento) & MASCARA].append(x)
        a = [x for balde in baldes for x in balde]
        deslocamento += BITS_POR_DIGITO
    return [x + minimo for x in a]
