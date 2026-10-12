# 10 — Glosario y FAQ

## Glosario breve

| Término | Definición corta |
|---|---|
| Avalanche | Cambio fuerte en C ante un flip mínimo en P o K |
| Bias (lineal) | Desviación de 1/2 en una aproximación XOR |
| CBC | Modo que encadena bloques con XOR del ciphertext previo |
| DDT | Tabla de distribución de diferencias de una S-box |
| Difusión | Cada entrada afecta muchas salidas |
| Confusión | Relación clave–ciphertext difícil de caracterizar |
| Feistel | Estructura de rondas L/R con XOR que facilita el descifrado |
| IP / IP⁻¹ | Permutaciones inicial e inversa de DES |
| K-D | Key-Distribution: expansión 48 bits de KE-DES |
| Odd/Even | Transformación post PC-1 que colapsa la clave en KE-DES |
| PC-1 / PC-2 | Permuted Choice del schedule de claves |
| Round key Kᵢ | Subclave de 48 bits de la ronda i |
| S-box | Sustitución no lineal 6→4 bits |
| Subclave | Ver round key |

## FAQ

### ¿Por qué mi PC-1 no coincide con el del paper?

El paper tiene una errata tipográfica en el PC-1 impreso. Esta implementación usa la tabla FIPS/Stallings; el test `test_pc1_matches_stallings_example` lo fija. Documenta la discrepancia en el reporte (ver `docs/03` y `docs/05`).

### ¿Por qué Listing 1 y Tabla III parecen contradictorios?

Listing 1 uniforme implica `C0 == D0`; Tabla III tiene `D0 = 1010...` y solo así salen las Kᵢ de Tabla IV. Seguimos las tablas publicadas.

### ¿Por qué todas las claves producen las mismas Kᵢ?

Por diseño de Odd/Even en esta lectura: la salida no depende de los bits de entrada. Es el hallazgo de seguridad central.

### Entonces, ¿el ciphertext tampoco depende de la clave?

Sí puede depender: `pc1_8` entra en K-D. Pero el espacio residual es pequeño (orden 2⁸ por ese canal), no 2⁵⁶.

### ¿CBC o ECB?

Para 2 bloques sueltos basta ECB implícito (cada bloque independiente). CBC está en `kedes/cbc.py` si quieren acercarse al paper.

### ¿Puedo usar PyCryptodome?

No para implementar KE-DES. El enunciado pide **tu propia** función.

### ¿Qué hago si el profesor define otro orden K-D?

Cambia `kd_expand` en `kedes/kd.py`, actualiza `docs/03`, regenera `demo.py` y pega los nuevos hex en Resultados.

### ¿Los timings deben igualar la Tabla V del paper?

No. Reporta **tu** entorno y tus medias (`demo.py`). La Tabla V es solo referencia de formato.
