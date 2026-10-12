# Guía detallada — Homework No. 3: KE-DES y la Máquina Enigma

**Curso:** LIS4062 Information Security — Autumn 2026  
**Entrega:** Wednesday, 14 October 2026, 11:59 PM  
**Fuente de requisitos:** `Instrucciones.txt`, `HW3 LIS4062 Autumn 26.pdf`, `Key-Based_Enhancement_of_DES 2021.pdf`

---

## Metadatos de generación del documento

| Campo | Detalle |
|---|---|
| **Agente / sistema** | Auto (agent router de Cursor), impulsado por Composer |
| **Rol en este documento** | Lectura y síntesis de los enunciados y del paper KE-DES; razonamiento sobre organización del trabajo, proceso de implementación y estructura de entregables; redacción de la guía en español |
| **Modelos / capas involucradas** | (1) **Composer** — modelo principal de razonamiento y redacción de esta guía; (2) herramientas del entorno Cursor (lectura de archivos, extracción de texto PDF con `pdftotext`) para recuperar el contenido literal de los materiales del curso |
| **Fecha de elaboración** | 8 October 2026 |
| **Propósito declarado** | Orientar al equipo a **aprender** los temas de la tarea (DES/KE-DES, criptoanálisis, Enigma, GF(2³)) y a organizar implementación, división de trabajo y reporte — no a sustituir el trabajo académico ni a entregar una solución lista para calificar |
| **Limitaciones** | El paper KE-DES deja ambigüedades (p. ej. orden exacto de bits en la función K-D). Esta guía señala esas decisiones; el equipo debe documentar y justificar las suyas. Las tablas DES estándar (S-boxes, IP, etc.) deben tomarse de Stallings [1] o del material del curso, no se reproducen aquí completas |

---

## 1. Qué pide la tarea (checklist)

| Entregable / actividad | Qué demostrar |
|---|---|
| Implementar **KE-DES desde cero** | Sin librerías DES; tu propia función |
| **2 bloques de 64 bits** distintos | Clave, cifrado, descifrado correctos |
| Tiempos / proceso | Generación de claves, cifrado, descifrado |
| Ataques (investigación) | Fuerza bruta + diferencial + lineal sobre KE-DES |
| Comparación | Relación KE-DES ↔ DES |
| Enigma | Cifrado, descifrado y criptoanálisis (conceptual + ejemplos) |
| Apéndice | Tablas de suma y multiplicación en **GF(2³)** |
| Reporte PDF | Portada, abstract, intro, método, resultados, conclusiones, biblio |
| Subida | **Cada** integrante sube `HW3_ID_ID_ID.pdf` a Blackboard |

**Reglas administrativas (de `Instrucciones.txt`):**

- Equipo: máximo **3** estudiantes; la colaboración se anima.
- Portada: Title and Homework # · Student Name · ID · Course · Date · Autumn Term.
- Todas las figuras, tablas y referencias de la bibliografía deben citarse en el texto principal.
- Entregas tardías **no** se aceptan.
- Si un integrante no sube el PDF, ese integrante puede quedar en **0.0**.

---

## 2. Orden de aprendizaje (antes de codear)

El propósito principal del equipo debe ser **entender** Feistel, el schedule de claves, por qué Odd/Even debilita KE-DES, y el contraste con Enigma — no solo “que compile”.

### Fase A — DES clásico (base común, 1–2 días)

Sin esto, KE-DES se siente “mágico”.

1. Bloque 64 bits, clave 64 (efectiva 56), 16 rondas Feistel.
2. Flujo: `IP` → 16 rondas `(L,R)` → swap final → `IP⁻¹`.
3. Función `f`: expansión E (32→48) → XOR con subclave → 8 S-boxes → permutación P.
4. Schedule de claves: PC-1 → shifts (Tabla I del paper) → PC-2.
5. Descifrado = mismas rondas con claves en orden inverso.

**Objetivo de aprendizaje:** poder dibujar el diagrama y explicar cada caja sin mirar notas.

**Recurso:** Stallings [1] (capítulos de DES) + figuras del paper [2].

### Fase B — Qué cambia KE-DES (paper [2])

Dos modificaciones centrales:

#### B.1 Odd/Even sobre los 56 bits post PC-1

Pseudocódigo del paper (Listing 1): en posiciones pares pone `1`, en impares pone `0`.

En el ejemplo del paper, tras Odd/Even queda un patrón tipo `010101…`.

**Aprende esto:** esa transformación **destruye entropía de la clave**; por eso el enunciado del curso dice que KE-DES *no es criptográficamente seguro*. Eso alimenta la sección de ataques y la discusión DES vs KE-DES.

#### B.2 K-D en lugar de la expansión E

En cada ronda, en vez de E(R), construyen 48 bits con:

- 8 bits fijos de PC-1 (iguales en todas las rondas),
- 32 bits de R,
- 8 bits de PC-2 de esa ronda.

Luego: XOR con Ki → S-boxes → P → resto Feistel igual que DES.

**Ambigüedad a resolver en equipo (importante):** el paper no fija el *orden exacto* de concatenación de esos 8+32+8. Acuerden un orden, documenten en Metodología y sean consistentes en cifrado/descifrado. Validar con el ejemplo del paper (clave `133457799BBCDFF1`, tablas III–IV) ayuda a depurar PC-1, Odd/Even, shifts y PC-2 aunque el ejemplo de texto del paper sea incompleto.

### Fase C — Enigma + GF(2³) (en paralelo, no bloquea el código)

- **Enigma:** rotores, reflector, steckerbrett (plugboard), avance de rotores; por qué es una sustitución polialfabética.
- **Criptoanálisis histórico (nivel conceptual):** crib, Banburismus, Bombe — ideas y limitaciones, no procedimientos ofensivos contra sistemas reales.
- **GF(2³):** campo con 8 elementos; suma = XOR de coeficientes; producto módulo un polinomio irreducible (el del slide 124 del material del curso). El apéndice pide las **tablas 8×8** de suma y multiplicación.

---

## 3. Cómo implementar KE-DES (proceso práctico)

Lenguaje libre (Python, C++, Java, Go, etc.). Prioricen claridad sobre micro-optimización. **Crear su propia función KE-DES**; no usar implementaciones DES preexistentes de librerías.

### 3.1 Módulos sugeridos

```
tables.py / Tables   → IP, IP⁻¹, PC-1, PC-2, S-boxes, P, shifts
key_schedule.py      → PC-1 → Odd/Even → C/D → shifts → PC-2 → K1..K16
kd.py                → construir 48 bits (sustituto de E)
round.py             → f_KE(R, Ki, bits_PC1_8)
kedes.py             → encrypt/decrypt bloque 64
demo.py              → 2 bloques, timings, verificación
```

### 3.2 Pipeline de cifrado (por bloque)

Según la sección III.C del paper (adaptado a una checklist implementable):

1. Aplicar IP al plaintext de 64 bits.
2. Dividir en L₀ y R₀ (32 bits cada uno).
3. Para i = 1..16:
   - T = K-D(Rᵢ₋₁, bits₈_PC1, bits₈_PC2ᵢ)
   - U = T ⊕ Kᵢ
   - V = S-boxes(U); W = P(V)
   - Rᵢ = Lᵢ₋₁ ⊕ W
   - Lᵢ = Rᵢ₋₁
4. Concatenar R₁₆ ‖ L₁₆ (swap final como en DES) → IP⁻¹ → ciphertext.

**Descifrado:** misma estructura Feistel; claves en orden **K₁₆ … K₁**.

### 3.3 Generación de claves (sección III.B del paper)

1. PC-1: clave 64 → 56 bits.
2. Odd/Even sobre el bloque de 56 bits.
3. Dividir en C₀ y D₀ (28+28).
4. Left shifts según Tabla I (schedule estándar DES de shifts).
5. PC-2 sobre Cᵢ‖Dᵢ → Kᵢ (48 bits).
6. Repetir para i = 1..16.

**Ejemplo de verificación del paper:**

- Clave hex: `133457799BBCDFF1`
- Tras PC-1 y Odd/Even: patrón alternante (ver paper, pasos 2–3 y Tabla III para C₀/D₀).
- Round keys: comparar contra Tabla IV (al menos K1, K2, K15, K16 publicados).

### 3.4 CBC (como usa el paper)

- Dividir texto en bloques de 8 bytes (64 bits).
- Usar modo CBC con un IV documentado.
- Para lo mínimo pedido por la HW bastan **dos bloques de 64 bits**; CBC es un plus si quieren un archivo corto de demostración.

### 3.5 Validación (criterio de “está bien”)

1. Reproducir: clave hex del paper → PC-1 → Odd/Even → C₀/D₀ (coincidir con Tabla III).
2. `decrypt(encrypt(P, K), K) == P` para los 2 bloques.
3. Cambiar 1 bit de clave o plaintext y observar avalanche (útil en Resultados).
4. Medir tiempo de: key schedule, encrypt, decrypt (mismo estilo que Tabla V del paper).
5. Reportar entorno: CPU, RAM, OS (el paper reporta el suyo).

### 3.6 Dos datasets de 64 bits (sugerencia)

Elijan algo legible y algo “aleatorio”, por ejemplo:

- `P1 = "SECURITY"` (ASCII → 64 bits)
- `P2` = hex fijo tipo `0123456789ABCDEF`

Misma clave o dos claves; documenten ambas en Resultados (plaintext, key, ciphertext, plaintext recuperado, tiempos).

---

## 4. Ataques: investigar para aprender

El enunciado pide **investigación e inclusión en el reporte**. El foco es entender *por qué* KE-DES es débil respecto a DES, con experimentos acotados sobre **su propia implementación de laboratorio**.

> Nota pedagógica: KE-DES se declara no seguro en el propio homework. Los experimentos son de criptoanálisis académico sobre un cifrador débil del curso, no ataques a sistemas de terceros.

### 4.1 Fuerza bruta

- Espacio teórico DES ≈ 2⁵⁶; tras Odd/Even el espacio efectivo se colapsa (pocas claves distintas post-transformación).
- Experimento didáctico: contar cuántas salidas distintas produce Odd/Even; o búsqueda exhaustiva en un espacio reducido (pocos bits libres) midiendo tiempo.
- Conclusión de aprendizaje: la seguridad depende del **tamaño efectivo** del espacio de claves, no solo de “64 bits de entrada”.

### 4.2 Diferencial y lineal (nivel curso)

No hace falta un ataque completo de 16 rondas tipo Biham/Matsui. Sí hace falta demostrar comprensión:

| Ataque | Idea a explicar | Experimento pequeño |
|---|---|---|
| Diferencial | Propagación de diferencias ΔP → ΔC vía S-boxes | 1–2 rondas: tablas de diferencia de una S-box; probabilidad de una característica |
| Lineal | Aproximaciones lineales bits de entrada/salida/clave | Bias de una S-box; cómo se encadenaría en Feistel |

Luego argumenten:

- K-D introduce bits de clave en lo que antes era solo expansión de datos → cambia el análisis respecto a DES.
- Odd/Even empeora el key space más (y de forma más obvia) que cualquier “mejora” de difusión.

### 4.3 Relación KE-DES–DES (sección obligatoria)

Misma estructura Feistel, mismas S-boxes/P/IP en lo esencial; diferencias en:

1. Schedule de claves (inserción de Odd/Even tras PC-1).
2. Expansión (K-D vs E).

KE-DES no es “más seguro” solo por llamarse *enhanced*. El paper compara sobre todo estimaciones/tiempos (Tabla V), no ofrece un análisis de seguridad fuerte frente a diferencial/lineal.

---

## 5. Enigma (sección del reporte)

Estructura útil:

1. Historia breve y contexto (WWII).
2. Modelo operativo: teclado → plugboard → rotores → reflector → camino inverso.
3. Ejemplo a mano o con un simulador simple propio: 1–2 letras, mostrando el estado de los rotores.
4. Criptoanálisis: por qué el reflector prohíbe auto-cifrar una letra a sí misma; uso de cribs; idea general de la Bombe.
5. Contraste con DES/KE-DES: máquina electromecánica vs cifrador de bloque moderno; ambos ilustran confusión/difusión a distinto nivel.

---

## 6. Apéndice GF(2³)

1. Listar los 8 elementos: como polinomios `{0, 1, α, α+1, α², …}` o como enteros 0–7.
2. Fijar el polinomio irreducible del **slide 124** del material del profesor (PP). Si no lo tienen a mano, confirmarlo en clase.
3. Construir tabla de **suma** 8×8 y de **multiplicación** 8×8.
4. Una frase en Metodología: por qué GF(2ⁿ) aparece en criptografía moderna (p. ej. AES usa GF(2⁸)); aquí es el ejercicio de álgebra finita del curso.

---

## 7. División del trabajo (equipo de 3)

Asumiendo integrantes **A**, **B** y **C**. Todos deben entender el todo: cada uno sube el mismo PDF.

| Rol | Responsable | Entregables de aprendizaje |
|---|---|---|
| **A — Núcleo KE-DES** | Key schedule + K-D + encrypt/decrypt + tests de round-trip | Código + tablas de verificación (clave paper, 2 bloques) |
| **B — Experimentos y ataques** | Timings, comparación DES vs KE-DES, sección fuerza bruta + diferencial/lineal | Figuras/tablas + texto de Resultados/Discusión |
| **C — Enigma + GF(2³) + ensamble del reporte** | Investigación Enigma, tablas GF, portada/abstract/biblio, unificación del PDF | Apéndices + redondeo editorial |

### 7.1 Ritmo sugerido (referencia: 8 oct → entrega 14 oct)

| Día | Meta |
|---|---|
| Jue–Vie | Lectura conjunta paper + Stallings DES; acuerdo de orden K-D; scaffolding del código |
| Sáb | Key schedule validado vs paper; encrypt/decrypt de 1 bloque |
| Dom | Segundo bloque, timings, CBC opcional; B empieza ataques; C empieza Enigma/GF |
| Lun | Integrar resultados; borrador Metodología + Resultados |
| Mar | Abstract, conclusiones, biblio, figuras citadas; revisión cruzada |
| Mié mañana | PDF final `HW3_ID1_ID2_ID3.pdf`; **los 3 suben** a Blackboard |

### 7.2 Rituales que ayudan a aprender

- Daily ~20 min: A explica un bug; B pregunta “¿esto sería igual en DES?”; C conecta con Enigma/GF.
- Cada integrante debe poder ejecutar el demo y explicar una ronda en pizarra.
- Code review cruzado antes de redactar Resultados (evita reportar números de un bug).

### 7.3 Equipo de 2 (ajuste)

Si solo hay dos personas: A+B fusionan núcleo + experimentos; C se reparte entre ambos (uno Enigma, otro GF + ensamble del PDF). Mantener la regla de que ambos suban el archivo.

---

## 8. Estructura del reporte (plantilla)

1. **Cover page:** título + Homework #3, nombres, IDs, LIS4062, fecha, Autumn 2026.
2. **Abstract:** ~150–200 palabras: qué es KE-DES, qué implementaron, hallazgos principales (debilidad Odd/Even, tiempos, Enigma/GF).
3. **Introduction:** DES → motivación del paper → objetivos de la HW → organización del documento.
4. **Methodology:**
   - DES vs KE-DES (diagramas; citar Fig. 1 del paper y/o figura propia)
   - Decisiones de implementación (lenguaje, orden K-D, IV CBC)
   - Diseño de experimentos (2 bloques, métricas, alcance de ataques)
   - Método de estudio de Enigma y GF(2³)
5. **Results and discussion:**
   - Tablas: muestra de claves Kᵢ, P/C/P recuperado, tiempos
   - Discusión de ataques y relación con DES
   - Hallazgos Enigma
6. **Conclusions:** qué aprendieron; limitaciones (ambigüedades del paper, inseguridad de KE-DES); posible trabajo futuro académico.
7. **Bibliography:** Stallings [1], Reyad et al. [2], fuentes Enigma, material del curso; **todas citadas en el texto**.
8. **Appendix:** tablas GF(2³); opcional: pseudocódigo o extractos (no pegar decenas de páginas de código).

Figuras/tablas: numeradas y mencionadas en el texto (“como se muestra en la Tabla 2…”).

**Nombre de archivo:** `HW3_<ID>_<ID>_<ID>.pdf` (orden de IDs acordado por el equipo).

---

## 9. Criterios de calidad (autoevaluación)

- [ ] Round-trip correcto en 2 bloques
- [ ] Key schedule alineado con el ejemplo del paper (al menos PC-1, Odd/Even, C₀/D₀, muestra de Kᵢ)
- [ ] Tiempos reportados con entorno (CPU/RAM/OS)
- [ ] Ataques: explicación correcta + al menos un experimento o número propio
- [ ] Enigma: proceso de cifrado/descifrado + criptoanálisis (no solo historia)
- [ ] GF(2³) completo en apéndice (suma y multiplicación)
- [ ] Secciones formales completas; citas cruzadas
- [ ] Los 3 integrantes subieron el mismo PDF a tiempo

---

## 10. Errores frecuentes a evitar

1. Usar `PyCryptodome` / OpenSSL DES y “modificar un poco” → incumple *Create your own KE-DES function*.
2. Implementar solo DES y renombrarlo KE-DES.
3. No documentar el orden de bits de K-D.
4. Hablar de ataques sin conectar con Odd/Even / key space efectivo.
5. Que solo una persona suba el PDF → los demás en riesgo de 0.0.
6. Apéndice GF sin citar el polinomio irreducible usado.
7. Figuras/tablas sin cita en el texto, o bibliografía no referenciada.

---

## 11. Propósito de aprendizaje (norte del equipo)

Al terminar deberían poder explicar sin notas:

1. Por qué Feistel permite descifrar con la misma función `f`.
2. Rol de las S-boxes en confusión y de permutaciones/expansión en difusión.
3. Cómo una “mejora” mal diseñada (Odd/Even) **empeora** la seguridad.
4. Diferencia conceptual entre fuerza bruta, criptoanálisis diferencial y lineal.
5. Enigma como sistema histórico frente a un cifrador de bloque moderno.
6. Aritmética básica en GF(2³) (tablas de suma y producto).

---

## 12. Referencias mínimas (del enunciado)

[1] William Stallings, *Cryptography and Network Security: Principles and Practices*, 7th Edition, Pearson Prentice Hall, 2016.

[2] O. Reyad, H. M. Mansour, M. Heshmat, and E. A. Zanaty, “Key-Based Enhancement of Data Encryption Standard for Text Security,” IEEE National Computing Colleges Conference (NCCC), 2021. DOI: 10.1109/NCCC49330.2021.9428818.

Material adicional del curso: descripción KE-DES en Blackboard; PP slide 124 (tablas GF(2³)).

---

## 13. Diagrama mental del flujo de trabajo

```
Leer Stallings DES ──► Leer paper KE-DES ──► Acordar K-D
         │                      │                  │
         └──────────┬───────────┘                  │
                    ▼                              ▼
            Implementar key schedule      Implementar ronda KE
                    │                              │
                    └──────────┬───────────────────┘
                               ▼
                    Demo 2 bloques + timings
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
         Ataques         Enigma + GF         Redacción
         (B)             (C)                 reporte
              └────────────────┼────────────────┘
                               ▼
                    PDF único → suben los 3
```

---

*Fin del documento. Elaborado como guía de estudio y organización para HW3; el trabajo de implementación, análisis y redacción del reporte corresponde al equipo.*
