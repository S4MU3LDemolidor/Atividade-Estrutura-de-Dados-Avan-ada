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
