import sys
from typing import List, Iterable

def gaps_shell(n: int):
    g = n // 2
    while g > 0:
        yield g
        g //= 2

def gaps_knuth(n: int):
    gaps = []
    h = 1
    while h < n:
        gaps.append(h)
        h = 3*h + 1
    for g in reversed(gaps):
        if g > 0:
            yield g

def gaps_sedgewick(n: int):
    gaps = set()
    k = 0
    while True:
        g1 = 4**k + 3*(2**(k-1)) + 1 if k > 0 else 1
        g2 = 9*(4**k) - 9*(2**k) + 1
        if g1 < n: gaps.add(g1)
        if g2 < n: gaps.add(g2)
        if g1 >= n and g2 >= n: break
        k += 1
    for g in sorted(gaps, reverse=True):
        if g > 0:
            yield g

def shell_sort(arr: List[int], seq: str = "shell") -> None:
    n = len(arr)
    if seq == "shell":
        gaps = gaps_shell(n)
    elif seq == "knuth":
        gaps = gaps_knuth(n)
    elif seq == "sedgewick":
        gaps = gaps_sedgewick(n)
    else:
        raise ValueError("Sequência desconhecida. Use 'shell', 'knuth', ou 'sedgewick'.")

    for gap in gaps:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp

def main(args_cli: Iterable[str]):
    import argparse
    parser = argparse.ArgumentParser(description="Shell Sort em Python")
    parser.add_argument("--sequence", choices=["shell","knuth","sedgewick"], default="shell",
                        help="Sequência de gaps a usar")
    parser.add_argument("--demo", action="store_true", help="Rodar uma ordenação de demonstração rápida")
    args = parser.parse_args(list(args_cli))

    if args.demo:
        data = [23, 12, 1, 8, 34, 54, 2, 3]
        print("Antes:", data)
        shell_sort(data, seq=args.sequence)
        print("Depois: ", data)
    else:
        data = []
        for line in sys.stdin:
            data.extend(int(x) for x in line.strip().split())
        shell_sort(data, seq=args.sequence)
        print(" ".join(map(str, data)))

if __name__ == "__main__":
    main(sys.argv[1:])