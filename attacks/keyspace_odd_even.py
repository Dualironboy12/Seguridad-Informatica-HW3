#!/usr/bin/env python3
"""Experimento: Odd/Even colapsa el espacio efectivo de subclaves."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kedes.bits import to_bin
from kedes.key_schedule import generate_keys, odd_even


def main() -> int:
    samples = [
        0x133457799BBCDFF1,
        0x0123456789ABCDEF,
        0x0000000000000000,
        0xFFFFFFFFFFFFFFFF,
        0xFEDCBA9876543210,
    ]

    oes = {odd_even(generate_keys(k).pc1) for k in samples}
    schedules = {generate_keys(k).round_keys for k in samples}
    pc1_8s = {generate_keys(k).pc1_8 for k in samples}

    lines = [
        "=== Keyspace experiment: Odd/Even ===",
        "",
        "DES teórico: ~2^56 claves efectivas (ignorando paridad).",
        "Tras Odd/Even en KE-DES (alineado a Tablas III/IV):",
        f"  Distinct Odd/Even outputs on samples : {len(oes)}",
        f"  Distinct round-key schedules         : {len(schedules)}",
        f"  Distinct pc1_8 values (for K-D)      : {len(pc1_8s)}",
        "",
        "Odd/Even output (56 bits):",
        f"  {to_bin(next(iter(oes)), 56)}",
        "",
        "Conclusión didáctica:",
        "  La transformación fija C0||D0 con independencia de la clave de entrada,",
        "  por lo que K1..K16 son idénticas para todas las claves.",
        "  Solo pc1_8 (8 bits de PC-1 previos a Odd/Even) aporta diversidad",
        "  residual vía la función K-D → a lo sumo 2^8 comportamientos distintos",
        "  por ese canal, mucho menor que 2^56.",
        "",
    ]

    text = "\n".join(lines)
    out = ROOT / "results" / "keyspace_odd_even.txt"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"[wrote {out}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
