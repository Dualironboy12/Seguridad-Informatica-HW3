#!/usr/bin/env python3
"""Tablas de suma y multiplicación en GF(2^3).

Irreducible por defecto: x^3 + x + 1  (binario 0b1011 = 0xB).
Verificar contra el PP slide 124 del curso; si difiere, pasar --mod.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def gf_mul(a: int, b: int, mod: int = 0b1011, degree: int = 3) -> int:
    """Multiplicación en GF(2^degree) con reducción módulo ``mod``."""
    result = 0
    a &= (1 << degree) - 1
    b &= (1 << degree) - 1
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & (1 << degree):
            a ^= mod
    return result & ((1 << degree) - 1)


def addition_table() -> list[list[int]]:
    return [[i ^ j for j in range(8)] for i in range(8)]


def multiplication_table(mod: int = 0b1011) -> list[list[int]]:
    return [[gf_mul(i, j, mod=mod) for j in range(8)] for i in range(8)]


def _fmt_table(table: list[list[int]], title: str) -> str:
    header = "   | " + " ".join(f"{j:03b}" for j in range(8))
    sep = "---+-" + "-" * (4 * 8)
    lines = [title, header, sep]
    for i, row in enumerate(table):
        lines.append(f"{i:03b}| " + " ".join(f"{v:03b}" for v in row))
    return "\n".join(lines)


def poly_str(mod: int) -> str:
    parts = []
    for i in range(3, -1, -1):
        if mod & (1 << i):
            if i == 0:
                parts.append("1")
            elif i == 1:
                parts.append("x")
            else:
                parts.append(f"x^{i}")
    return " + ".join(parts)


def build_report(mod: int = 0b1011) -> str:
    add = addition_table()
    mul = multiplication_table(mod)
    lines = [
        "=== GF(2^3) addition and multiplication tables ===",
        f"Elements: 0..7 as polynomials over GF(2), degree < 3",
        f"Addition: XOR of coefficient vectors",
        f"Multiplication modulus: {poly_str(mod)} (0b{mod:b})",
        "",
        "Verify this irreducible against course PP slide 124.",
        "If the slide uses another polynomial, rerun with --mod (e.g. --mod 0b1101).",
        "",
        _fmt_table(add, "Addition table (row + col):"),
        "",
        _fmt_table(mul, "Multiplication table (row * col):"),
        "",
        "Decimal forms:",
        "Add:",
    ]
    for row in add:
        lines.append("  " + " ".join(f"{v}" for v in row))
    lines.append("Mul:")
    for row in mul:
        lines.append("  " + " ".join(f"{v}" for v in row))
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="GF(2^3) tables")
    p.add_argument(
        "--mod",
        type=lambda s: int(s, 0),
        default=0b1011,
        help="irreducible polynomial as int (default 0b1011 = x^3+x+1)",
    )
    args = p.parse_args(argv)
    text = build_report(args.mod)
    out = ROOT / "results" / "gf23_tables.txt"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"[wrote {out}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
