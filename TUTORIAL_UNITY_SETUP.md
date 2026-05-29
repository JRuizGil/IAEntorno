# Tutorial: Configuración en el Editor de Unity

**Proyecto:** IA de Enemigos — A* + Behavior Tree + Blackboard  
**Entorno:** Unity 6000.0.59f2 · URP 17.0.4 · Input System 1.14.2

---

## Índice

1. [Crear las Layers necesarias](#1-crear-las-layers-necesarias)
2. [Configurar el Grid A*](#2-configurar-el-grid-a)
3. [Crear obstáculos y zonas oscuras](#3-crear-obstáculos-y-zonas-oscuras)
4. [Configurar el Jugador](#4-configurar-el-jugador)
5. [Crear el primer Enemigo](#5-crear-el-primer-enemigo)
6. [Crear los Waypoints de patrulla](#6-crear-los-waypoints-de-patrulla)
7. [Crear el segundo Enemigo y conectar la alerta](#7-crear-el-segundo-enemigo-y-conectar-la-alerta)
8. [Verificar con Gizmos](#8-verificar-con-gizmos)
9. [Teclas de prueba en Play Mode](#9-teclas-de-prueba-en-play-mode)
10. [Solución de problemas frecuentes](#10-solución-de-problemas-frecuentes)

---

## 1. Crear las Layers necesarias

Las layers permiten que los Physics checks de A* y los sensores identifiquen qué es qué.

1. Menú superior → **Edit → Project Settings → Tags and Layers**
2. En la sección **Layers**, busca los primeros slots vacíos (desde User Layer 6) y crea:

| Nombre | Para qué se usa |
|---|---|
| `Obstacle` | Objetos que bloquean el paso (paredes, muebles) |
| `DarkZone` | Zonas con luz reducida (coste A* ×3, stealth del jugador) |
| `Ground` | El suelo, para que el jugador detecte si está en el suelo |
| `Player` | El GameObject del jugador (para que los sensores lo encuentren) |

> También necesitas el **Tag** `Player` en el jugador para que `StateMachine` y otros scripts lo localicen con `FindGameObjectWithTag("Player")`.
> Ve a **Tags** (sección de arriba) → `+` → escribe `Player`.

---

## 2. Configurar el Grid A*

El grid es la cuadrícula que A* usa para navegar. Necesita dos GameObjects vacíos.

### 2.1 — GameObject "Grid"

1. Jerarquía → clic derecho → **Create Empty** → renombra a `Grid`
2. Posiciónalo en el **centro** del área jugable (ej. `0, 0, 0`)
3. Inspector → **Add Component** → busca `GridManager`
4. Configura los campos:

| Campo | Valor recomendado | Descripción |
|---|---|---|
| Grid World Size | `(20, 20)` | Tamaño en metros del área navegable |
| Node Radius | `0.5` | Celdas de 1×1 metro |
| Unwalkable Mask | `Obstacle` | Layer de objetos que bloquean el paso |
| Dark Zone Mask | `DarkZone` | Layer de zonas oscuras (coste ×3) |

> **Truco:** Con el GameObject `Grid` seleccionado, verás el grid en la Scene View incluso fuera de Play Mode (gracias a `[ExecuteAlways]`). Celdas rojas = no walkable, blancas = walkable.

### 2.2 — GameObject "Pathfinder"

1. Jerarquía → clic derecho → **Create Empty** → renombra a `Pathfinder`
2. Inspector → **Add Component** → busca `AStarPathfinder`
3. En **Heuristic**, elige la variante que quieras comparar:
   - `Euclidean` — línea recta (recomendado para inicio)
   - `Manhattan` — sin diagonales
   - `Diagonal` — Chebyshev (bueno con movimiento en 8 direcciones)

---

## 3. Crear obstáculos y zonas oscuras

### 3.1 — Obstáculos (paredes, cubos)

1. Jerarquía → **3D Object → Cube** (o usa los que ya tengas)
2. Asegúrate de que tiene un **Collider** (Box Collider viene por defecto)
3. Inspector → en el desplegable de Layer → selecciona **Obstacle**
4. Repite para todos los obstáculos
5. Pulsa Play (o sin pulsar, si ves el grid en tiempo real) → esos cubos aparecen en **rojo** en el grid

### 3.2 — Zonas oscuras

Las zonas oscuras son áreas donde:
- A* asigna coste ×3 (los enemigos las evitan si pueden)
- Los sensores detectan al jugador con rango reducido al 30%

1. Jerarquía → **3D Object → Plane** (o Cube aplanado)
2. Dale un material oscuro: Assets → clic derecho → **Create → Material** → color negro/gris oscuro → arrástralo al plano
3. Inspector → Layer → **DarkZone**
4. El Collider debe estar presente; si usas Plane, tiene MeshCollider por defecto
5. Asegúrate de que el plano tiene **Is Trigger = false** (para que `Physics.CheckSphere` lo detecte)

> Si el plano oscuro está en el suelo, ponlo a Y = 0 y escálalo para cubrir el área oscura.

---

## 4. Configurar el Jugador

### 4.1 — Estructura de GameObjects

Crea esta jerarquía:
```
Player  (tiene CharacterController + PlayerMovement + PlayerCamera + tag "Player")
└── GroundCheck  (objeto vacío, posición Y = -1 aproximadamente, justo bajo los pies)
```

Y separado:
```
Main Camera  (tiene PlayerCamera apuntando al Player)
```

### 4.2 — Componentes del Player

1. Selecciona el GameObject `Player`
2. **Add Component → Character Controller** (ajusta Height y Radius al tamaño de tu personaje)
3. **Add Component → Player Movement**
4. En **Player Movement**, arrastra los campos:
   - `Controller` → el mismo GameObject (se detecta automáticamente, o arrástralo)
   - `Ground Check` → el hijo `GroundCheck`
   - `Ground Mask` → selecciona la layer **Ground**
5. En el GameObject raíz: **Tag → Player** y **Layer → Player**

### 4.3 — Cámara

1. Selecciona `Main Camera`
2. **Add Component → Player Camera**
3. Arrastra el `Player` al campo `Target`
4. Ajusta `Offset`: prueba con `(0, 5, -10)` para vista en tercera persona

---

## 5. Crear el primer Enemigo

### 5.1 — Estructura base

```
Enemy_1  (Capsule o tu modelo + Enemigo_BT_Blackboard + EnemyLife + Renderer)
```

1. Jerarquía → **3D Object → Capsule** → renombra a `Enemy_1`
2. Crea y asigna un **Material** (cualquier color de base; el script lo cambia en tiempo real)

### 5.2 — Añadir Enemigo_BT_Blackboard

1. **Add Component** → busca `Enemigo_BT_Blackboard`
2. Configura los campos del Inspector:

**Referencias:**
| Campo | Valor |
|---|---|
| Player | Arrastra el GameObject `Player` |

**Salud:**
| Campo | Valor |
|---|---|
| Health | `100` |
| Max Health | `100` |

**Detección visual:**
| Campo | Valor sugerido |
|---|---|
| Detection Range | `7` (metros) |

**Escucha (Parte 3):**
| Campo | Valor sugerido |
|---|---|
| Hearing Range | `10` (metros) |

**Patrulla:**
| Campo | Valor sugerido |
|---|---|
| Patrol Speed | `2` |
| Waypoint Distance | `0.5` |
| Waypoints | (lo asignaremos en el paso 6) |

**Persecución / Investigación / Huida:**
| Campo | Valor sugerido |
|---|---|
| Chase Speed | `4` |
| Investigate Speed | `3` |
| Investigation Distance | `0.5` |
| Flee Speed | `7` |

**Ataque:**
| Campo | Valor sugerido |
|---|---|
| Attack Range | `1.5` |

**Zonas oscuras (stealth):**
| Campo | Valor |
|---|---|
| Dark Zone Mask | Selecciona la layer **DarkZone** |

**Alerta multiagente:**
| Campo | Valor |
|---|---|
| Partner | (lo asignaremos en el paso 7) |

### 5.3 — Añadir EnemyLife (barra de vida)

1. **Add Component → Enemy Life**
2. Si tienes un Scrollbar en la UI, arrástralo a `Health Bar`
3. Si no tienes UI, déjalo vacío de momento

---

## 6. Crear los Waypoints de patrulla

Los waypoints son GameObjects vacíos que el enemigo visita en orden.

1. Jerarquía → clic derecho → **Create Empty** → renombra a `Waypoints_Enemy1`
2. Dentro de ese objeto, crea 4 hijos vacíos: `WP_0`, `WP_1`, `WP_2`, `WP_3`
3. Colócalos en diferentes esquinas del área de patrulla (en el plano Y del suelo)
4. Selecciona `Enemy_1` → en el componente `Enemigo_BT_Blackboard` → campo **Waypoints**:
   - Cambia el Size a `4`
   - Arrastra `WP_0`, `WP_1`, `WP_2`, `WP_3` a los slots

> Repite el mismo proceso para `Enemy_2` (paso 7).

---

## 7. Crear el segundo Enemigo y conectar la alerta

### 7.1 — Duplicar el enemigo

1. Selecciona `Enemy_1` en la Jerarquía → **Ctrl+D** para duplicar
2. Renombra el duplicado a `Enemy_2`
3. Muévelo a otra posición en la escena

### 7.2 — Waypoints propios

Crea otro grupo de waypoints `Waypoints_Enemy2` con sus 4 hijos y asígnalos al campo **Waypoints** de `Enemy_2`.

### 7.3 — Conectar la alerta entre guardias

Esto permite que cuando `Enemy_1` ve al jugador, `Enemy_2` también lo investigue (y viceversa).

1. Selecciona `Enemy_1`
2. En el campo **Partner** del componente `Enemigo_BT_Blackboard` → arrastra `Enemy_2`
3. Selecciona `Enemy_2`
4. En el campo **Partner** → arrastra `Enemy_1`

> Cuando un enemigo persigue al jugador, escribe en la pizarra del compañero:
> `HasClue = true` y `LastKnownPosition = posición actual del jugador`.

---

## 8. Verificar con Gizmos

Antes de entrar en Play Mode, selecciona el GameObject `Grid` y comprueba en la **Scene View**:

| Color de celda | Significado |
|---|---|
| Blanco semitransparente | Walkable (el enemigo puede pasar) |
| Rojo | No walkable (hay un obstáculo) |
| Azul | Camino A* calculado (solo en Play Mode) |

Con los enemigos seleccionados, verás:
| Color de esfera Gizmo | Significado |
|---|---|
| Amarillo | Rango de detección visual |
| Naranja semitransparente | Rango de escucha |
| Rojo + línea | Posición conocida del jugador (LastKnownPosition) |
| Cian | Waypoints de patrulla |

---

## 9. Teclas de prueba en Play Mode

| Tecla | Efecto |
|---|---|
| **WASD** | Mover al jugador |
| **Espacio** | Saltar |
| **Q** | Infligir daño al enemigo (−1 HP/frame mientras se mantiene) |
| **K** | Infligir 25% de daño (en EnemyLife, debug) |
| **E** | El jugador emite ruido → activa SoundSensor del enemigo |

**Comportamiento esperado del enemigo (colores):**

| Color del enemigo | Estado |
|---|---|
| Cian | Patrullando waypoints |
| Amarillo | Persiguiendo al jugador (lo ve) |
| Negro | Atacando (jugador muy cerca) |
| Rojo | Investigando última posición conocida |
| Magenta | Huyendo (vida < 50%) |

---

## 10. Solución de problemas frecuentes

### El grid no aparece en Scene View
- Asegúrate de que el GridManager está en un GameObject en la escena (no en prefab sin instanciar)
- Comprueba que `Node Radius` > 0 y `Grid World Size` > 0

### El enemigo no se mueve
- Verifica que `AStarPathfinder` está en la escena
- Comprueba que los waypoints están asignados en el Inspector
- Asegúrate de que la posición del enemigo **está dentro del área del grid** (el contorno blanco)

### El enemigo ignora al jugador aunque esté cerca
- Comprueba que el campo `Player` del componente `Enemigo_BT_Blackboard` tiene asignado el GameObject del jugador
- Verifica que `Detection Range` es suficientemente grande

### Unity muestra "Missing Script" en un GameObject
- Es el componente `StateMachine` antiguo. Selecciona el GameObject → componente con `?` → clic derecho → **Remove Component**

### A* muestra "nodo de inicio no walkable"
- El enemigo está encima de un objeto con layer `Obstacle`. Mueve al enemigo a una celda blanca del grid.
- Si el enemigo está por debajo del grid, ajusta la posición Y del `Grid` GameObject.

### Los nodos oscuros no tienen mayor coste
- Asegúrate de que los GameObjects de zona oscura tienen **collider** activo
- Verifica que su **Layer** es exactamente `DarkZone` y que el campo `Dark Zone Mask` en `GridManager` incluye esa layer
- El grid se construye en `Awake()`. Si cambias la layer en Play Mode, reinicia la escena.

### El segundo enemigo no se alerta cuando el primero ve al jugador
- Verifica que el campo `Partner` en **ambos** enemigos está asignado (cruzado: Enemy_1 → Enemy_2 y Enemy_2 → Enemy_1)

---

## Estructura final de la Jerarquía

```
Scene
├── Grid                    ← GridManager (centro del área)
├── Pathfinder              ← AStarPathfinder
├── Player                  ← CharacterController + PlayerMovement
│   └── GroundCheck         ← Transform para detección de suelo
├── Main Camera             ← PlayerCamera
├── Enemy_1                 ← Enemigo_BT_Blackboard + EnemyLife
├── Enemy_2                 ← Enemigo_BT_Blackboard + EnemyLife
├── Waypoints_Enemy1
│   ├── WP_0
│   ├── WP_1
│   ├── WP_2
│   └── WP_3
├── Waypoints_Enemy2
│   ├── WP_0 ... WP_3
├── Obstacles               ← GameObjects con layer Obstacle + Collider
└── DarkZones               ← GameObjects con layer DarkZone + Collider
```
