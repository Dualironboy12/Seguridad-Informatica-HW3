# 08 — Máquina Enigma (visión de ingeniería)

## Analogía

Enigma es como un **cableado eléctrico que cambia cada letra**. Cada vez que pulsas una tecla, un rotor avanza y el camino eléctrico se reconfigura. Por eso la misma letra no se cifra siempre igual (polialfabético).

## Piezas

| Pieza | Rol |
|---|---|
| **Teclado / lámparas** | Entrada y salida de letras |
| **Plugboard (Steckbrett)** | Permutación opcional de pares de letras al inicio/final |
| **Rotores** | Cableado fijo + rotación; el derecho avanza en cada tecla |
| **Reflector** | Devuelve la señal por otro camino; hace el cifrado **involutivo** |

Involutivo: cifrar dos veces con la misma configuración recupera el texto (en el modelo básico). Por eso el simulador “descifra” volviendo a cifrar.

## Propiedad famosa del reflector

Ninguna letra se cifra a **sí misma**. Eso dio pistas históricas (cribs): si sospechas que un fragmento es `WETTER`, puedes descartar alineamientos donde plaintext y ciphertext coinciden en una posición.

## Cómo correr el simulador

```bash
python enigma/simulator.py HI
```

Salida típica: muestra posiciones de rotores antes/después de cada letra y el ciphertext; luego recupera el plaintext.

Código: `enigma/simulator.py` — rotores I/II/III, reflector B, posiciones iniciales `AAA`, sin plugboard por defecto.

## Contraste con DES/KE-DES

| | Enigma | DES/KE-DES |
|---|---|---|
| Época / medio | Electromecánica WWII | Algoritmo digital de bloque |
| Unidad | Letra | Bloque 64 bits |
| Secreto | Orden/posiciones/plugs/rotores del día | Clave binaria |
| Análisis | Cribs, Bombe, patrones del reflector | Diferencial, lineal, fuerza bruta |

Ambos ilustran **confusión** (sustituciones) y cambio de estado; DES añade difusión diseñada sobre bits y rondas Feistel.

## Criptoanálisis (nivel curso)

Menciona en el reporte, sin pretender reimplementar Bletchley Park:

- Uso de **cribs** (texto probable).
- Explotación de que `Cᵢ ≠ Pᵢ` nunca.
- Idea de la **Bombe**: automatizar pruebas de settings compatibles con un crib.

## Siguiente

[09_GF23.md](09_GF23.md)
