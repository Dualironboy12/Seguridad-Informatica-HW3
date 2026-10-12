"""Cifrado y descifrado de un bloque de 64 bits con KE-DES."""

from __future__ import annotations

from kedes.bits import join, permute, split, xor
from kedes.kd import kd_expand
from kedes.key_schedule import KeySchedule, generate_keys
from kedes.tables import IP, IP_INV, P, sbox_lookup


def _sboxes(block48: int) -> int:
    """Aplica las 8 S-boxes a 48 bits; retorna 32 bits."""
    out = 0
    for i in range(8):
        shift = 42 - 6 * i  # chunks from MSB: bits 47..42, 41..36, ...
        six = (block48 >> shift) & 0x3F
        out = (out << 4) | sbox_lookup(i, six)
    return out


def f_function(r32: int, ki48: int, pc1_8: int) -> int:
    """Función f de KE-DES: K-D → XOR Ki → S-boxes → P."""
    expanded = kd_expand(r32, pc1_8, ki48)
    mixed = xor(expanded, ki48)
    substituted = _sboxes(mixed)
    return permute(substituted, P, 32)


def _feistel(block64: int, round_keys: tuple[int, ...], pc1_8: int) -> int:
    """16 rondas Feistel + IP / IP⁻¹. ``round_keys`` ya en el orden deseado."""
    state = permute(block64, IP, 64)
    left, right = split(state, 32, 32)

    for ki in round_keys:
        new_right = xor(left, f_function(right, ki, pc1_8))
        left = right
        right = new_right

    # Swap final: R16 || L16
    preoutput = join(right, left, 32)
    return permute(preoutput, IP_INV, 64)


def encrypt_block(plaintext64: int, key64: int, schedule: KeySchedule | None = None) -> int:
    """Cifra un bloque de 64 bits.

    Example:
        >>> c = encrypt_block(0x0123456789ABCDEF, 0x133457799BBCDFF1)
        >>> decrypt_block(c, 0x133457799BBCDFF1) == 0x0123456789ABCDEF
        True
    """
    ks = schedule if schedule is not None else generate_keys(key64)
    return _feistel(plaintext64, ks.round_keys, ks.pc1_8)


def decrypt_block(ciphertext64: int, key64: int, schedule: KeySchedule | None = None) -> int:
    """Descifra un bloque de 64 bits (claves en orden inverso)."""
    ks = schedule if schedule is not None else generate_keys(key64)
    reversed_keys = tuple(reversed(ks.round_keys))
    return _feistel(ciphertext64, reversed_keys, ks.pc1_8)
