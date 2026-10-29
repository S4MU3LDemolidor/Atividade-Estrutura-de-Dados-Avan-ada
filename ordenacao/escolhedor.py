"""Escolhe o método de ordenação mais adequado para uma lista.

escolher(v) percorre a lista uma única vez e olha o tamanho, o mínimo, o máximo,
quantas vezes um elemento é maior que o seguinte (descidas) e a soma dessas
diferenças (quedas). Com isso aplica regras cujos limiares saem das medições de
medicoes/calibrar.py.
"""

import math
from typing import NamedTuple

from ordenacao.base import base, passadas
from ordenacao.contagem import LIMITE_CONTADORES, contagem
from ordenacao.hibrida import hibrida
from ordenacao.insercao import insercao
from ordenacao.intercalacao import intercalacao
from ordenacao.rapida import rapida

# Limiares tirados de resultados/calibracao.md (python3 -m medicoes.calibrar).

# Até esse tamanho a inserção vence todos os outros métodos.
N_MINUSCULA = 24
# Metade da maior fração de descidas em que a inserção ainda venceu (desordem local).
FRACAO_DESCIDAS = 0.228
# Metade do maior quedas/amplitude em que a inserção ainda venceu (desordem longe).
FATOR_QUEDAS = 3.38
# Maior razão faixa/n em que a contagem ainda venceu a base e a híbrida.
FATOR_CONTAGEM = 2
# Para cada número de passadas da base, o menor n a partir do qual ela vence a híbrida.
N_MIN_BASE = {1: 64, 2: 256, 3: 256, 4: 512, 5: 512, 6: 1024,
              7: 1024, 8: 2048, 9: 2048, 10: 2048, 11: 4096, 12: 8192}

METODOS = {
    "insercao": insercao,
    "intercalacao": intercalacao,
    "rapida": rapida,
    "hibrida": hibrida,
    "contagem": contagem,
    "base": base,
}
USAM_FAIXA = {"contagem", "base"}


class Escolha(NamedTuple):
    """Resultado do escolher.

    minimo e maximo vão junto para que contagem e base não precisem percorrer a
    lista de novo.
    """

    metodo: str
    minimo: int | None
    maximo: int | None


class Perfil(NamedTuple):
    """O que a passada única descobre sobre a lista."""

    minimo: int
    maximo: int
    descidas: int  # posições com v[i] > v[i+1]
    quedas: int    # soma de v[i] - v[i+1] nessas posições


def perfil(v: list[int]) -> Perfil:
    """Percorre a lista (não vazia) uma única vez e devolve o seu Perfil.

    Um novo mínimo é sempre uma descida (x < anterior) e um novo máximo nunca
    é, então cada elemento custa só duas comparações na maior parte das vezes.
    """
    minimo = maximo = anterior = v[0]
    descidas = 0
    quedas = 0
    for x in v:
        if x < anterior:
            descidas += 1
            quedas += anterior - x
            if x < minimo:
                minimo = x
        elif x > maximo:
            maximo = x
        anterior = x
    return Perfil(minimo, maximo, descidas, quedas)


def escolher(v: list[int]) -> Escolha:
    """Olha a lista e devolve o método mais adequado para ordená-la."""
    n = len(v)
    if n < 2 or n <= N_MINUSCULA:
        return Escolha("insercao", None, None)

    minimo, maximo, descidas, quedas = perfil(v)
    amplitude = maximo - minimo

    # quedas / amplitude estima quantas posições, em média, cada elemento anda
    # na inserção. As descidas barram listas desordenadas com um valor extremo,
    # que infla a amplitude e esconde as quedas.
    if descidas <= FRACAO_DESCIDAS * n and quedas <= FATOR_QUEDAS * amplitude:
        metodo = "insercao"
    elif amplitude + 1 <= LIMITE_CONTADORES and amplitude + 1 <= FATOR_CONTAGEM * n:
        metodo = "contagem"
    elif n >= N_MIN_BASE.get(passadas(amplitude), math.inf):
        metodo = "base"
    else:
        metodo = "hibrida"
    return Escolha(metodo, minimo, maximo)


def ordenar(v: list[int]) -> list[int]:
    """Chama escolher(v) e executa o método escolhido."""
    escolha = escolher(v)
    metodo = METODOS[escolha.metodo]
    if escolha.metodo in USAM_FAIXA:
        return metodo(v, escolha.minimo, escolha.maximo)
    return metodo(v)
