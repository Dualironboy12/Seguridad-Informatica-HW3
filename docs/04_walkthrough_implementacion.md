# 04 — Walkthrough de la implementación

## Estructura del repo

```text
HW3/
  kedes/           núcleo del cifrador
  attacks/         experimentos educativos
  enigma/          simulador Enigma
  gf/              tablas GF(2³)
  tests/           vectores del paper + round-trip
  docs/            esta documentación
  results/         salidas para el reporte
  demo.py          demo principal
```

## Orden recomendado (como se construyó)

### Paso 1 — Bits y tablas

Archivos: `kedes/bits.py`, `kedes/tables.py`.

- `permute(value, table, in_bits)` resta 1 a índices 1-based.
- Tablas: IP, IP_INV, PC1, PC2, P, SBOX, SHIFTS.

**Debes poder explicar:** qué es MSB en un entero de n bits.

### Paso 2 — Key schedule (gate crítico)

Archivo: `kedes/key_schedule.py`.

```bash
python tests/run_all.py
```

Deben pasar:

- `test_pc1_matches_stallings_example`
- `test_odd_even_matches_table_iii`
- `test_round_keys_match_table_iv`

Si falla Tabla IV pero C0/D0 OK → revisar shifts/PC-2.  
Si falla C0/D0 → revisar Odd/Even.  
Si falla PC-1 → revisar tabla PC1 o endianness de la clave.

**No avances al cifrado sin este gate.**

### Paso 3 — K-D + Feistel

Archivos: `kedes/kd.py`, `kedes/cipher.py`.

Flujo encrypt:

1. IP  
2. 16× (`R_new = L ⊕ f_KD(R, Ki)`, `L = R_old`)  
3. `R16||L16` → IP⁻¹  

Decrypt: igual con `reversed(round_keys)`.

Tests: `test_round_trip_*`.

### Paso 4 — Demo

```bash
python demo.py
```

Genera `results/demo_output.txt` con 2 bloques, timings y avalanche.

### Paso 5 — Ataques educativos

```bash
python attacks/keyspace_odd_even.py
python attacks/reduced_bruteforce.py
python attacks/sbox_diff_linear.py
```

### Paso 6 — Enigma y GF

```bash
python enigma/simulator.py HI
python gf/gf8_tables.py
```

## CBC (opcional)

`kedes/cbc.py`: CBC + PKCS#7, IV por defecto 0. Útil si quieren un archivo multi-bloque; la HW mínima pide 2 bloques de 64 bits.

## Checklist de aprendizaje

- [ ] Sé qué test falla si PC-2 está mal.
- [ ] Sé por qué `generate_keys(k1).round_keys == generate_keys(k2).round_keys`.
- [ ] Sé dónde se usa `pc1_8` (solo en K-D, no en Odd/Even).

## Siguiente

[05_ejemplo_clave_paper.md](05_ejemplo_clave_paper.md)
