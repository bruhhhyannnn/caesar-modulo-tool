"""
Caesar Modulo Tool (stream/file I/O; key-based encrypt/decrypt; brute-force crack)

This tool implements a generalized Caesar cipher over an arbitrary alphabet.

Notes:
  - Characters not found in the alphabet are preserved unchanged.
  - This is an educational cipher and not secure for real-world use.

Author: Bryan Jesus Mangapit
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Dict, Optional, TextIO


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
            # This is critical: duplicates break the bijection char<->index
            raise ValueError("Alphabet must not contain duplicate characters.")

        pos = {ch: i for i, ch in enumerate(symbols)}
        return Alphabet(symbols=symbols, pos=pos, m=len(symbols))


def transform(text: str, alpha: Alphabet, shift: int) -> str:
    """Apply Caesar shift using modulo arithmetic."""
    output = []
    for ch in text:
        idx = alpha.pos.get(ch)
        if idx is None:
            output.append(
                ch
            )  # keep unknown symbols (spaces, punctuation, emojis, etc.)
        else:
            output.append(alpha.symbols[(idx + shift) % alpha.m])
    return "".join(output)


def crack_preview(ciphertext: str, alpha: Alphabet) -> str:
    """Brute-force all possible keys and return candidate plaintexts."""
    results = []
    for k in range(alpha.m):
        candidate = transform(ciphertext, alpha, shift=-k)
        results.append(f"k={k:>3} | {candidate}")
    return "\n".join(results)


def open_input(path: Optional[str]) -> TextIO:
    if path:
        return open(path, "r", encoding="utf-8", errors="replace")
    return sys.stdin


def open_output(path: Optional[str]) -> TextIO:
    if path:
        return open(path, "w", encoding="utf-8", errors="replace")
    return sys.stdout


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generalized Caesar cipher over a configurable alphabet."
    )

    parser.add_argument(
        "--alphabet",
        default=DEFAULT_ALPHABET,
        help="Alphabet to use (default: lowercase a-z).",
    )

    parser.add_argument("-f", "--file", help="Input file (default: stdin).")
    parser.add_argument("-o", "--out", help="Output file (default: stdout).")

    sub = parser.add_subparsers(dest="command", required=True)

    enc = sub.add_parser("encrypt", help="Encrypt using key k.")
    enc.add_argument("-k", "--key", type=int, required=True)

    dec = sub.add_parser("decrypt", help="Decrypt using key k.")
    dec.add_argument("-k", "--key", type=int, required=True)

    sub.add_parser("crack", help="Brute-force all possible keys.")

    return parser


def main() -> None:
    args = build_cli().parse_args()
    alpha = Alphabet.from_string(args.alphabet)

    instream = open_input(args.file)
    outstream = open_output(args.out)

    try:
        text = instream.read()

        if args.command == "crack":
            outstream.write(crack_preview(text, alpha) + "\n")
            return

        # encrypt/decrypt
        k = args.key % alpha.m
        shift = +k if args.command == "encrypt" else -k

        result = transform(text, alpha, shift)
        outstream.write(result)

    finally:
        if args.file:
            instream.close()
        if args.out:
            outstream.close()


if __name__ == "__main__":
    main()
