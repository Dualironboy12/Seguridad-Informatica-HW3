"""KE-DES: Key-Based Enhancement of DES (implementación educativa HW3)."""

from kedes.cipher import decrypt_block, encrypt_block
from kedes.key_schedule import KeySchedule, generate_keys
from kedes.kd import kd_expand

__all__ = [
    "KeySchedule",
    "generate_keys",
    "kd_expand",
    "encrypt_block",
    "decrypt_block",
]
