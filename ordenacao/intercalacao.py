"""Ordenação por intercalação (merge sort)."""


def intercalacao(v: list[int]) -> list[int]:
    """Devolve uma nova lista com os elementos de v em ordem crescente.

    Não altera v.
    """
    a = list(v)
    aux = [0] * len(a)
    _ordenar(a, aux, 0, len(a))
    return a


def _ordenar(a: list[int], aux: list[int], ini: int, fim: int) -> None:
    """Ordena a[ini:fim] (fim exclusivo)."""
    if fim - ini < 2:
        return
    meio = (ini + fim) // 2
    _ordenar(a, aux, ini, meio)
    _ordenar(a, aux, meio, fim)
    _intercalar(a, aux, ini, meio, fim)


def _intercalar(a: list[int], aux: list[int], ini: int, meio: int, fim: int) -> None:
    """Junta as metades ordenadas a[ini:meio] e a[meio:fim].

    Em caso de empate pega da esquerda, o que mantém a ordenação estável.
    """
    aux[ini:fim] = a[ini:fim]
    i, j = ini, meio
    for k in range(ini, fim):
        if j >= fim or (i < meio and aux[i] <= aux[j]):
            a[k] = aux[i]
            i += 1
        else:
            a[k] = aux[j]
            j += 1
