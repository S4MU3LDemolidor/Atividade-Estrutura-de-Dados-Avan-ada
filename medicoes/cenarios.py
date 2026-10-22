"""Geradores das listas usadas nas medições.

Todos recebem uma semente para que as medições possam ser refeitas com
exatamente as mesmas listas.
"""


def aleatorio_chaves_grandes(n: int, semente: int) -> list[int]:
    """Valores aleatórios espalhados numa faixa muito maior que n."""
    raise NotImplementedError


def faixa_estreita(n: int, semente: int) -> list[int]:
    """Valores aleatórios numa faixa pequena, com muitas repetições."""
    raise NotImplementedError


def quase_ordenado(n: int, semente: int) -> list[int]:
    """Lista ordenada com uma pequena parte dos elementos fora do lugar."""
    raise NotImplementedError


def minuscula(n: int, semente: int) -> list[int]:
    """Lista aleatória com poucos elementos."""
    raise NotImplementedError
