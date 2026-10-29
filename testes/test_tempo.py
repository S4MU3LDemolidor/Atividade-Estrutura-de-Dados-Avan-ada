"""Testes da cronometragem usada nas medições."""

import gc
import unittest

from medicoes.tempo import cronometrar, cronometrar_lote


class TestCronometrar(unittest.TestCase):
    def test_chama_a_funcao_uma_vez_por_repeticao(self):
        chamadas = []
        tempos = cronometrar(chamadas.append, "entrada", 4)
        self.assertEqual(chamadas, ["entrada"] * 4)
        self.assertEqual(len(tempos), 4)
        self.assertTrue(all(t >= 0 for t in tempos))

    def test_lote_chama_para_cada_lista_e_divide_pelo_tamanho(self):
        chamadas = []
        lote = [[1], [2], [3]]
        tempos = cronometrar_lote(chamadas.append, lote, 2)
        self.assertEqual(chamadas, lote * 2)
        self.assertEqual(len(tempos), 2)
        self.assertTrue(all(t >= 0 for t in tempos))

    def test_religa_o_coletor_mesmo_com_erro(self):
        self.assertTrue(gc.isenabled())

        def falha(_):
            raise RuntimeError("falhou")

        with self.assertRaises(RuntimeError):
            cronometrar(falha, None, 1)
        self.assertTrue(gc.isenabled())


if __name__ == "__main__":
    unittest.main()
