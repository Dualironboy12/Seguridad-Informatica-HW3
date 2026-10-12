"""Modo CBC opcional sobre bloques KE-DES de 64 bits.

IV por defecto: 8 bytes en cero (documentar en el reporte si se usa).
"""

from __future__ import annotations

from kedes.bits import from_bytes, to_bytes, xor
from kedes.cipher import decrypt_block, encrypt_block
from kedes.key_schedule import generate_keys

DEFAULT_IV = 0x0000000000000000


def _pad_pkcs7(data: bytes, block_size: int = 8) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return data + bytes([pad_len] * pad_len)


def _unpad_pkcs7(data: bytes) -> bytes:
    if not data:
        raise ValueError("datos vacíos")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 8 or data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("padding PKCS#7 inválido")
    return data[:-pad_len]


def encrypt_cbc(plaintext: bytes, key64: int, iv: int = DEFAULT_IV) -> bytes:
    """Cifra ``plaintext`` en CBC con padding PKCS#7."""
    ks = generate_keys(key64)
    data = _pad_pkcs7(plaintext)
    out = bytearray()
    prev = iv
    for i in range(0, len(data), 8):
        block = from_bytes(data[i : i + 8])
        xored = xor(block, prev)
        c = encrypt_block(xored, key64, schedule=ks)
        out.extend(to_bytes(c))
        prev = c
    return bytes(out)


def decrypt_cbc(ciphertext: bytes, key64: int, iv: int = DEFAULT_IV) -> bytes:
    """Descifra ciphertext CBC y quita padding PKCS#7."""
    if len(ciphertext) % 8 != 0:
        raise ValueError("ciphertext no alineado a 8 bytes")
    ks = generate_keys(key64)
    out = bytearray()
    prev = iv
    for i in range(0, len(ciphertext), 8):
        block = from_bytes(ciphertext[i : i + 8])
        p = decrypt_block(block, key64, schedule=ks)
        out.extend(to_bytes(xor(p, prev)))
        prev = block
    return _unpad_pkcs7(bytes(out))
