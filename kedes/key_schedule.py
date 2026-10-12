"""Generación de subclaves KE-DES (PC-1, Odd/Even, shifts, PC-2).

Nota sobre Odd/Even y el paper Reyad et al. (2021)
-------------------------------------------------
El Listing 1 del paper, aplicado literalmente a 56 bits, produce el patrón
uniforme ``010101...`` y por tanto C0 == D0. Eso **no** reproduce la Tabla III
(D0 = ``1010...``) ni las round keys de la Tabla IV.

La implementación sigue las **Tablas III y IV publicadas** como verdad de
verificación: tras Odd/Even,

- C0 = ``0101010101010101010101010101`` (28 bits)
- D0 = ``1010101010101010101010101010`` (28 bits)

Es decir, la mitad izquierda alterna 01 y la derecha alterna 10. Al igual que
el Listing 1, el resultado **no depende del valor de los bits de entrada**:
la entropía de la clave colapsa (hallazgo central para el análisis).

PC-1 se implementa con la tabla DES estándar (FIPS 46 / Stallings). El valor
de PC-1 mostrado en el paper para la clave ejemplo difiere por una errata
tipográfica; nuestro PC-1 coincide con el ejemplo clásico de Stallings.
"""

from __future__ import annotations

from dataclasses import dataclass

from kedes.bits import join, left_shift, permute, set_bit, split, to_bin
from kedes.tables import PC1, PC2, SHIFTS


def _alternating_01(n_bits: int) -> int:
    """Patrón 0101... de ``n_bits`` (posición 1-based impar = 0, par = 1)."""
    out = 0
    for j in range(1, n_bits + 1):
        bit = 0 if (j % 2 == 1) else 1
        out = set_bit(out, j, n_bits, bit)
    return out


def _alternating_10(n_bits: int) -> int:
    """Patrón 1010... de ``n_bits`` (posición 1-based impar = 1, par = 0)."""
    out = 0
    for j in range(1, n_bits + 1):
        bit = 1 if (j % 2 == 1) else 0
        out = set_bit(out, j, n_bits, bit)
    return out


def odd_even(block56: int) -> int:
    """Transformación Odd/Even alineada a Tablas III/IV del paper.

    El argumento ``block56`` se ignora a propósito (colapso de entropía),
    igual que el espíritu del Listing 1 del paper.

    Returns:
        Entero de 56 bits = C0 || D0 con los patrones de la Tabla III.
    """
    _ = block56  # entrada descartada: la salida no depende de la clave
    c0 = _alternating_01(28)
    d0 = _alternating_10(28)
    return join(c0, d0, 28)


@dataclass(frozen=True)
class KeySchedule:
    """Resultado del schedule de claves KE-DES."""

    pc1: int  # 56 bits post PC-1 (antes de Odd/Even)
    pc1_8: int  # primeros 8 bits de pc1 (constantes en K-D)
    after_odd_even: int  # 56 bits
    c0: int
    d0: int
    round_keys: tuple[int, ...]  # 16 claves de 48 bits (K1..K16)


def generate_keys(key64: int) -> KeySchedule:
    """Genera K1..K16 a partir de una clave de 64 bits.

    Example:
        >>> ks = generate_keys(0x133457799BBCDFF1)
        >>> len(ks.round_keys)
        16
    """
    pc1 = permute(key64, PC1, 64)
    pc1_8 = (pc1 >> 48) & 0xFF  # top 8 bits of 56-bit value
    oe = odd_even(pc1)
    c0, d0 = split(oe, 28, 28)

    c, d = c0, d0
    keys: list[int] = []
    for shift in SHIFTS:
        c = left_shift(c, 28, shift)
        d = left_shift(d, 28, shift)
        cd = join(c, d, 28)
        keys.append(permute(cd, PC2, 56))

    return KeySchedule(
        pc1=pc1,
        pc1_8=pc1_8,
        after_odd_even=oe,
        c0=c0,
        d0=d0,
        round_keys=tuple(keys),
    )


def describe_schedule(ks: KeySchedule) -> str:
    """Resumen legible del schedule (útil para demos/docs)."""
    lines = [
        f"PC-1:       {to_bin(ks.pc1, 56)}",
        f"PC1_8:      {to_bin(ks.pc1_8, 8)}",
        f"Odd/Even:   {to_bin(ks.after_odd_even, 56)}",
        f"C0:         {to_bin(ks.c0, 28)}",
        f"D0:         {to_bin(ks.d0, 28)}",
    ]
    for i, k in enumerate(ks.round_keys, start=1):
        lines.append(f"K{i:02d}:        {to_bin(k, 48)}")
    return "\n".join(lines)
