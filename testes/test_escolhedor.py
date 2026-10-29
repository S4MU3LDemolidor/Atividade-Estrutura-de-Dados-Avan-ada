"""Testes das regras do escolher.

As listas são montadas a partir das constantes do próprio escolhedor, então os
testes continuam valendo depois de uma nova calibração.
"""

import math
import random
import unittest
from unittest import mock

from ordenacao import escolhedor
from ordenacao.base import passadas
from ordenacao.contagem import LIMITE_CONTADORES
from ordenacao.escolhedor import escolher, ordenar

CHAVE_GRANDE = 10**12


def aleatoria(n, faixa, semente=1):
    """Lista desordenada com valores em [0, faixa), incluindo os dois extremos."""
    gerador = random.Random(semente)
    v = [gerador.randrange(faixa) for _ in range(n - 2)] + [0, faixa - 1]
    gerador.shuffle(v)
    return v


def com_descidas(n, quantidade):
    """Lista crescente de chaves grandes com exatamente `quantidade` descidas.

    Troca pares vizinhos (0,1), (2,3), ...; cada troca cria uma descida só.
    """
    v = [CHAVE_GRANDE + 7 * i for i in range(n)]
    for t in range(quantidade):
        i = 2 * t
        v[i], v[i + 1] = v[i + 1], v[i]
    return v


def trocas_longe(n, trocas):
    """Lista crescente com `trocas` trocas entre as posições i e i + n/2.

    As trocas ficam espaçadas, então cada uma desloca dois elementos por n/2
    posições e soma quase uma amplitude inteira às quedas.
    """
    v = [CHAVE_GRANDE + 7 * i for i in range(n)]
    for t in range(trocas):
        i = 3 * t
        j = i + n // 2
        v[i], v[j] = v[j], v[i]
    return v


class ContaAcessos(list):
    """Lista que conta quantas vezes foi percorrida ou indexada."""

    def __init__(self, *args):
        super().__init__(*args)
        self.iteracoes = 0
        self.indexacoes = 0

    def __iter__(self):
        self.iteracoes += 1
        return super().__iter__()

    def __getitem__(self, i):
        self.indexacoes += 1
        return super().__getitem__(i)


class TestListasMinusculas(unittest.TestCase):
    def test_vazia_e_um_elemento(self):
        self.assertEqual(escolher([]).metodo, "insercao")
        self.assertEqual(escolher([3]).metodo, "insercao")

    def test_ate_n_minuscula_vai_para_insercao_sem_olhar(self):
        v = ContaAcessos(aleatoria(escolhedor.N_MINUSCULA, CHAVE_GRANDE))
        escolha = escolher(v)
        self.assertEqual(escolha.metodo, "insercao")
        self.assertIsNone(escolha.minimo)
        self.assertEqual(v.iteracoes + v.indexacoes, 0)


class TestQuaseOrdenada(unittest.TestCase):
    n = 4000

    def test_limiar_menor_que_lista_aleatoria(self):
        # uma lista aleatória tem perto de n/2 descidas
        self.assertLess(escolhedor.FRACAO_DESCIDAS, 0.5)

    def test_ordenada_vai_para_insercao(self):
        self.assertEqual(escolher(com_descidas(self.n, 0)).metodo, "insercao")

    def test_no_limiar_vai_para_insercao(self):
        limite = math.floor(escolhedor.FRACAO_DESCIDAS * self.n)
        self.assertEqual(escolher(com_descidas(self.n, limite)).metodo, "insercao")

    def test_acima_do_limiar_nao_vai_para_insercao(self):
        limite = math.floor(escolhedor.FRACAO_DESCIDAS * self.n)
        self.assertNotEqual(escolher(com_descidas(self.n, limite + 1)).metodo, "insercao")

    def test_trocas_longe_ate_o_fator_vao_para_insercao(self):
        trocas = math.floor(escolhedor.FATOR_QUEDAS)
        if trocas == 0:
            self.skipTest("FATOR_QUEDAS < 1")
        self.assertEqual(escolher(trocas_longe(self.n, trocas)).metodo, "insercao")

    def test_trocas_longe_acima_do_fator_nao_vao_para_insercao(self):
        trocas = math.floor(escolhedor.FATOR_QUEDAS) + 2
        # poucas descidas: quem decide aqui são as quedas
        self.assertLessEqual(2 * trocas, escolhedor.FRACAO_DESCIDAS * self.n)
        self.assertNotEqual(escolher(trocas_longe(self.n, trocas)).metodo, "insercao")

    def test_valor_extremo_isolado_nao_engana(self):
        # o extremo infla a amplitude e deixa as quedas pequenas; as descidas barram
        gerador = random.Random(4)
        v = [gerador.randrange(1000) for _ in range(self.n)] + [CHAVE_GRANDE]
        self.assertNotEqual(escolher(v).metodo, "insercao")


class TestFaixaEstreita(unittest.TestCase):
    n = 5000

    def test_faixa_no_limiar_vai_para_contagem(self):
        faixa = math.floor(escolhedor.FATOR_CONTAGEM * self.n)
        escolha = escolher(aleatoria(self.n, faixa))
        self.assertEqual(escolha, ("contagem", 0, faixa - 1))

    def test_faixa_acima_do_limiar_nao_vai_para_contagem(self):
        faixa = math.floor(escolhedor.FATOR_CONTAGEM * self.n) + 1
        self.assertNotEqual(escolher(aleatoria(self.n, faixa)).metodo, "contagem")

    def test_faixa_acima_do_limite_de_memoria_nunca_vai_para_contagem(self):
        v = aleatoria(1000, LIMITE_CONTADORES + 1)
        with mock.patch.object(escolhedor, "FATOR_CONTAGEM", 10**9):
            self.assertNotEqual(escolher(v).metodo, "contagem")
            self.assertEqual(escolher(aleatoria(1000, LIMITE_CONTADORES)).metodo, "contagem")


class TestBaseEHibrida(unittest.TestCase):
    def test_base_a_partir_do_tamanho_minimo(self):
        self.assertTrue(escolhedor.N_MIN_BASE)
        for p, n_min in escolhedor.N_MIN_BASE.items():
            faixa = 256**p
            n = max(n_min, escolhedor.N_MINUSCULA + 1)
            if faixa <= escolhedor.FATOR_CONTAGEM * n and faixa <= LIMITE_CONTADORES:
                continue  # a contagem vem antes
            with self.subTest(passadas=p):
                self.assertEqual(passadas(faixa - 1), p)
                self.assertEqual(escolher(aleatoria(n, faixa)).metodo, "base")
                if n - 1 > escolhedor.N_MINUSCULA and n == n_min:
                    self.assertEqual(escolher(aleatoria(n - 1, faixa)).metodo, "hibrida")

    def test_faixa_enorme_vai_para_hibrida(self):
        self.assertEqual(escolher(aleatoria(2000, 2**100)).metodo, "hibrida")


class TestPassadaUnica(unittest.TestCase):
    def test_percorre_a_lista_uma_vez(self):
        v = ContaAcessos(aleatoria(3000, CHAVE_GRANDE))
        escolher(v)
        self.assertEqual(v.iteracoes, 1)
        self.assertLessEqual(v.indexacoes, 1)

    def test_minimo_e_maximo_corretos(self):
        gerador = random.Random(3)
        v = [gerador.randrange(-10**9, 10**9) for _ in range(3000)]
        escolha = escolher(v)
        self.assertEqual((escolha.minimo, escolha.maximo), (min(v), max(v)))


class TestOrdenar(unittest.TestCase):
    def test_repassa_minimo_e_maximo(self):
        espiao = mock.Mock(return_value=[])
        faixa = math.floor(escolhedor.FATOR_CONTAGEM * 5000)
        v = aleatoria(5000, faixa)
        with mock.patch.dict(escolhedor.METODOS, {"contagem": espiao}):
            ordenar(v)
        espiao.assert_called_once_with(v, 0, faixa - 1)

    def test_executa_o_metodo_escolhido(self):
        espiao = mock.Mock(return_value=["ok"])
        with mock.patch.dict(escolhedor.METODOS, {"insercao": espiao}):
            self.assertEqual(ordenar([2, 1]), ["ok"])
        espiao.assert_called_once_with([2, 1])


if __name__ == "__main__":
    unittest.main()
