from __future__ import annotations
import argparse
import sys
from dataclasses import dataclass
from typing import Dict

DEFAULT_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


@dataclass(frozen=True)
class Alphabet:
    symbols: str
    pos: Dict[str, int]
    m: int

    @staticmethod
    def from_string(symbols: str) -> "Alphabet":
        symbols = symbols.strip("\n")
        if not symbols:
            raise ValueError("Alphabet cannot be empty.")
        if len(symbols) < 2:
            raise ValueError("Alphabet must contain at least two unique characters.")
        if len(set(symbols)) != len(symbols):
            raise ValueError("Alphabet must not contain duplicate characters.")
        pos = {ch: i for i, ch in enumerate(symbols)}
        return Alphabet(symbols=symbols, pos=pos, m=len(symbols))


def transform(text: str, alpha: Alphabet, shift: int) -> str:
    output = []
    for ch in text:
        idx = alpha.pos.get(ch)
        if idx is None:
            output.append(ch)
        else:
            output.append(alpha.symbols[(idx + shift) % alpha.m])
    return "".join(output)


def crack_preview(ciphertext: str, alpha: Alphabet) -> str:
    results = []
    for k in range(alpha.m):
        candidate = transform(ciphertext, alpha, shift=-k)
        results.append(f"k={k:>3} | {candidate}")
    return "\n".join(results)


def open_input(path):
    if path:
        try:
            return open(path, "r", encoding="utf-8", errors="replace")
        except FileNotFoundError:
            print(f"Error: input file '{path}' not found.", file=sys.stderr)
            sys.exit(1)
    return sys.stdin


def open_output(path):
    if path:
        return open(path, "w", encoding="utf-8", errors="replace")
    return sys.stdout


def build_cli():
    parser = argparse.ArgumentParser(description="Generalized Caesar cipher.")
    sub = parser.add_subparsers(dest="command", required=True)

    # Encrypt
    enc = sub.add_parser("encrypt")
    enc.add_argument("-k", "--key", type=int, required=True)
    enc.add_argument("-f", "--file")
    enc.add_argument("-o", "--out")
    enc.add_argument("--alphabet", default=DEFAULT_ALPHABET)
    enc.add_argument("--alphabet-file", help="Read alphabet from a file.")

    # Decrypt
    dec = sub.add_parser("decrypt")
    dec.add_argument("-k", "--key", type=int, required=True)
    dec.add_argument("-f", "--file")
    dec.add_argument("-o", "--out")
    dec.add_argument("--alphabet", default=DEFAULT_ALPHABET)
    dec.add_argument("--alphabet-file", help="Read alphabet from a file.")

    # Crack
    crack = sub.add_parser("crack")
    crack.add_argument("-f", "--file")
    crack.add_argument("-o", "--out")
    crack.add_argument("--alphabet", default=DEFAULT_ALPHABET)
    crack.add_argument("--alphabet-file", help="Read alphabet from a file.")

    return parser


def main():
    args = build_cli().parse_args()

    # Load alphabet from file if provided
    if args.alphabet_file:
        try:
            with open(args.alphabet_file, "r", encoding="utf-8") as f:
                args.alphabet = f.read().strip("\n")
        except FileNotFoundError:
            print(
                f"Error: alphabet file '{args.alphabet_file}' not found.",
                file=sys.stderr,
            )
            sys.exit(1)

    alpha = Alphabet.from_string(args.alphabet)
    print(f"[INFO] Command      : {args.command}", file=sys.stderr)
    print(f"[INFO] Alphabet     : {args.alphabet}", file=sys.stderr)
    print(f"[INFO] Alphabet size: m = {alpha.m}", file=sys.stderr)
    if args.command in ("encrypt", "decrypt"):
        print(f"[INFO] Key          : k = {args.key}", file=sys.stderr)
        print(f"[INFO] Shift        : {args.key % alpha.m} (k mod m)", file=sys.stderr)
    print(f"[INFO] Input file   : {args.file or 'stdin'}", file=sys.stderr)
    print(f"[INFO] Output file  : {args.out or 'stdout'}", file=sys.stderr)
    instream = open_input(args.file)
    outstream = open_output(args.out)

    try:
        if args.command == "crack":
            text = instream.read()
            outstream.write(crack_preview(text, alpha) + "\n")
            return

        k = args.key % alpha.m
        shift = +k if args.command == "encrypt" else -k

        while True:
            chunk = instream.read(4 * 1024 * 1024)  # 4MB at a time
            if not chunk:
                break
            result = transform(chunk, alpha, shift)
            outstream.write(result)

    finally:
        if args.file:
            instream.close()
        if args.out:
            outstream.close()


if __name__ == "__main__":
    main()
