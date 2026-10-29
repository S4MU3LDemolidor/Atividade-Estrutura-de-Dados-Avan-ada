"""Cronometragem usada pela calibração e pela medição final.

O coletor de lixo fica desligado enquanto o relógio corre, para que uma coleta
no meio de uma medição não seja contada como tempo do método.
"""

import gc
import platform
import subprocess
import sys
import time


def cronometrar(funcao, entrada, repeticoes: int) -> list[float]:
    """Tempos, em segundos, de `repeticoes` chamadas de funcao(entrada)."""
    tempos = []
    for _ in range(repeticoes):
        gc.collect()
        gc.disable()
        try:
            inicio = time.perf_counter_ns()
            funcao(entrada)
            fim = time.perf_counter_ns()
        finally:
            gc.enable()
        tempos.append((fim - inicio) / 1e9)
    return tempos


def cronometrar_lote(funcao, lote: list, repeticoes: int) -> list[float]:
    """Tempo médio por lista, em segundos, de funcao em cada lista do lote.

    Serve para listas pequenas demais para serem medidas uma a uma.
    """
    tempos = []
    for _ in range(repeticoes):
        gc.collect()
        gc.disable()
        try:
            inicio = time.perf_counter_ns()
            for entrada in lote:
                funcao(entrada)
            fim = time.perf_counter_ns()
        finally:
            gc.enable()
        tempos.append((fim - inicio) / 1e9 / len(lote))
    return tempos


def cronometrar_intercalado(funcoes: dict, entrada, repeticoes: int,
                            em_lote: bool = False, recusas: tuple = ()) -> dict:
    """Mede várias funções na mesma entrada, intercalando as repetições.

    Cada rodada mede todas as funções uma vez, e a ordem gira de uma rodada para
    a outra. Assim uma interferência passageira (outro processo, o sistema
    trocando o processo de núcleo) atinge todas, e não só a que estava no
    relógio naquele momento.

    Devolve {nome: lista de tempos em segundos}. Uma função que lança uma das
    exceções de `recusas` fica com None e não é chamada de novo.
    """
    medir = cronometrar_lote if em_lote else cronometrar
    nomes = list(funcoes)
    tempos = {nome: [] for nome in nomes}
    for rodada in range(repeticoes):
        k = rodada % len(nomes)
        for nome in nomes[k:] + nomes[:k]:
            if tempos[nome] is None:
                continue
            try:
                tempos[nome] += medir(funcoes[nome], entrada, 1)
            except recusas:
                tempos[nome] = None
    return tempos


def descrever_maquina() -> str:
    """Processador, sistema e versão do Python, para registrar junto dos tempos."""
    processador = platform.processor() or platform.machine()
    if sys.platform == "darwin":
        try:
            processador = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True, text=True, check=True,
            ).stdout.strip() or processador
        except (OSError, subprocess.CalledProcessError):
            pass
    return f"{processador}, {platform.system()} {platform.release()}, Python {platform.python_version()}"
