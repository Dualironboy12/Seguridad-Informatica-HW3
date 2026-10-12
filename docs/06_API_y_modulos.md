# 06 — API y módulos

Convención general: los valores de bloques y claves son **enteros de Python**; el ancho (64, 56, 48, 32…) se indica en el nombre o en la docstring. Las tablas DES son listas de enteros **1-based**.

## `kedes.bits`

| Función | Rol |
|---|---|
| `permute(value, table, in_bits)` | Aplica tabla 1-based |
| `left_shift(value, n_bits, amount)` | Rotación izquierda |
| `split` / `join` | Partir / concatenar mitades |
| `to_bin` / `to_hex` | Formato para demos |
| `hamming_distance` | Avalanche |

## `kedes.tables`

Constantes: `IP`, `IP_INV`, `PC1`, `PC2`, `P`, `E`, `SHIFTS`, `SBOX`.  
`sbox_lookup(box_index, six_bits) -> 4 bits`.

## `kedes.key_schedule`

```python
ks = generate_keys(key64)
# ks.pc1, ks.pc1_8, ks.after_odd_even, ks.c0, ks.d0, ks.round_keys
```

- `odd_even(block56)`: salida alineada a Tabla III; **ignora** el contenido de entrada.
- `describe_schedule(ks)`: string legible.

Invariante: para cualquier `k1, k2`, `generate_keys(k1).round_keys == generate_keys(k2).round_keys`.

## `kedes.kd`

```python
kd_expand(r32, pc1_8, ki48) -> int  # 48 bits
# = pc1_8 || r32 || (ki48 >> 40) & 0xFF
```

## `kedes.cipher`

```python
encrypt_block(plaintext64, key64, schedule=None) -> ciphertext64
decrypt_block(ciphertext64, key64, schedule=None) -> plaintext64
```

Si pasas `schedule`, se reutiliza (útil en timings/CBC).

## `kedes.cbc`

```python
encrypt_cbc(plaintext_bytes, key64, iv=0) -> bytes
decrypt_cbc(ciphertext_bytes, key64, iv=0) -> bytes
```

Padding PKCS#7. IV por defecto todo cero.

## Scripts de nivel superior

| Script | Salida |
|---|---|
| `demo.py` | `results/demo_output.txt` |
| `attacks/keyspace_odd_even.py` | `results/keyspace_odd_even.txt` |
| `attacks/reduced_bruteforce.py` | `results/reduced_bruteforce.txt` |
| `attacks/sbox_diff_linear.py` | `results/sbox_diff_linear.txt` |
| `enigma/simulator.py` | stdout (demo letra a letra) |
| `gf/gf8_tables.py` | `results/gf23_tables.txt` |
| `tests/run_all.py` | OK/FAIL por test |

## Siguiente

[07_ataques_educativos.md](07_ataques_educativos.md)
