"""
Shell Sort implementation in Python with selectable gap sequences,
plus a simple CLI to sort numbers from stdin or to run a quick demo.

Usage:
  python shell_sort.py --sequence shell < numbers.txt
  python shell_sort.py --demo
"""
import sys
from typing import List, Iterable

def gaps_shell(n: int):
    g = n // 2
    while g > 0:
        yield g
        g //= 2

def gaps_knuth(n: int):
    # Knuth: 1, 4, 13, 40, 121, ...  h = 3*h + 1; reverse to descend
    gaps = []
    h = 1
    while h < n:
        gaps.append(h)
        h = 3*h + 1
    for g in reversed(gaps):
        if g > 0:
            yield g

def gaps_sedgewick(n: int):
    # Sedgewick 1982: mix of 4^k + 3*2^(k-1) + 1 and 9*4^k - 9*2^k + 1
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

def shell_sort(arr: List[int], sequence: str = "shell") -> None:
    n = len(arr)
    if sequence == "shell":
        gaps = gaps_shell(n)
    elif sequence == "knuth":
        gaps = gaps_knuth(n)
    elif sequence == "sedgewick":
        gaps = gaps_sedgewick(n)
    else:
        raise ValueError("Unknown sequence. Use 'shell', 'knuth', or 'sedgewick'.")

    for gap in gaps:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp

def main(argv: Iterable[str]):
    import argparse
    parser = argparse.ArgumentParser(description="Shell Sort in Python")
    parser.add_argument("--sequence", choices=["shell","knuth","sedgewick"], default="shell",
                        help="Gap sequence to use")
    parser.add_argument("--demo", action="store_true", help="Run a quick demo sort")
    args = parser.parse_args(list(argv))

    if args.demo:
        data = [23, 12, 1, 8, 34, 54, 2, 3]
        print("Before:", data)
        shell_sort(data, sequence=args.sequence)
        print("After: ", data)
    else:
        # Read integers from stdin
        data = []
        for line in sys.stdin:
            data.extend(int(x) for x in line.strip().split())
        shell_sort(data, sequence=args.sequence)
        print(" ".join(map(str, data)))

if __name__ == "__main__":
    main(sys.argv[1:])