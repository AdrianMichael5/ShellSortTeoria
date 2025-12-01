"""
Script de benchmark para Shell Sort em Python (e opcionalmente C).
- Gera arrays aleatórios para tamanhos: 1k, 5k, 10k, 20k, 50k (configurável)
- Executa 20 repetições por padrão, calcula média/desvio padrão
- Salva CSV e gráficos PNG
- Se um executável C compilado "./shell_sort_c" estiver presente, também fará o benchmark dele.

Uso:
  python benchmark_shell_sort.py
  # Após compilar C:
  gcc -O2 -o shell_sort_c shell_sort.c
  python benchmark_shell_sort.py --include-c
"""
import argparse
import csv
import os
import random
import statistics as stats
import subprocess
import time
from typing import List, Tuple

import matplotlib.pyplot as plt

from shell_sort import shell_sort

def gerar_array(n: int, seed: int = None) -> List[int]:
    if seed is not None:
        random.seed(seed)
    return [random.randint(0, 10**6) for _ in range(n)]

def medir_tempo_python(dados: List[int], sequencia: str) -> float:
    arr = list(dados)  # copiar
    t0 = time.perf_counter()
    shell_sort(arr, seq=sequencia)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0  # ms

def medir_tempo_c(dados: List[int], sequencia: str, exe: str = "./shell_sort_c") -> float:
    # Fornecer números via stdin, separados por espaço; ler saída (ignorada aqui).
    inp = " ".join(str(x) for x in dados).encode("utf-8")
    t0 = time.perf_counter()
    proc = subprocess.run([exe, "--sequence", sequencia], input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t1 = time.perf_counter()
    if proc.returncode != 0:
        raise RuntimeError(f"Executável C falhou: {proc.stderr.decode('utf-8', errors='ignore')}")
    return (t1 - t0) * 1000.0

def plotar_curva(xs, ys, titulo, xlabel, ylabel, caminho_saida):
    plt.figure()
    plt.plot(xs, ys, marker="o")
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=160)
    plt.close()

def plotar_com_teoria(xs, ys, titulo, xlabel, ylabel, caminho_saida, potencia_teorica=1.5):
    # Sobrepor empírico com uma curva n^p normalizada para comparação visual
    import numpy as np
    xs_np = np.array(xs, dtype=float)
    teoria = xs_np ** potencia_teorica
    # Escalar teoria para coincidir com o primeiro ponto empírico não-zero
    s = ys[0] / teoria[0] if teoria[0] != 0 else 1.0
    teoria_escalada = teoria * s

    plt.figure()
    plt.plot(xs, ys, marker="o", label="Empírico")
    plt.plot(xs, teoria_escalada, marker="x", linestyle="--", label=f"n^{potencia_teorica} (normalizado)")
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=160)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Benchmark Shell Sort (Python vs C)")
    parser.add_argument("--sizes", type=str, default="1000,5000,10000,20000,50000",
                        help="Tamanhos de entrada separados por vírgula")
    parser.add_argument("--reps", type=int, default=20, help="Repetições por tamanho")
    parser.add_argument("--sequence", choices=["shell","knuth","sedgewick"], default="shell",
                        help="Sequência de gaps")
    parser.add_argument("--include-c", action="store_true", help="Benchmark ./shell_sort_c se presente")
    args = parser.parse_args()

    tamanhos = [int(x) for x in args.sizes.split(",")]
    repeticoes = int(args.reps)

    resultados = []  # linhas: (impl, tamanho, media_ms, desvio_ms)
    csv_saida = "results_shell_sort.csv"

    # Benchmark Python
    for n in tamanhos:
        tempos = []
        for r in range(repeticoes):
            dados = gerar_array(n, seed=r)
            ms = medir_tempo_python(dados, sequencia=args.sequence)
            tempos.append(ms)
        media_ms = stats.mean(tempos)
        desvio_ms = stats.pstdev(tempos)
        resultados.append(("python", n, media_ms, desvio_ms))
        print(f"[PY] n={n:6d}  media={media_ms:8.3f} ms  desvio={desvio_ms:8.3f} ms")

    # Benchmark C (opcional)
    # AJUSTE PARA WINDOWS: procura por .exe também
    if args.include_c and os.path.exists("shell_sort_c.exe"):
        for n in tamanhos:
            tempos = []
            for r in range(repeticoes):
                dados = gerar_array(n, seed=r)
                # AJUSTE PARA WINDOWS: chama o executável com .exe
                ms = medir_tempo_c(dados, sequencia=args.sequence, exe="shell_sort_c.exe")
                tempos.append(ms)
            media_ms = stats.mean(tempos)
            desvio_ms = stats.pstdev(tempos)
            resultados.append(("c", n, media_ms, desvio_ms))
            print(f"[ C ] n={n:6d}  media={media_ms:8.3f} ms  desvio={desvio_ms:8.3f} ms")
    elif args.include_c:
        print("Aviso: './shell_sort_c' (ou .exe) não encontrado. Compile primeiro com: gcc -O2 -o shell_sort_c shell_sort.c")

    # Salvar CSV
    with open(csv_saida, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["implementacao","n","media_ms","desvio_ms"])
        for linha in resultados:
            w.writerow(linha)

    # Criar gráficos
    # 1) Curva Python
    ns_py = [n for impl,n,_,_ in resultados if impl=="python"]
    medias_py = [media for impl,n,media,_ in resultados if impl=="python"]
    plotar_curva(ns_py, medias_py, "Shell Sort (Python) - Tempo médio", "n", "ms", "plot_python_mean.png")
    plotar_com_teoria(ns_py, medias_py, "Shell Sort (Python) - Empírico vs n^1.5", "n", "ms",
                      "plot_python_vs_theory.png", potencia_teorica=1.5)

    # 2) Se C existe: comparar Python vs C
    if any(impl=="c" for impl,_,_,_ in resultados):
        ns_c = [n for impl,n,_,_ in resultados if impl=="c"]
        medias_c = [media for impl,n,media,_ in resultados if impl=="c"]
        # Gráfico combinado
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(ns_py, medias_py, marker="o", label="Python")
        plt.plot(ns_c, medias_c, marker="s", label="C")
        plt.title("Shell Sort - Comparação Python vs C")
        plt.xlabel("n")
        plt.ylabel("ms")
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig("plot_python_vs_c.png", dpi=160)
        plt.close()

    # --- TABELA DE RESUMO FORMATADA ---
    print("\n" + "="*62)
    print(f"{'RESUMO DOS RESULTADOS':^62}")
    print("="*62)
    print(f"| {'Ling.':<10} | {'N (Tam.)':<10} | {'Média (ms)':<15} | {'Desvio Pad.':<15} |")
    print("-" * 62)

    for impl, n, media, desvio in resultados:
        # Deixa o nome da linguagem mais bonito
        nome_ling = "Python" if impl == "python" else "C"
        print(f"| {nome_ling:<10} | {n:<10} | {media:<15.4f} | {desvio:<15.4f} |")
    
    print("="*62 + "\n")
    # ----------------------------------

    print("Arquivos gerados:")
    print(f" - {csv_saida}")
    print(" - plot_python_mean.png")
    print(" - plot_python_vs_theory.png")
    if any(impl=="c" for impl,_,_,_ in resultados):
        print(" - plot_python_vs_c.png")

if __name__ == "__main__":
    main()