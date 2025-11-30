"""
Benchmark script for Shell Sort in Python (and optionally C).
- Generates random arrays for sizes: 1k, 5k, 10k, 20k, 50k (configurable)
- Runs 20 repetitions by default, computes mean/std
- Saves CSV and PNG charts
- If a compiled C executable "./shell_sort_c" is present, it will also benchmark it.

Usage:
  python benchmark_shell_sort.py
  # After compiling C:
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

def gen_array(n: int, seed: int = None) -> List[int]:
    if seed is not None:
        random.seed(seed)
    return [random.randint(0, 10**6) for _ in range(n)]

def time_python_shell_sort(data: List[int], sequence: str) -> float:
    arr = list(data)  # copy
    t0 = time.perf_counter()
    shell_sort(arr, sequence=sequence)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0  # ms

def time_c_shell_sort(data: List[int], sequence: str, exe: str = "./shell_sort_c") -> float:
    # Provide numbers via stdin, space-separated; read output (ignored here).
    inp = " ".join(str(x) for x in data).encode("utf-8")
    t0 = time.perf_counter()
    proc = subprocess.run([exe, "--sequence", sequence], input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t1 = time.perf_counter()
    if proc.returncode != 0:
        raise RuntimeError(f"C executable failed: {proc.stderr.decode('utf-8', errors='ignore')}")
    return (t1 - t0) * 1000.0

def plot_curve(xs, ys, title, xlabel, ylabel, outpath):
    plt.figure()
    plt.plot(xs, ys, marker="o")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(outpath, dpi=160)
    plt.close()

def plot_with_theory(xs, ys, title, xlabel, ylabel, outpath, theory_power=1.5):
    # Overlay empirical with a normalized n^p curve for visual comparison
    import numpy as np
    xs_np = np.array(xs, dtype=float)
    theory = xs_np ** theory_power
    # Scale theory to match the first non-zero empirical point
    s = ys[0] / theory[0] if theory[0] != 0 else 1.0
    theory_scaled = theory * s

    plt.figure()
    plt.plot(xs, ys, marker="o", label="Empírico")
    plt.plot(xs, theory_scaled, marker="x", linestyle="--", label=f"n^{theory_power} (normalizado)")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=160)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Benchmark Shell Sort (Python vs C)")
    parser.add_argument("--sizes", type=str, default="1000,5000,10000,20000,50000",
                        help="Comma-separated input sizes")
    parser.add_argument("--reps", type=int, default=20, help="Repetitions per size")
    parser.add_argument("--sequence", choices=["shell","knuth","sedgewick"], default="shell",
                        help="Gap sequence")
    parser.add_argument("--include-c", action="store_true", help="Benchmark ./shell_sort_c if present")
    args = parser.parse_args()

    sizes = [int(x) for x in args.sizes.split(",")]
    reps = int(args.reps)

    results = []  # rows: (impl, size, mean_ms, std_ms)
    out_csv = "results_shell_sort.csv"

    # Benchmark Python
    for n in sizes:
        times = []
        for r in range(reps):
            data = gen_array(n, seed=r)
            ms = time_python_shell_sort(data, sequence=args.sequence)
            times.append(ms)
        mean_ms = stats.mean(times)
        std_ms = stats.pstdev(times)
        results.append(("python", n, mean_ms, std_ms))
        print(f"[PY] n={n:6d}  mean={mean_ms:8.3f} ms  std={std_ms:8.3f} ms")

    # Benchmark C (optional)
    if args.include_c and os.path.exists("shell_sort_c.exe"):
        for n in sizes:
            times = []
            for r in range(reps):
                data = gen_array(n, seed=r)
                ms = time_c_shell_sort(data, sequence=args.sequence, exe="shell_sort_c.exe")
                times.append(ms)
            mean_ms = stats.mean(times)
            std_ms = stats.pstdev(times)
            results.append(("c", n, mean_ms, std_ms))
            print(f"[ C ] n={n:6d}  mean={mean_ms:8.3f} ms  std={std_ms:8.3f} ms")
    elif args.include_c:
        print("Aviso: './shell_sort_c' não encontrado. Compile primeiro com: gcc -O2 -o shell_sort_c shell_sort.c")

    # Save CSV
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["implementation","n","mean_ms","std_ms"])
        for row in results:
            w.writerow(row)

    # Create plots
    # 1) Python curve
    py_ns = [n for impl,n,_,_ in results if impl=="python"]
    py_means = [mean for impl,n,mean,_ in results if impl=="python"]
    plot_curve(py_ns, py_means, "Shell Sort (Python) - Tempo médio", "n", "ms", "plot_python_mean.png")
    plot_with_theory(py_ns, py_means, "Shell Sort (Python) - Empírico vs n^1.5", "n", "ms",
                     "plot_python_vs_theory.png", theory_power=1.5)

    # 2) If C exists: compare Python vs C
    if any(impl=="c" for impl,_,_,_ in results):
        c_ns = [n for impl,n,_,_ in results if impl=="c"]
        c_means = [mean for impl,n,mean,_ in results if impl=="c"]
        # Combined plot
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(py_ns, py_means, marker="o", label="Python")
        plt.plot(c_ns, c_means, marker="s", label="C")
        plt.title("Shell Sort - Comparação Python vs C")
        plt.xlabel("n")
        plt.ylabel("ms")
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig("plot_python_vs_c.png", dpi=160)
        plt.close()

    print("Arquivos gerados:")
    print(" - results_shell_sort.csv")
    print(" - plot_python_mean.png")
    print(" - plot_python_vs_theory.png")
    if any(impl=="c" for impl,_,_,_ in results):
        print(" - plot_python_vs_c.png")

if __name__ == "__main__":
    main()