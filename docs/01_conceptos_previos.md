# 01 — Conceptos previos

## Analogía de apertura

Imagina un candado con **la misma llave** para cerrar y abrir (cifrado simétrico), frente a un buzón donde cualquiera echa cartas pero solo el dueño tiene la llave para sacarlas (asimétrico). DES y KE-DES son del primer tipo: **una sola clave secreta** compartida entre quien cifra y quien descifra.

## Plaintext, ciphertext y clave

| Término | Significado intuitivo |
|---|---|
| **Plaintext (P)** | Mensaje legible (o bytes “en claro”). |
| **Ciphertext (C)** | Mensaje transformado; sin la clave no debería ser útil. |
| **Key (K)** | Secreto que parametriza la transformación. |
| **Bloque** | Pedazo de tamaño fijo que procesa el algoritmo de una vez. |

DES/KE-DES operan sobre **bloques de 64 bits** (8 bytes). Un texto largo se parte en varios bloques (en el paper usan modo CBC).

## Simétrico vs asimétrico

- **Simétrico:** misma K para cifrar y descifrar. Rápido. Problema: cómo compartir K de forma segura.
- **Asimétrico (RSA, etc.):** par público/privado. Más lento; suele usarse para intercambiar claves simétricas.

Esta tarea se centra en el simétrico de bloque.

## Operaciones que verás todo el tiempo

### XOR (⊕)

Suma bit a bit módulo 2: `0⊕0=0`, `0⊕1=1`, `1⊕1=0`.  
Propiedades útiles:

- `A ⊕ A = 0`
- `A ⊕ 0 = A`
- `(A ⊕ B) ⊕ B = A` → **reversible**: si mezclas con B, volver a XOR con B deshace el cambio.

Por eso Feistel puede descifrar sin “invertir” la función `f` de forma complicada.

### Permutación

Reordenar bits según una tabla. No pierde información; solo cambia posiciones. Ejemplo mental de 4 bits:

```
entrada:  b1 b2 b3 b4
tabla:    [4, 1, 2, 3]
salida:   b4 b1 b2 b3
```

En el código: `kedes.bits.permute` (las tablas DES usan índices **1-based**: la posición 1 es el bit más significativo).

### Sustitución (S-box)

Caja que mira un pedazo pequeño de bits y lo reemplaza por otro. Introduce **no linealidad**: sin ella, todo el cifrado sería ecuaciones lineales sobre GF(2) y se rompería con álgebra lineal.

## Confusión y difusión (Shannon)

- **Confusión:** ocultar la relación entre clave y ciphertext (S-boxes ayudan).
- **Difusión:** que cada bit del plaintext (y de la clave) influya en muchos bits del ciphertext (permutaciones + varias rondas).

El efecto **avalanche** mide difusión: cambias 1 bit de P y cuentas cuántos bits de C cambian. Idealmente cerca de la mitad. Ver salida de `demo.py`.

## ¿Por qué 64 bits y 16 rondas?

Diseño histórico de DES (años 70): compromiso entre seguridad de la época y hardware. Hoy 64 bits de bloque y 56 bits efectivos de clave son **insuficientes** frente a hardware moderno; por eso DES se considera obsoleto para protección real. KE-DES, además, introduce una debilidad propia (Odd/Even). El enunciado del curso lo dice explícitamente: **no es criptográficamente seguro**; lo usamos para aprender.

## Por qué importa

Sin estos conceptos, el diagrama de DES parece una caja negra. Con ellos, cada flecha del diagrama tiene un “para qué”.

## Errores comunes

- Confundir “64 bits de clave” con “2⁶⁴ claves útiles” (en DES hay bits de paridad; efectivos ≈ 2⁵⁶).
- Pensar que “más pasos = más seguro” sin mirar si algún paso **destruye** entropía (spoiler: Odd/Even en KE-DES).

## Siguiente

[02_DES_y_Feistel.md](02_DES_y_Feistel.md)
