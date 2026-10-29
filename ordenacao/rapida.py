"""Ordenação rápida (quicksort) com pivô aleatório.

A partição é feita em três vias (menores, iguais e maiores que o pivô) para não
degradar quando há muitos valores repetidos. A recursão vai sempre para a parte
menor e a maior é tratada num laço, o que mantém a profundidade em O(log n).
"""

import random


def rapida(v: list[int]) -> list[int]:
    """Devolve uma nova lista com os elementos de v em ordem crescente.

    Não altera v.
    """
    a = list(v)
    _ordenar(a, 0, len(a) - 1)
    return a


def particionar(a: list[int], ini: int, fim: int) -> tuple[int, int]:
    """Particiona a[ini..fim] em torno de um pivô sorteado (Dijkstra).

    Devolve (menor, maior) tais que a[ini..menor-1] < pivô,
    a[menor..maior] == pivô e a[maior+1..fim] > pivô.
    """
    p = random.randint(ini, fim)
    a[ini], a[p] = a[p], a[ini]
    pivo = a[ini]
    menor, i, maior = ini, ini + 1, fim
    while i <= maior:
        x = a[i]
        if x < pivo:
            a[i] = a[menor]
            a[menor] = x
            menor += 1
            i += 1
        elif x > pivo:
            a[i] = a[maior]
            a[maior] = x
            maior -= 1
        else:
            i += 1
    return menor, maior


def _ordenar(a: list[int], ini: int, fim: int) -> None:
    while ini < fim:
        menor, maior = particionar(a, ini, fim)
        if menor - ini < fim - maior:
            _ordenar(a, ini, menor - 1)
            ini = maior + 1
        else:
            _ordenar(a, maior + 1, fim)
            fim = menor - 1
