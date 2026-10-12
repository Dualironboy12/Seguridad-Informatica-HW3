# 07 — Ataques educativos sobre KE-DES

> Ámbito: cifrador de **laboratorio** de esta tarea. No son procedimientos para atacar sistemas de terceros.

## 1) Fuerza bruta y espacio efectivo

**Idea:** probar claves hasta que `encrypt(P,K) == C`.

En DES clásico el costo escala con ~2⁵⁶. En KE-DES, tras Odd/Even:

- Las subclaves `K1..K16` son **fijas**.
- Solo `pc1_8` (8 bits) cambia el comportamiento vía K-D.

Scripts:

```bash
python attacks/keyspace_odd_even.py
python attacks/reduced_bruteforce.py
```

El segundo recupera un `pc1_8` secreto de laboratorio buscando en 2⁸ candidatos y extrapola tiempos a espacios mayores.

**Conclusión para el reporte:** la seguridad no la da el rótulo “64-bit key”, sino la **entropía efectiva** que sobrevive al diseño.

## 2) Criptoanálisis diferencial (intuición)

**Pregunta:** si dos plaintexts difieren en `ΔP`, ¿con qué frecuencia los ciphertexts difieren en un `ΔC` concreto?

Las **S-boxes** son el cuello de botella no lineal. La **DDT** (Difference Distribution Table) de una S-box cuenta, para cada `(din, dout)`, cuántos `x` cumplen `S(x) ⊕ S(x⊕din) = dout`.

Si algún `din → dout` ocurre mucho más que el promedio, hay una **característica diferencial** explotable en pocas rondas.

```bash
python attacks/sbox_diff_linear.py
```

En DES/KE-DES las S-boxes son las mismas → DDT locales iguales. K-D cambia cómo se alimentan esas S-boxes (mezcla bits de clave en la “expansión”).

## 3) Criptoanálisis lineal (intuición)

**Pregunta:** ¿existe una combinación XOR de bits de entrada que “casi siempre” coincida con una combinación de bits de salida?

El **bias** mide `|Pr[igualdad] - 1/2|`. Bias 0 = impredecible (ideal); bias grande = aproximación útil (Matsui).

El script reporta el mejor bias no trivial por S-box.

## 4) Qué enfatizar en la discusión KE-DES

1. Debilidad dominante: **Odd/Even** (colapso de schedule).
2. K-D: cambio estructural respecto a E; relevante para propagación, secundario frente al colapso.
3. No hace falta un ataque completo de 16 rondas tipo papers clásicos: a nivel curso basta demostrar comprensión + números propios.

## Errores comunes

- Hablar de “2⁶⁴ claves” sin mencionar Odd/Even.
- Copiar definiciones de diferencial/lineal sin conectarlas a las S-boxes ni a `results/`.

## Siguiente

[08_Enigma.md](08_Enigma.md)
