#!/usr/bin/env python3
"""Fuerza bruta educativa sobre un espacio artificialmente reducido.

No intenta romper sistemas reales. Mide tiempo vs n bits libres de pc1_8
(el único residuo de diversidad de clave tras Odd/Even en esta implementación).
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kedes.bits import join, left_shift, permute, split
from kedes.cipher import encrypt_block
from kedes.key_schedule import KeySchedule, odd_even
from kedes.tables import PC2, SHIFTS


def _schedule_with_pc1_8(pc1_8: int) -> KeySchedule:
    """Construye un schedule con pc1_8 forzado; round keys fijas post-OE."""
    # PC-1 dummy: top 8 bits = pc1_8, resto 0 (solo importa pc1_8 para K-D)
    pc1 = (pc1_8 & 0xFF) << 48
    oe = odd_even(pc1)
    c0, d0 = split(oe, 28, 28)
    c, d = c0, d0
    keys = []
    for shift in SHIFTS:
        c = left_shift(c, 28, shift)
        d = left_shift(d, 28, shift)
        keys.append(permute(join(c, d, 28), PC2, 56))
    return KeySchedule(
        pc1=pc1,
        pc1_8=pc1_8 & 0xFF,
        after_odd_even=oe,
        c0=c0,
        d0=d0,
        round_keys=tuple(keys),
    )


def recover_pc1_8(plaintext: int, ciphertext: int, n_bits: int) -> tuple[int | None, float, int]:
    """Prueba 2^n_bits candidatos en los n_bits bajos de pc1_8."""
    space = 1 << n_bits
    t0 = time.perf_counter()
    for cand in range(space):
        ks = _schedule_with_pc1_8(cand)
        if encrypt_block(plaintext, 0, schedule=ks) == ciphertext:
            return cand, time.perf_counter() - t0, space
    return None, time.perf_counter() - t0, space


def main() -> int:
    plaintext = int.from_bytes(b"SECURITY", "big")
    secret_pc1_8 = 0x2A  # secreto de laboratorio
    ks_true = _schedule_with_pc1_8(secret_pc1_8)
    ciphertext = encrypt_block(plaintext, 0, schedule=ks_true)

    lines = [
        "=== Reduced brute-force (educational) ===",
        f"Plaintext : 0x{plaintext:016X}",
        f"Ciphertext: 0x{ciphertext:016X}",
        f"Secret pc1_8 (low bits searched): 0x{secret_pc1_8:02X}",
        "",
        f"{'n_bits':>6}  {'space':>8}  {'found':>6}  {'seconds':>10}",
    ]

    for n in (8, 10, 12, 14):
        # For n>8 we still only have 8 real bits; pad search to show scaling
        # by searching n bits where only low 8 matter — use masked secret.
        target = secret_pc1_8 & ((1 << min(n, 8)) - 1)
        # Rebuild ciphertext for the masked target when n < 8
        ks_t = _schedule_with_pc1_8(target)
        ct = encrypt_block(plaintext, 0, schedule=ks_t)
        found, elapsed, space = recover_pc1_8(plaintext, ct, min(n, 8) if n <= 8 else 8)
        # Explicit scaling demos for n=8 only meaningful; for larger n simulate
        # by reporting extrapolated 2^n * time_per_guess from n=8 run
        if n == 8:
            t_per = elapsed / space
            lines.append(f"{n:6d}  {space:8d}  {found!s:>6}  {elapsed:10.6f}")
            base_t_per = t_per
        else:
            space_n = 1 << n
            est = base_t_per * space_n
            lines.append(
                f"{n:6d}  {space_n:8d}  {'(est)':>6}  {est:10.6f}  "
                f"# extrapolated from {base_t_per:.3e} s/guess"
            )

    lines.extend(
        [
            "",
            "Interpretación:",
            "  Tras Odd/Even, atacar las subclaves Ki por fuerza bruta no aporta:",
            "  son fijas. El residuo searchable aquí es pc1_8 (8 bits) vía K-D.",
            "  En DES clásico el espacio sería ~2^56; la diferencia ilustra por qué",
            "  KE-DES no es criptográficamente seguro.",
            "",
        ]
    )

    text = "\n".join(lines)
    out = ROOT / "results" / "reduced_bruteforce.txt"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"[wrote {out}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
