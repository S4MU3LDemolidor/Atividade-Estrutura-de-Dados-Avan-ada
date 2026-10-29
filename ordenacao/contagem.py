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
    de novo; eles precisam ser o mínimo e o máximo verdadeiros de v (valores
    errados dão resultado errado ou IndexError). Lança FaixaGrandeDemais se
    maximo - minimo + 1 passar de LIMITE_CONTADORES. Não altera v.
    """
    if not v:
        return []
    if minimo is None or maximo is None:
        minimo, maximo = min(v), max(v)

    faixa = maximo - minimo + 1
    if faixa > LIMITE_CONTADORES:
        raise FaixaGrandeDemais(
            f"a faixa {minimo}..{maximo} precisaria de {faixa} contadores "
            f"(limite: {LIMITE_CONTADORES})"
        )

    contadores = [0] * faixa
    for x in v:
        contadores[x - minimo] += 1

    saida = []
    for deslocado, quantidade in enumerate(contadores):
        if quantidade:
            saida.extend([deslocado + minimo] * quantidade)
    return saida
