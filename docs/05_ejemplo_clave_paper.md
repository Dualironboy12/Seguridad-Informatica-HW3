# 05 — Ejemplo numérico (clave del paper)

Clave de referencia (Reyad et al. / Stallings):

```text
K = 0x133457799BBCDFF1
```

Ejecuta `python demo.py` y compara con esta guía. Los ciphertext de los bloques A/B están en `results/demo_output.txt`.

## 1) PC-1 (56 bits)

Valor en esta implementación (estándar Stallings; el paper imprime una variante errónea):

```text
PC-1 = 11110000110011001010101011110101010101100110011110001111
pc1_8 (8 MSB) = 11110000 = 0xF0
```

## 2) Odd/Even → Tabla III

```text
C0 = 0101010101010101010101010101
D0 = 1010101010101010101010101010
```

Concatenados (56 bits):

```text
0101010101010101010101010101 1010101010101010101010101010
```

## 3) Round keys → Tabla IV (muestra)

Tras shifts + PC-2:

```text
K1  = 011011101010110000011010010000110001100110111101
K2  = 100100010101001111100101101111001110011001000010
K15 = (igual a K1)
K16 = (igual a K2)
```

Observación didáctica: con C/D tan estructurados, muchas de las 16 subclaves **se repiten** (ver listado completo en `demo_output.txt`). Eso refuerza que el schedule no se comporta como el de DES real.

## 4) Bloques de demostración

### Block A — ASCII `SECURITY`

```text
P  = 0x5345435552495459
C  = 0xD54564886BDE8928
P' = 0x5345435552495459   (round-trip OK)
```

### Block B — hex

```text
P  = 0x0123456789ABCDEF
C  = 0x8A5CC89B96BF8B50
P' = 0x0123456789ABCDEF   (round-trip OK)
```

> Si reimplementas K-D con otro orden de bits, los ciphertext cambiarán; el round-trip debe seguir cumpliéndose y debes documentar tu decisión.

## 5) Avalanche (demo)

Flip del bit MSB de Block A → distancia de Hamming reportada por `demo.py` (típicamente del orden de decenas de bits sobre 64). Úsalo en Resultados para hablar de difusión **a pesar de** la clave colapsada.

## 6) Qué citar en el reporte

- Tabla de C0/D0/K1/K2 (este doc + `results/demo_output.txt`).
- Los dos bloques P/C/P'.
- Tiempos de keygen/encrypt/decrypt del mismo archivo.
- Nota sobre erratas del paper (PC-1 impreso vs Stallings; Listing 1 vs Tablas III/IV).

## Siguiente

[06_API_y_modulos.md](06_API_y_modulos.md)
