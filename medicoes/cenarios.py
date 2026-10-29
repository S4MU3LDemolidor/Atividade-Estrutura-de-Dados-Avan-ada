"""Geradores das listas usadas nas medições.

Todos recebem uma semente para que as medições possam ser refeitas com
exatamente as mesmas listas.
"""

import random

CHAVE_GRANDE = 10**12   # valores em [0, 10^12): 40 bits, 5 passadas da base
FAIXA_ESTREITA = 100    # valores em [0, 100)
CHAVE_MINUSCULA = 10**6


def aleatorio_chaves_grandes(n: int, semente: int) -> list[int]:
    """Valores aleatórios espalhados numa faixa muito maior que n."""
    gerador = random.Random(semente)
    return [gerador.randrange(CHAVE_GRANDE) for _ in range(n)]


def faixa_estreita(n: int, semente: int) -> list[int]:
    """Valores aleatórios numa faixa pequena, com muitas repetições."""
    gerador = random.Random(semente)
    return [gerador.randrange(FAIXA_ESTREITA) for _ in range(n)]


def quase_ordenado(n: int, semente: int, fracao: float = 0.01, distancia: int = 10) -> list[int]:
    """Lista ordenada com uma pequena parte dos elementos fora do lugar.

    Parte de chaves grandes já ordenadas e faz fracao * n trocas, cada uma entre
    uma posição i e outra até `distancia` posições à frente. A desordem é
    local: nenhum elemento fica longe do seu lugar.
    """
    gerador = random.Random(semente)
    v = sorted(gerador.randrange(CHAVE_GRANDE) for _ in range(n))
    for _ in range(int(fracao * n)):
        i = gerador.randrange(n)
        j = min(n - 1, i + gerador.randint(1, distancia))
        v[i], v[j] = v[j], v[i]
    return v


def minuscula(n: int, semente: int) -> list[int]:
    """Lista aleatória com poucos elementos."""
    gerador = random.Random(semente)
    return [gerador.randrange(CHAVE_MINUSCULA) for _ in range(n)]


def lote_minusculas(quantidade: int, n: int, semente: int) -> list[list[int]]:
    """Várias listas minúsculas diferentes, para medir em lote."""
    gerador = random.Random(semente)
    return [[gerador.randrange(CHAVE_MINUSCULA) for _ in range(n)] for _ in range(quantidade)]


def metades_trocadas(n: int, semente: int) -> list[int]:
    """Chaves grandes ordenadas com a segunda metade movida para a frente.

    Tem uma única descida, mas metade dos elementos está longe do seu lugar.
    É o cenário em que o escolhedor erra.
    """
    v = sorted(aleatorio_chaves_grandes(n, semente))
    meio = n // 2
    return v[meio:] + v[:meio]
