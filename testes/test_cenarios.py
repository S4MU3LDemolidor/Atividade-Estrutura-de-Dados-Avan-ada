"""Testes dos geradores de cenários."""

import unittest

from medicoes import cenarios


def descidas(v):
    return sum(1 for a, b in zip(v, v[1:]) if a > b)


class TestCenarios(unittest.TestCase):
    def test_tamanhos(self):
        self.assertEqual(len(cenarios.aleatorio_chaves_grandes(1000, 1)), 1000)
        self.assertEqual(len(cenarios.faixa_estreita(1000, 1)), 1000)
        self.assertEqual(len(cenarios.quase_ordenado(1000, 1)), 1000)
        self.assertEqual(len(cenarios.minuscula(8, 1)), 8)
        self.assertEqual(len(cenarios.metades_trocadas(1000, 1)), 1000)

    def test_mesma_semente_mesma_lista(self):
        for gerador in (cenarios.aleatorio_chaves_grandes, cenarios.faixa_estreita,
                        cenarios.quase_ordenado, cenarios.minuscula,
                        cenarios.metades_trocadas):
            with self.subTest(gerador=gerador.__name__):
                self.assertEqual(gerador(500, 42), gerador(500, 42))
                self.assertNotEqual(gerador(500, 42), gerador(500, 43))

    def test_faixas(self):
        v = cenarios.aleatorio_chaves_grandes(5000, 1)
        self.assertTrue(all(0 <= x < cenarios.CHAVE_GRANDE for x in v))
        self.assertGreater(max(v) - min(v), 10**11)
        v = cenarios.faixa_estreita(5000, 1)
        self.assertTrue(all(0 <= x < cenarios.FAIXA_ESTREITA for x in v))

    def test_quase_ordenado_tem_poucas_descidas(self):
        v = cenarios.quase_ordenado(10_000, 1, fracao=0.01)
        self.assertGreater(descidas(v), 0)
        # 100 trocas; cada troca mexe em no máximo 4 pares vizinhos
        self.assertLessEqual(descidas(v), 4 * 100)

    def test_quase_ordenado_sem_trocas_e_ordenado(self):
        v = cenarios.quase_ordenado(1000, 1, fracao=0)
        self.assertEqual(v, sorted(v))

    def test_metades_trocadas_tem_uma_descida(self):
        v = cenarios.metades_trocadas(1000, 1)
        self.assertEqual(descidas(v), 1)
        self.assertGreater(v[0], v[-1])

    def test_lote_de_minusculas(self):
        lote = cenarios.lote_minusculas(50, 8, 1)
        self.assertEqual(len(lote), 50)
        self.assertTrue(all(len(v) == 8 for v in lote))
        self.assertEqual(lote, cenarios.lote_minusculas(50, 8, 1))


if __name__ == "__main__":
    unittest.main()
