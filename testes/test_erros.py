"""Testes da medida usada na análise dos erros do escolher."""

import unittest

from medicoes.erros import abaixo_do_maximo


class TestAbaixoDoMaximo(unittest.TestCase):
    def test_lista_ordenada(self):
        self.assertEqual(abaixo_do_maximo([1, 2, 2, 5]), 0)

    def test_conta_quem_fica_abaixo_do_maior_visto_ate_ali(self):
        self.assertEqual(abaixo_do_maximo([1, 3, 2, 5, 4]), 2)

    def test_metades_trocadas(self):
        self.assertEqual(abaixo_do_maximo([3, 4, 5, 0, 1, 2]), 3)


if __name__ == "__main__":
    unittest.main()
