"""Testes dos seis métodos e do ordenar.

Todos os métodos passam pelos mesmos casos de CasosComuns: lista vazia, um
elemento, todos iguais, já ordenada, invertida, valores negativos e listas
aleatórias comparadas com sorted().
"""

import random
import time
import unittest
from unittest import mock

from ordenacao import contagem as modulo_contagem
from ordenacao.base import base, passadas
from ordenacao.contagem import FaixaGrandeDemais, contagem
from ordenacao.escolhedor import ordenar
from ordenacao.hibrida import hibrida
from ordenacao.insercao import insercao
from ordenacao.intercalacao import intercalacao
from ordenacao.rapida import particionar, rapida


class CasosComuns:
    """Casos que valem para qualquer método. As subclasses definem `metodo`."""

    metodo = None

    def ordena(self, v):
        return type(self).metodo(v)

    def test_lista_vazia(self):
        self.assertEqual(self.ordena([]), [])

    def test_um_elemento(self):
        self.assertEqual(self.ordena([7]), [7])

    def test_todos_iguais(self):
        self.assertEqual(self.ordena([5] * 2000), [5] * 2000)

    def test_ja_ordenada(self):
        v = list(range(500))
        self.assertEqual(self.ordena(v), v)

    def test_invertida(self):
        self.assertEqual(self.ordena(list(range(500, 0, -1))), list(range(1, 501)))

    def test_so_negativos(self):
        self.assertEqual(self.ordena([-3, -10, -1, -7]), [-10, -7, -3, -1])

    def test_negativos_e_positivos(self):
        v = [3, -2, 0, -15, 8, -2, 1]
        self.assertEqual(self.ordena(v), sorted(v))

    def test_muitos_repetidos(self):
        gerador = random.Random(7)
        v = [gerador.randrange(5) for _ in range(1000)]
        self.assertEqual(self.ordena(v), sorted(v))

    def test_aleatorias(self):
        for semente in (1, 2, 3):
            gerador = random.Random(semente)
            for n in (2, 10, 100, 1000):
                v = [gerador.randrange(-10**6, 10**6) for _ in range(n)]
                with self.subTest(semente=semente, n=n):
                    self.assertEqual(self.ordena(v), sorted(v))

    def test_nao_altera_entrada(self):
        v = [4, 1, 3, 1, -2]
        copia = list(v)
        self.ordena(v)
        self.assertEqual(v, copia)


class TestInsercao(CasosComuns, unittest.TestCase):
    metodo = staticmethod(insercao)


class TestIntercalacao(CasosComuns, unittest.TestCase):
    metodo = staticmethod(intercalacao)


class TestRapida(CasosComuns, unittest.TestCase):
    metodo = staticmethod(rapida)

    def test_particionar_separa_em_tres_faixas(self):
        gerador = random.Random(11)
        for _ in range(50):
            a = [gerador.randrange(20) for _ in range(60)]
            original = sorted(a)
            ini, fim = 5, 50
            fora = a[:ini] + a[fim + 1:]
            menor, maior = particionar(a, ini, fim)
            pivo = a[menor]
            self.assertTrue(all(x < pivo for x in a[ini:menor]))
            self.assertTrue(all(x == pivo for x in a[menor:maior + 1]))
            self.assertTrue(all(x > pivo for x in a[maior + 1:fim + 1]))
            self.assertEqual(a[:ini] + a[fim + 1:], fora)
            self.assertEqual(sorted(a), original)



class TestHibrida(CasosComuns, unittest.TestCase):
    metodo = staticmethod(hibrida)

    def test_cortes_extremos(self):
        gerador = random.Random(5)
        v = [gerador.randrange(-1000, 1000) for _ in range(500)]
        for corte in (1, 64, 1000):
            with self.subTest(corte=corte):
                self.assertEqual(hibrida(v, corte=corte), sorted(v))



class TestContagem(CasosComuns, unittest.TestCase):
    metodo = staticmethod(contagem)

    def test_faixa_grande_e_recusada_sem_alocar(self):
        inicio = time.perf_counter()
        with self.assertRaises(FaixaGrandeDemais):
            contagem([0, 10**12])
        self.assertLess(time.perf_counter() - inicio, 0.1)

    def test_faixa_no_limite_e_aceita(self):
        with mock.patch.object(modulo_contagem, "LIMITE_CONTADORES", 10):
            self.assertEqual(contagem([9, 0, 5]), [0, 5, 9])
            with self.assertRaises(FaixaGrandeDemais):
                contagem([10, 0, 5])

    def test_minimo_e_maximo_repassados(self):
        v = [3, -4, 8, 3, 0]
        self.assertEqual(contagem(v, minimo=-4, maximo=8), sorted(v))



class TestBase(CasosComuns, unittest.TestCase):
    metodo = staticmethod(base)

    def test_valores_acima_de_64_bits(self):
        v = [2**70, -2**70, 5, 2**70 - 1, -3, 0]
        self.assertEqual(base(v), sorted(v))

    def test_minimo_e_maximo_repassados(self):
        v = [300, -4, 70000, 3, 0]
        self.assertEqual(base(v, minimo=-4, maximo=70000), sorted(v))

    def test_passadas(self):
        self.assertEqual(passadas(0), 0)
        self.assertEqual(passadas(1), 1)
        self.assertEqual(passadas(255), 1)
        self.assertEqual(passadas(256), 2)
        self.assertEqual(passadas(2**64 - 1), 8)



class TestOrdenar(CasosComuns, unittest.TestCase):
    metodo = staticmethod(ordenar)

    def test_listas_grandes_de_cada_tipo(self):
        gerador = random.Random(9)
        casos = {
            "faixa estreita": [gerador.randrange(-50, 50) for _ in range(3000)],
            "chaves grandes": [gerador.randrange(-10**12, 10**12) for _ in range(3000)],
            "chaves enormes": [gerador.randrange(-2**90, 2**90) for _ in range(3000)],
            "quase ordenada": list(range(2990)) + [2995, 2993, 2991, 2994, 2990, 2999, 2992],
        }
        for nome, v in casos.items():
            with self.subTest(caso=nome):
                self.assertEqual(ordenar(v), sorted(v))


if __name__ == "__main__":
    unittest.main()
