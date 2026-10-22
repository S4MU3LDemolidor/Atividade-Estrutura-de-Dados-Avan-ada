"""Escolhe o método de ordenação mais adequado para uma lista.

escolher(v) percorre a lista uma única vez e olha o tamanho, o mínimo, o máximo
e quantas vezes um elemento é maior que o seguinte (descidas). Com isso aplica
regras cujos limiares saem das medições de medicoes/calibrar.py.
"""

from typing import NamedTuple


class Escolha(NamedTuple):
    """Resultado do escolher.

    minimo e maximo vão junto para que contagem e base não precisem percorrer a
    lista de novo.
    """

    metodo: str
    minimo: int | None
    maximo: int | None


def escolher(v: list[int]) -> Escolha:
    """Olha a lista e devolve o método mais adequado para ordená-la."""
    raise NotImplementedError


def ordenar(v: list[int]) -> list[int]:
    """Chama escolher(v) e executa o método escolhido."""
    raise NotImplementedError
