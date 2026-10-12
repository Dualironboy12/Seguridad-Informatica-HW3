"""Vectores de verificación del paper KE-DES y round-trip."""

from __future__ import annotations

import random

from kedes.bits import to_bin
from kedes.cipher import decrypt_block, encrypt_block
from kedes.key_schedule import generate_keys, odd_even

PAPER_KEY = 0x133457799BBCDFF1

# Tabla III
C0 = "0101010101010101010101010101"
D0 = "1010101010101010101010101010"

# Tabla IV
K1 = "011011101010110000011010010000110001100110111101"
K2 = "100100010101001111100101101111001110011001000010"
K15 = K1
K16 = K2

# Stallings classic PC-1 for this key (paper has a typographical error)
STALLINGS_PC1_PREFIX_C = "1111000011001100101010101111"
STALLINGS_PC1_PREFIX_D = "0101010101100110011110001111"


def test_pc1_matches_stallings_example():
    ks = generate_keys(PAPER_KEY)
    assert to_bin(ks.pc1, 56) == STALLINGS_PC1_PREFIX_C + STALLINGS_PC1_PREFIX_D


def test_odd_even_matches_table_iii():
    oe = odd_even(0)  # input ignored
    assert to_bin(oe, 56) == C0 + D0
    ks = generate_keys(PAPER_KEY)
    assert to_bin(ks.c0, 28) == C0
    assert to_bin(ks.d0, 28) == D0


def test_round_keys_match_table_iv():
    ks = generate_keys(PAPER_KEY)
    assert to_bin(ks.round_keys[0], 48) == K1
    assert to_bin(ks.round_keys[1], 48) == K2
    assert to_bin(ks.round_keys[14], 48) == K15
    assert to_bin(ks.round_keys[15], 48) == K16


def test_round_trip_security_block():
    p = int.from_bytes(b"SECURITY", "big")
    c = encrypt_block(p, PAPER_KEY)
    assert decrypt_block(c, PAPER_KEY) == p


def test_round_trip_hex_block():
    p = 0x0123456789ABCDEF
    c = encrypt_block(p, PAPER_KEY)
    assert decrypt_block(c, PAPER_KEY) == p


def test_round_trip_random_blocks():
    rng = random.Random(0)
    key = PAPER_KEY
    for _ in range(20):
        p = rng.getrandbits(64)
        assert decrypt_block(encrypt_block(p, key), key) == p


def test_all_keys_share_round_keys_after_odd_even():
    """Odd/Even colapsa el schedule: K_i idénticas para claves distintas."""
    ks_a = generate_keys(0x133457799BBCDFF1)
    ks_b = generate_keys(0x0123456789ABCDEF)
    assert ks_a.round_keys == ks_b.round_keys
    # pc1_8 sí puede diferir (afecta K-D)
    assert isinstance(ks_a.pc1_8, int)
