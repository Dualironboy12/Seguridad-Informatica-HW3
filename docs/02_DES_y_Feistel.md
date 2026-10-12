# 02 — DES y la estructura Feistel

## Analogía

Piensa en dos montones de cartas (L y R). En cada ronda:

1. Tomas el montón derecho R y lo “revuelves” con la clave de esa ronda (`f(R, Ki)`).
2. Mezclas ese revolvido con el montón izquierdo mediante XOR.
3. Intercambias los montones y repites.

Al final, aunque `f` sea complicada, **puedes deshacer todo** recorriendo las rondas al revés: la magia está en el XOR, no en invertir `f`.

## Vista de pájaro de DES

```text
Plaintext (64)
    │
    ▼
   IP          ← permutación inicial
    │
    ▼
 L0 (32)   R0 (32)
    │         │
    │    ┌────┴────┐
    │    │ 16 rondas│
    │    └────┬────┘
    ▼         ▼
 R16      L16      ← swap final (concatenar R16||L16)
    │
    ▼
  IP⁻¹
    │
    ▼
Ciphertext (64)
```

Código equivalente: `kedes/cipher.py` (en KE-DES, dentro de `f`, la expansión E se reemplaza por K-D).

## Una ronda Feistel (forma general)

```text
Lᵢ = Rᵢ₋₁
Rᵢ = Lᵢ₋₁ ⊕ f(Rᵢ₋₁, Kᵢ)
```

### Por qué el descifrado funciona

En descifrado usas las mismas fórmulas con claves **K₁₆ … K₁**.  
Si en cifrado `Rᵢ = Lᵢ₋₁ ⊕ f(Rᵢ₋₁, Kᵢ)` y `Lᵢ = Rᵢ₋₁`, entonces:

`Lᵢ₋₁ = Rᵢ ⊕ f(Lᵢ, Kᵢ)` porque `Rᵢ₋₁ = Lᵢ`.

No necesitas la inversa de `f`.

## Anatomía de `f` en DES clásico

1. **Expansión E:** 32 → 48 bits (repite algunos bits).
2. **XOR** con subclave Kᵢ (48 bits).
3. **8 S-boxes:** cada una 6 → 4 bits → quedan 32 bits.
4. **Permutación P:** reordena esos 32 bits.

En KE-DES el paso 1 es **K-D** en lugar de E; el resto se mantiene. Ver [03_KE-DES_diferencias.md](03_KE-DES_diferencias.md).

## Schedule de claves (DES)

```text
K (64) → PC-1 → 56 bits → partir en C0,D0 (28+28)
              → 16 veces: left shift + PC-2 → K1..K16 (48)
```

Los left shifts siguen la tabla `[1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]` (`kedes/tables.py` → `SHIFTS`).

## IP e IP⁻¹

Solo reordenan bits. No añaden secreto; facilitan implementación histórica en hardware. Deben ser inversas una de la otra.

## Checklist de aprendizaje

Al terminar esta sección deberías poder:

- [ ] Dibujar Feistel de una ronda y explicar el swap.
- [ ] Explicar por qué descifrar = mismas rondas con claves al revés.
- [ ] Nombrar los cuatro pasos de `f` en DES.

## Errores comunes

- Olvidar el **swap final** antes de IP⁻¹ (rompe compatibilidad con la definición estándar).
- Indexar tablas DES como 0-based sin restar 1 (nuestro `permute` ya lo contempla).

## Siguiente

[03_KE-DES_diferencias.md](03_KE-DES_diferencias.md)
