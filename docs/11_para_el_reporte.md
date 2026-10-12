# 11 — Puente hacia el reporte PDF del curso

Este documento **no** es el entregable de Blackboard. Indica de dónde sacar figuras, tablas y párrafos técnicos para armar el PDF con las secciones pedidas (portada, abstract, intro, metodología, resultados, conclusiones, bibliografía).

## Portada y forma

Sigue `Instrucciones.txt`: Title + Homework #3, nombres, IDs, curso, fecha, Autumn Term.  
Nombre de archivo: `HW3_ID_ID_ID.pdf`. **Cada** integrante sube el mismo PDF.

## Abstract / Introduction

Insumos:

- Definición KE-DES en [03_KE-DES_diferencias.md](03_KE-DES_diferencias.md).
- Objetivo de aprendizaje en [00_indice.md](00_indice.md).
- Referencias Stallings + Reyad et al.

## Methodology

| Qué describir | Fuente |
|---|---|
| DES/Feistel base | [02_DES_y_Feistel.md](02_DES_y_Feistel.md) + diagrama propio |
| Odd/Even y decisión frente al paper | [03](03_KE-DES_diferencias.md), docstring de `key_schedule.py` |
| Orden K-D 8+32+8 | [03](03_KE-DES_diferencias.md), `kedes/kd.py` |
| Entorno y procedimiento de timings | `results/demo_output.txt` |
| Diseño de ataques educativos | [07_ataques_educativos.md](07_ataques_educativos.md) |
| Enigma + GF(2³) | [08](08_Enigma.md), [09](09_GF23.md) |

## Results and discussion

| Resultado | Archivo |
|---|---|
| Schedule C0/D0/Kᵢ | `results/demo_output.txt` |
| 2 bloques P/C/P' | idem |
| Timings keygen/enc/dec | idem |
| Avalanche | idem |
| Colapso de keyspace | `results/keyspace_odd_even.txt` |
| Brute-force reducido | `results/reduced_bruteforce.txt` |
| DDT / bias S-boxes | `results/sbox_diff_linear.txt` |
| Tablas GF | `results/gf23_tables.txt` (apéndice) |
| Ejemplo Enigma | salida de `enigma/simulator.py` |

Discute: relación KE-DES–DES; por qué Odd/Even invalida la promesa de “enhancement”.

## Conclusions

Qué aprendieron sobre Feistel, entropía efectiva, y límites de “mejoras” ad hoc. Limitaciones: ambigüedad K-D del paper, alcance educativo de los ataques.

## Bibliography (mínimo)

1. Stallings, *Cryptography and Network Security*.
2. Reyad et al., IEEE NCCC 2021 (DOI 10.1109/NCCC49330.2021.9428818).
3. Material del curso (PP slide 124).
4. Fuentes Enigma históricas/académicas que usen.

Cita cada una en el texto principal.

## Checklist final antes de subir

- [ ] Round-trip OK en demo
- [ ] Tests `python tests/run_all.py` en verde
- [ ] Figuras/tablas numeradas y mencionadas en el texto
- [ ] Apéndice GF(2³) con irreducible declarado
- [ ] Los 3 IDs en el nombre del PDF y los 3 suben a Blackboard
