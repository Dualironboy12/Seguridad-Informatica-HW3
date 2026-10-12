# HW3 — KE-DES, criptoanálisis educativo, Enigma y GF(2³)

Implementación desde cero (Python 3, sin librerías DES) del esquema **KE-DES** (Reyad et al., 2021), demos, experimentos de laboratorio, simulador Enigma mínimo, tablas GF(2³) y documentación didáctica para estudiantes de ingeniería en sistemas.

## Decisión K-D (importante)

```text
K-D = pc1_8 || R_32 || Ki_top8
```

Documentada en [`kedes/kd.py`](kedes/kd.py) y [`docs/03_KE-DES_diferencias.md`](docs/03_KE-DES_diferencias.md).

## Quickstart

```bash
cd HW3
python tests/run_all.py          # vectores del paper + round-trip
python demo.py                   # 2 bloques, timings, avalanche → results/
python attacks/keyspace_odd_even.py
python attacks/reduced_bruteforce.py
python attacks/sbox_diff_linear.py
python enigma/simulator.py HI
python gf/gf8_tables.py          # verificar irreducible vs PP slide 124
```

Requisito: Python 3.10+ recomendado (probado en 3.12). Solo biblioteca estándar.

## Documentación (empieza aquí para aprender)

**Índice didáctico:** [`docs/00_indice.md`](docs/00_indice.md)

Ahí encontrarás rutas de lectura rápida/profunda, teoría Feistel/KE-DES, walkthrough de implementación, API, ataques, Enigma, GF(2³), glosario y guía para armar el PDF del curso.

## Layout

| Ruta | Contenido |
|---|---|
| `kedes/` | Bits, tablas DES, key schedule, K-D, cipher, CBC |
| `attacks/` | Keyspace, brute-force reducido, DDT/LAT |
| `enigma/` | Simulador Enigma I mínimo |
| `gf/` | Tablas GF(2³) |
| `tests/` | Verificación Tablas III/IV + round-trip |
| `docs/` | Documentación didáctica completa |
| `results/` | Salidas listas para citar en el reporte |

## Checklist de verificación

- [ ] `python tests/run_all.py` → 7/7 passed
- [ ] `demo.py` round-trip OK en Block A y B
- [ ] Existen archivos bajo `results/`
- [ ] Entiendes Odd/Even y el orden K-D (docs 03 y 05)
- [ ] GF: irreducible contrastado con slide 124

## Referencias

1. Stallings, *Cryptography and Network Security*.
2. Reyad, Mansour, Heshmat, Zanaty — *Key-Based Enhancement of Data Encryption Standard for Text Security*, IEEE NCCC 2021.
3. Enunciado del curso: `HW3 LIS4062 Autumn 26.pdf`, `Instrucciones.txt`.

## Nota académica

KE-DES **no es seguro**; el colapso de clave por Odd/Even es intencionalmente visible en esta implementación alineada a las Tablas III/IV del paper. El propósito es aprender, no proteger datos reales.
