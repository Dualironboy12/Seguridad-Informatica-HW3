"""Utilidades de manipulación de bits para KE-DES.

Las tablas DES usan índices 1-based (la posición 1 es el bit más
significativo). ``permute`` convierte eso a índices 0-based internamente.
"""

from __future__ import annotations


def mask(n_bits: int) -> int:
    """Máscara con los ``n_bits`` bits bajos en 1."""
    return (1 << n_bits) - 1


def get_bit(value: int, position: int, n_bits: int) -> int:
    """Devuelve el bit en posición 1-based (1 = MSB de un bloque de n_bits)."""
    shift = n_bits - position
    return (value >> shift) & 1


def set_bit(value: int, position: int, n_bits: int, bit: int) -> int:
    """Pone el bit 1-based ``position`` a ``bit`` (0 o 1)."""
    shift = n_bits - position
    if bit:
        return value | (1 << shift)
    return value & ~(1 << shift)


def permute(value: int, table: list[int], in_bits: int) -> int:
    """Aplica una tabla de permutación 1-based.

    Args:
        value: entero de entrada.
        table: lista de posiciones de origen (1-based) en orden de salida.
        in_bits: ancho en bits del valor de entrada.

    Returns:
        Entero de ``len(table)`` bits.

    Example:
        >>> permute(0b1010, [4, 1, 2, 3], 4)
        0b0101
    """
    out = 0
    for src_pos in table:
        out = (out << 1) | get_bit(value, src_pos, in_bits)
    return out


def left_shift(value: int, n_bits: int, amount: int) -> int:
    """Rotación a la izquierda de ``amount`` bits sobre un bloque de ``n_bits``."""
    amount %= n_bits
    m = mask(n_bits)
    value &= m
    return ((value << amount) | (value >> (n_bits - amount))) & m


def split(value: int, left_bits: int, right_bits: int) -> tuple[int, int]:
    """Parte ``value`` en (izquierda, derecha) con los anchos dados."""
    right = value & mask(right_bits)
    left = (value >> right_bits) & mask(left_bits)
    return left, right


def join(left: int, right: int, right_bits: int) -> int:
    """Concatena ``left || right`` donde ``right`` tiene ``right_bits``."""
    return (left << right_bits) | (right & mask(right_bits))


def xor(a: int, b: int) -> int:
    """XOR de enteros."""
    return a ^ b


def bit_count(value: int) -> int:
    """Número de bits en 1 (popcount)."""
    return value.bit_count()


def to_bin(value: int, n_bits: int) -> str:
    """Representación binaria con ceros a la izquierda."""
    return format(value & mask(n_bits), f"0{n_bits}b")


def to_hex(value: int, n_bits: int) -> str:
    """Hex mayúsculas con ancho acorde a ``n_bits``."""
    nibbles = (n_bits + 3) // 4
    return format(value & mask(n_bits), f"0{nibbles}X")


def from_bytes(data: bytes) -> int:
    """8 bytes big-endian -> entero 64-bit."""
    if len(data) != 8:
        raise ValueError("se esperan exactamente 8 bytes")
    return int.from_bytes(data, "big")


def to_bytes(value: int) -> bytes:
    """Entero 64-bit -> 8 bytes big-endian."""
    return (value & mask(64)).to_bytes(8, "big")


def hamming_distance(a: int, b: int, n_bits: int = 64) -> int:
    """Distancia de Hamming entre dos valores de ``n_bits``."""
    return bit_count((a ^ b) & mask(n_bits))
