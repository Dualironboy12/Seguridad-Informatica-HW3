# Documentación técnica HW3 — Índice

**Curso:** LIS4062 Information Security (Autumn 2026)  
**Tema:** KE-DES (Key-Based Enhancement of DES), criptoanálisis educativo, Enigma y GF(2³)  
**Público:** estudiantes de ingeniería en sistemas / computación

Esta carpeta explica la parte técnica del proyecto de forma **didáctica e intuitiva**, ligada al código en el repositorio. No sustituye el reporte PDF formal de Blackboard; sirve para **aprender** y para redactar Metodología/Resultados con criterio.

## Prerrequisitos sugeridos

- Programación en Python a nivel introductorio (funciones, enteros, módulos).
- Matemática discreta básica: módulo, XOR, representación binaria.
- No se asume que ya hayas cursado criptografía avanzada.

## Ruta rápida (≈ 1–2 horas)

1. [01_conceptos_previos.md](01_conceptos_previos.md) — solo secciones de XOR, bloque y confusión/difusión.
2. [02_DES_y_Feistel.md](02_DES_y_Feistel.md) — idea Feistel + una ronda.
3. [03_KE-DES_diferencias.md](03_KE-DES_diferencias.md) — Odd/Even y K-D.
4. Ejecutar `python demo.py` y leer [05_ejemplo_clave_paper.md](05_ejemplo_clave_paper.md).
5. [07_ataques_educativos.md](07_ataques_educativos.md) — conclusiones de seguridad.

## Ruta profunda (implementar / defender el reporte)

Sigue el orden numerado 01 → 11. Usa [04_walkthrough_implementacion.md](04_walkthrough_implementacion.md) mientras lees el código.

## Mapa de documentos

| Doc | Contenido |
|---|---|
| [01_conceptos_previos.md](01_conceptos_previos.md) | Simétrico/asimétrico, XOR, permutación, Shannon |
| [02_DES_y_Feistel.md](02_DES_y_Feistel.md) | DES clásico y por qué el descifrado funciona |
| [03_KE-DES_diferencias.md](03_KE-DES_diferencias.md) | Odd/Even, K-D, decisión 8+32+8, erratas del paper |
| [04_walkthrough_implementacion.md](04_walkthrough_implementacion.md) | Cómo está armado el repo y qué test debe pasar |
| [05_ejemplo_clave_paper.md](05_ejemplo_clave_paper.md) | Walkthrough numérico con la clave del paper |
| [06_API_y_modulos.md](06_API_y_modulos.md) | Contrato de cada módulo Python |
| [07_ataques_educativos.md](07_ataques_educativos.md) | Fuerza bruta, diferencial, lineal |
| [08_Enigma.md](08_Enigma.md) | Máquina Enigma y simulador |
| [09_GF23.md](09_GF23.md) | Campo GF(2³) y tablas del apéndice |
| [10_glosario_y_faq.md](10_glosario_y_faq.md) | Glosario + preguntas frecuentes |
| [11_para_el_reporte.md](11_para_el_reporte.md) | Qué sacar de `docs/` y `results/` hacia el PDF |

## Cómo usar el repositorio

```bash
cd HW3
python tests/run_all.py
python demo.py
python attacks/keyspace_odd_even.py
python attacks/reduced_bruteforce.py
python attacks/sbox_diff_linear.py
python enigma/simulator.py HI
python gf/gf8_tables.py
```

Salidas reproducibles: carpeta [`results/`](../results/).

## Lecturas de apoyo

- William Stallings, *Cryptography and Network Security* (DES / Feistel).
- Reyad et al., “Key-Based Enhancement of Data Encryption Standard for Text Security,” IEEE NCCC 2021.
- Material del curso (Blackboard + PP slide 124 para GF(2³)).
