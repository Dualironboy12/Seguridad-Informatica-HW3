#!/usr/bin/env python3
"""DDT y aproximación lineal básica de las S-boxes DES (nivel curso)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kedes.tables import SBOX, sbox_lookup


def ddt(box_index: int) -> list[list[int]]:
    """Difference Distribution Table: 64x16 counts for (din -> dout)."""
    table = [[0] * 16 for _ in range(64)]
    for x in range(64):
        y = sbox_lookup(box_index, x)
        for din in range(64):
            x2 = x ^ din
            y2 = sbox_lookup(box_index, x2)
            dout = y ^ y2
            table[din][dout] += 1
    return table


def max_ddt_entry(table: list[list[int]]) -> tuple[int, int, int]:
    best = (0, 0, 0)  # count, din, dout
    for din in range(64):
        for dout in range(16):
            if din == 0 and dout == 0:
                continue
            c = table[din][dout]
            if c > best[0]:
                best = (c, din, dout)
    return best


def lat_bias(box_index: int) -> tuple[float, int, int]:
    """Mejor bias lineal no trivial |Pr[<a,x>=<b,S(x)>] - 1/2|."""
    best = (0.0, 0, 0)  # bias, a, b
    for a in range(64):
        for b in range(16):
            if a == 0 and b == 0:
                continue
            agree = 0
            for x in range(64):
                y = sbox_lookup(box_index, x)
                ax = bin(a & x).count("1") & 1
                by = bin(b & y).count("1") & 1
                if ax == by:
                    agree += 1
            bias = abs(agree / 64.0 - 0.5)
            if bias > best[0]:
                best = (bias, a, b)
    return best


def main() -> int:
    lines = [
        "=== S-box differential & linear analysis (educational) ===",
        "",
        "Intuición diferencial: ¿qué tan a menudo una diferencia de entrada",
        "din produce una diferencia de salida dout? La DDT cuenta eso.",
        "Intuición lineal: ¿qué tan a menudo una combinación XOR de bits de",
        "entrada coincide con una de salida? El bias mide el sesgo respecto a 1/2.",
        "",
    ]

    for i in range(8):
        table = ddt(i)
        count, din, dout = max_ddt_entry(table)
        bias, a, b = lat_bias(i)
        lines.append(
            f"S{i+1}: max DDT count={count}/64 "
            f"(din=0x{din:02X} -> dout=0x{dout:X})  "
            f"prob≈{count/64:.3f};  "
            f"best linear bias={bias:.3f} (a=0x{a:02X}, b=0x{b:X})"
        )

    lines.extend(
        [
            "",
            "Lectura para KE-DES:",
            "  Las S-boxes son las mismas que DES, así que las DDT/LAT locales",
            "  coinciden. Lo que cambia es la expansión: K-D inyecta bits de clave",
            "  (pc1_8 y 8 bits de Ki) junto a R, en lugar de la E fija de DES.",
            "  Eso altera cómo se propagan diferencias/aproximaciones entre rondas,",
            "  pero la debilidad dominante de KE-DES es el colapso de clave por Odd/Even,",
            "  no un rediseño de las S-boxes.",
            "",
            "Limitación académica: esto NO es un ataque completo de 16 rondas;",
            "sirve para entender las piezas y discutir el paper con rigor de curso.",
            "",
        ]
    )

    text = "\n".join(lines)
    out = ROOT / "results" / "sbox_diff_linear.txt"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"[wrote {out}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
