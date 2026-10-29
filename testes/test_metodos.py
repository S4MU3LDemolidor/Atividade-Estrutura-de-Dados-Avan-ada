"""Testes dos seis métodos e do ordenar.

Todos os métodos passam pelos mesmos casos de CasosComuns: lista vazia, um
elemento, todos iguais, já ordenada, invertida, valores negativos e listas
aleatórias comparadas com sorted().
"""

import random
import unittest

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


if __name__ == "__main__":
    unittest.main()
