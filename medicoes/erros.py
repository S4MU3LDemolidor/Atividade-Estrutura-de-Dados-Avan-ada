"""Casos em que o escolher erra a decisão.

Mede listas feitas de poucas sequências longas fora de ordem, que enganam a
regra das quedas, e grava resultados/erros.md. A lista quase ordenada entra
como comparação, porque nela a decisão está certa.

Uso: python3 -m medicoes.erros [--n 10000] [--repeticoes 5] [--semente 2026]
"""

import argparse
import datetime
import random
import sys
from pathlib import Path

from medicoes import cenarios
from medicoes.tabelas import numero, tabela
from medicoes.tempo import cronometrar_intercalado, descrever_maquina
from ordenacao.base import base
from ordenacao import escolhedor
from ordenacao.escolhedor import escolher, ordenar, perfil
from ordenacao.hibrida import hibrida
from ordenacao.intercalacao import intercalacao

SAIDA = Path(__file__).resolve().parent.parent / "resultados" / "erros.md"

CASOS = {
    "Quase ordenado (decisão certa, para comparar)": cenarios.quase_ordenado,
    "Metades trocadas": cenarios.metades_trocadas,
    "3 listas ordenadas concatenadas": cenarios.listas_concatenadas,
    "Blocos de 5 em ordem decrescente": cenarios.blocos_decrescentes,
    "Blocos de 5 embaralhados + um valor extremo no fim": cenarios.corridas_com_extremo,
}
FIXOS = {"hibrida": hibrida, "intercalacao": intercalacao, "base": base}


def abaixo_do_maximo(v: list[int]) -> int:
    """Quantos elementos ficam abaixo do maior valor visto antes deles.

    É a medida que corrigiria os erros desta análise: ela enxerga sequências
    longas fora de ordem, que a soma das quedas não enxerga.
    """
    maior = v[0]
    abaixo = 0
    for x in v:
        if x < maior:
            abaixo += 1
        else:
            maior = x
    return abaixo


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Mede os casos em que o escolher erra.")
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--repeticoes", type=int, default=5)
    parser.add_argument("--semente", type=int, default=2026)
    args = parser.parse_args(argv)

    random.seed(args.semente)
    print("Medindo os casos de erro (cerca de 20 segundos)...", file=sys.stderr)
    linhas = []
    for nome, gerar in CASOS.items():
        print(f"  {nome}", file=sys.stderr)
        v = gerar(args.n, args.semente)
        p = perfil(v)
        tempos = cronometrar_intercalado({"ordenar": ordenar, **FIXOS}, v, args.repeticoes)
        menores = {metodo: min(lista) for metodo, lista in tempos.items()}
        melhor = min(FIXOS, key=menores.get)
        linhas.append([
            nome, numero(p.descidas / len(v), 3), numero(p.quedas / (p.maximo - p.minimo), 2),
            abaixo_do_maximo(v), escolher(v).metodo, numero(menores["ordenar"] * 1e3),
            f"{melhor} {numero(menores[melhor] * 1e3)}", numero(menores["ordenar"] / menores[melhor], 1),
        ])

    relatorio = (
        "# Casos em que o escolher erra\n\n"
        f"Gerado por `python3 -m medicoes.erros` em {datetime.date.today():%d/%m/%Y}.\n\n"
        f"- Máquina: {descrever_maquina()}\n"
        f"- n = {args.n}, semente {args.semente}\n"
        f"- {args.repeticoes} repetições intercaladas; vale o menor tempo\n\n"
        + tabela(["lista", "descidas/n", "quedas/amplitude", "abaixo do máximo", "escolha",
                  "ordenar (ms)", "melhor fixo (ms)", "ordenar / melhor"], linhas)
        + f"\n\nA regra da inserção exige descidas/n <= {numero(escolhedor.FRACAO_DESCIDAS, 3)} "
        f"e quedas/amplitude <= {numero(escolhedor.FATOR_QUEDAS)}. "
        "\"abaixo do máximo\" é a medida que corrigiria esses erros (não usada pelo escolher).\n"
    )
    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text(relatorio, encoding="utf-8")
    print(relatorio)


if __name__ == "__main__":
    main()
