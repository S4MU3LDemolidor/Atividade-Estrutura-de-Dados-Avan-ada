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

# Limiares provisórios, até rodar a calibração.
N_MINUSCULA = 16
FRACAO_DESCIDAS = 0.05
FATOR_QUEDAS = 4.0
FATOR_CONTAGEM = 2.0
N_MIN_BASE = {1: 64, 2: 128, 3: 256, 4: 512, 5: 1024, 6: 2048, 7: 4096, 8: 8192}

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
