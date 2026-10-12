"""Función Key-Distribution (K-D): reemplazo de la expansión E en KE-DES.

Decisión de implementación (documentar en el reporte)
----------------------------------------------------
El paper no fija el orden de concatenación de los tres aportes (8 + 32 + 8).
Adoptamos:

    K-D(R, pc1_8, Ki) = pc1_8 || R_32 || Ki[0:8]

donde ``Ki[0:8]`` son los 8 bits más significativos de la subclave de ronda
(tras PC-2), y ``pc1_8`` son los 8 bits más significativos del resultado de
PC-1 (antes de Odd/Even), constantes en todas las rondas.
"""

from __future__ import annotations

from kedes.bits import join


def kd_expand(r32: int, pc1_8: int, ki48: int) -> int:
    """Construye el bloque de 48 bits que sustituye a E(R) en DES.

    Args:
        r32: mitad derecha de 32 bits.
        pc1_8: 8 bits fijos tomados de PC-1.
        ki48: subclave de ronda (48 bits); se usan los 8 MSB.

    Returns:
        Entero de 48 bits = pc1_8 || r32 || ki_top8.

    Example:
        >>> kd_expand(0, 0xAB, 0xF00000000000)  # doctest: +SKIP
    """
    ki_top8 = (ki48 >> 40) & 0xFF
    # pc1_8 (8) || r32 (32) || ki_top8 (8)  => 48 bits
    return join(join(pc1_8 & 0xFF, r32 & 0xFFFFFFFF, 32), ki_top8, 8)
