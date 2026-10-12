#!/usr/bin/env python3
"""Demo KE-DES: 2 bloques de 64 bits, timings, avalanche y salida a results/."""

from __future__ import annotations

import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kedes.bits import hamming_distance, to_bytes, to_hex
from kedes.cipher import decrypt_block, encrypt_block
from kedes.key_schedule import describe_schedule, generate_keys

PAPER_KEY = 0x133457799BBCDFF1
BLOCK_A = int.from_bytes(b"SECURITY", "big")
BLOCK_B = 0x0123456789ABCDEF
TIMING_ROUNDS = 2000


def _mean_time(fn, n: int = TIMING_ROUNDS) -> float:
    t0 = time.perf_counter()
    for _ in range(n):
        fn()
    return (time.perf_counter() - t0) / n


def run_block(name: str, plaintext: int, key: int, ks) -> list[str]:
    c = encrypt_block(plaintext, key, schedule=ks)
    p2 = decrypt_block(c, key, schedule=ks)
    ok = p2 == plaintext
    lines = [
        f"=== {name} ===",
        f"Plaintext  : 0x{to_hex(plaintext, 64)}  bytes={to_bytes(plaintext)!r}",
        f"Key        : 0x{to_hex(key, 64)}",
        f"Ciphertext : 0x{to_hex(c, 64)}",
        f"Decrypted  : 0x{to_hex(p2, 64)}",
        f"Round-trip : {'OK' if ok else 'FAIL'}",
        "",
    ]
    return lines


def main() -> int:
    lines: list[str] = []
    lines.append("KE-DES Demo — HW3 LIS4062")
    lines.append(f"Host     : {platform.node()}")
    lines.append(f"OS       : {platform.system()} {platform.release()}")
    lines.append(f"Machine  : {platform.machine()}")
    lines.append(f"Processor: {platform.processor() or 'n/a'}")
    lines.append(f"Python   : {platform.python_version()}")
    lines.append("")

    t_keygen = _mean_time(lambda: generate_keys(PAPER_KEY))
    ks = generate_keys(PAPER_KEY)

    lines.append("--- Key schedule (paper key 0x133457799BBCDFF1) ---")
    lines.append(describe_schedule(ks))
    lines.append("")
    lines.append(f"Avg key generation time ({TIMING_ROUNDS} runs): {t_keygen * 1e3:.6f} ms")
    lines.append("")

    lines.extend(run_block("Block A (ASCII 'SECURITY')", BLOCK_A, PAPER_KEY, ks))
    lines.extend(run_block("Block B (hex 0123456789ABCDEF)", BLOCK_B, PAPER_KEY, ks))

    t_enc = _mean_time(lambda: encrypt_block(BLOCK_A, PAPER_KEY, schedule=ks))
    c_a = encrypt_block(BLOCK_A, PAPER_KEY, schedule=ks)
    t_dec = _mean_time(lambda: decrypt_block(c_a, PAPER_KEY, schedule=ks))
    lines.append("--- Timings (Block A, schedule reused) ---")
    lines.append(f"Avg encrypt: {t_enc * 1e3:.6f} ms")
    lines.append(f"Avg decrypt: {t_dec * 1e3:.6f} ms")
    lines.append("")

    # Avalanche: flip MSB of plaintext
    p_flip = BLOCK_A ^ (1 << 63)
    c_flip = encrypt_block(p_flip, PAPER_KEY, schedule=ks)
    dist = hamming_distance(c_a, c_flip, 64)
    lines.append("--- Avalanche (1-bit plaintext flip) ---")
    lines.append(f"Original C : 0x{to_hex(c_a, 64)}")
    lines.append(f"Flipped  C : 0x{to_hex(c_flip, 64)}")
    lines.append(f"Hamming distance: {dist} / 64 bits ({100 * dist / 64:.1f}%)")
    lines.append("")

    # Distinct pc1_8 across keys (K-D still key-dependent)
    ks2 = generate_keys(0x0123456789ABCDEF)
    lines.append("--- Note on Odd/Even collapse ---")
    lines.append(f"Round keys identical across keys? {ks.round_keys == ks2.round_keys}")
    lines.append(f"pc1_8 paper key : 0x{ks.pc1_8:02X}")
    lines.append(f"pc1_8 other key : 0x{ks2.pc1_8:02X}")
    lines.append("K-D still mixes pc1_8, so ciphertexts can differ even if Ki match.")
    lines.append("")

    text = "\n".join(lines)
    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "demo_output.txt"
    out_path.write_text(text, encoding="utf-8")
    print(text)
    print(f"[wrote {out_path}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
