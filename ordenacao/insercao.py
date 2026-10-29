"""Ordenação por inserção."""


def insercao_intervalo(a: list[int], ini: int, fim: int) -> None:
    """Ordena a[ini..fim] (fim incluso) no próprio lugar.

    Também é usada pela híbrida para terminar as sublistas pequenas.
    """
    for i in range(ini + 1, fim + 1):
        x = a[i]
        j = i - 1
        while j >= ini and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


def insercao(v: list[int]) -> list[int]:
    """Devolve uma nova lista com os elementos de v em ordem crescente.

    Não altera v.
    """
    a = list(v)
    insercao_intervalo(a, 0, len(a) - 1)
    return a
