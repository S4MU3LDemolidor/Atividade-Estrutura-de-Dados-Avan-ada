"""Ordenação híbrida: rápida com pivô aleatório + inserção.

Funciona como a rápida, mas quando uma sublista fica pequena (até CORTE
elementos) ela é ordenada por inserção. O valor de CORTE sai da calibração
feita em medicoes/calibrar.py.
"""

from ordenacao.insercao import insercao_intervalo
from ordenacao.rapida import particionar

CORTE = 16  # provisório, até rodar a calibração


def hibrida(v: list[int], corte: int = CORTE) -> list[int]:
    """Devolve uma nova lista com os elementos de v em ordem crescente.

    Sublistas com até `corte` elementos são terminadas por inserção.
    Não altera v.
    """
    a = list(v)
    _ordenar(a, 0, len(a) - 1, corte)
    return a


def _ordenar(a: list[int], ini: int, fim: int, corte: int) -> None:
    while fim - ini + 1 > corte:
        menor, maior = particionar(a, ini, fim)
        if menor - ini < fim - maior:
            _ordenar(a, ini, menor - 1, corte)
            ini = maior + 1
        else:
            _ordenar(a, maior + 1, fim, corte)
            fim = menor - 1
    insercao_intervalo(a, ini, fim)
