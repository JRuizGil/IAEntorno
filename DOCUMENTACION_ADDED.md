# Documentación técnica — Scripts/Added

## Índice

1. [Visión general](#1-visión-general)
2. [A* Pathfinding](#2-a-pathfinding)
3. [Behavior Tree (BT)](#3-behavior-tree-bt)
4. [Blackboard](#4-blackboard)
5. [BT + Blackboard combinados](#5-bt--blackboard-combinados)
6. [Advanced BT — Conditional Aborts](#6-advanced-bt--conditional-aborts)
7. [Visualizador del árbol (Editor)](#7-visualizador-del-árbol-editor)
8. [Guía de implementación para el proyecto final](#8-guía-de-implementación-para-el-proyecto-final)

---

## 1. Visión general

Los scripts de `Added/` son una **biblioteca de ejercicios de clase** organizada en capas que van de menor a mayor complejidad:

```
Added/
├── AStar/                        ← Sistema de navegación por grid propio
├── Ejercicio blackboard/
│   ├── BT/                       ← Behavior Tree base (versión completa)
│   └── Blackboard/               ← Sistema de pizarra + sensores
├── Enemigo_BT_Blackboard/        ← Combinación BT + Blackboard (esqueleto)
├── BehaviorTreeVisualización/    ← Inspector editor del árbol en tiempo real
└── Unit5_AdvancedBT/             ← BT avanzado: aborts y cursores
```

**Estado del código:** los sistemas de clase están completos como referencia. Los scripts marcados con `TODO` son esqueletos que los ejercicios pedían implementar.

---

## 2. A* Pathfinding

**Carpeta:** `AStar/AStar/`

### Arquitectura

```
GridManager  (MonoBehaviour, Singleton)
  └── crea y almacena Node[,] _grid
  └── expone NodeFromWorldPoint(), GetNeighbours()

AStarPathfinder  (MonoBehaviour, Singleton)
  └── FindPath(start, target) → List<Node>
  └── usa GridManager para navegar el grid

PathRequester  (MonoBehaviour)
  └── llama a AStarPathfinder.FindPath()
  └── sigue el camino nodo a nodo

Node  (clase pura)
  └── datos de celda: walkable, worldPosition, gridX/Y, gCost, hCost, parent
```

### Node.cs

Clase de datos pura. Almacena:

| Campo | Tipo | Significado |
|---|---|---|
| `walkable` | bool | ¿Puede pisarse? |
| `worldPosition` | Vector3 | Centro de la celda en world space |
| `gridX`, `gridY` | int | Coordenadas en el grid |
| `gCost` | float | Coste acumulado desde el inicio |
| `hCost` | float | Estimación heurística al destino |
| `fCost` | float | `gCost + hCost` (propiedad calculada) |
| `parent` | Node | Nodo anterior en el camino |

### GridManager.cs

`[ExecuteAlways]` — se actualiza incluso fuera de Play Mode para ver el grid en Scene View (Gizmos).

**Lo que hace el Gizmo:**
- Contorno blanco = límite del grid.
- Celdas rojas = no walkable (hay un colisionador con la capa `unwalkableMask`).
- Celdas blancas semitransparentes = walkable.
- Celdas azules = camino A* actual.

**Métodos que hay que implementar** (están como `throw NotImplementedException`):

```csharp
// 1. CreateGrid() — construir el array de nodos
void CreateGrid()
{
    _grid = new Node[_gridSizeX, _gridSizeY];
    Vector3 worldBottomLeft = transform.position
        - Vector3.right   * gridWorldSize.x * 0.5f
        - Vector3.forward * gridWorldSize.y * 0.5f;

    for (int x = 0; x < _gridSizeX; x++)
        for (int y = 0; y < _gridSizeY; y++)
        {
            Vector3 worldPoint = worldBottomLeft
                + Vector3.right   * (x * _nodeDiameter + nodeRadius)
                + Vector3.forward * (y * _nodeDiameter + nodeRadius);
            bool walkable = !Physics.CheckSphere(worldPoint, nodeRadius, unwalkableMask);
            _grid[x, y] = new Node(walkable, worldPoint, x, y);
        }
}

// 2. NodeFromWorldPoint() — world space → celda del grid
public Node NodeFromWorldPoint(Vector3 worldPosition)
{
    float percentX = Mathf.Clamp01(
        (worldPosition.x - transform.position.x + gridWorldSize.x * 0.5f) / gridWorldSize.x);
    float percentY = Mathf.Clamp01(
        (worldPosition.z - transform.position.z + gridWorldSize.y * 0.5f) / gridWorldSize.y);
    int x = Mathf.RoundToInt((_gridSizeX - 1) * percentX);
    int y = Mathf.RoundToInt((_gridSizeY - 1) * percentY);
    return _grid[x, y];
}

// 3. GetNeighbours() — 8 vecinos (incluye diagonales)
public List<Node> GetNeighbours(Node node)
{
    var neighbours = new List<Node>();
    for (int dx = -1; dx <= 1; dx++)
        for (int dy = -1; dy <= 1; dy++)
        {
            if (dx == 0 && dy == 0) continue;
            int checkX = node.gridX + dx;
            int checkY = node.gridY + dy;
            if (checkX >= 0 && checkX < _gridSizeX &&
                checkY >= 0 && checkY < _gridSizeY)
                neighbours.Add(_grid[checkX, checkY]);
        }
    return neighbours;
}
```

### AStarPathfinder.cs

`FindPath()` **ya está implementado** y no hay que tocarlo. Llama a los métodos que sí hay que implementar:

```csharp
// 4. GetMoveCost() — coste de moverse entre dos nodos adyacentes
float GetMoveCost(Node a, Node b)
{
    bool diagonal = Mathf.Abs(a.gridX - b.gridX) == 1
                 && Mathf.Abs(a.gridY - b.gridY) == 1;
    return diagonal ? 14f : 10f;
}

// 5. RetracePath() — reconstruir el camino siguiendo los parent
List<Node> RetracePath(Node startNode, Node endNode)
{
    var path = new List<Node>();
    Node current = endNode;
    while (current != startNode)
    {
        path.Add(current);
        current = current.parent;
    }
    path.Reverse();
    GridManager.instance.path = path;
    return path;
}

// 6. HeuristicEuclidean — distancia en línea recta
float HeuristicEuclidean(Node a, Node b)
{
    int dx = Mathf.Abs(a.gridX - b.gridX);
    int dy = Mathf.Abs(a.gridY - b.gridY);
    return Mathf.Sqrt(dx * dx + dy * dy) * 10f;
}

// 7. HeuristicManhattan — solo 4 direcciones
float HeuristicManhattan(Node a, Node b)
{
    return (Mathf.Abs(a.gridX - b.gridX) + Mathf.Abs(a.gridY - b.gridY)) * 10f;
}

// 8. HeuristicDiagonal — distancia de Chebyshev
float HeuristicDiagonal(Node a, Node b)
{
    return Mathf.Max(Mathf.Abs(a.gridX - b.gridX), Mathf.Abs(a.gridY - b.gridY)) * 10f;
}
```

**Diferencia entre heurísticas:**

| Heurística | Movimiento permitido | Característica |
|---|---|---|
| Manhattan | 4 direcciones | Exacta sin diagonales, sobreestima con diagonales |
| Euclidea | 8 direcciones | Subestima siempre → caminos más largos pero óptimos |
| Diagonal (Chebyshev) | 8 direcciones | Exacta con diagonales de coste uniforme |

### PathRequester.cs

Componente que se adjunta al agente. Recalcula el camino automáticamente si el target se mueve más de 0.5 unidades. Tecla configurable (por defecto Espacio) para iniciar/detener el seguimiento.

### Cómo montar el sistema en escena

1. Crear un `GameObject` vacío llamado `Grid`, asignarle `GridManager`. Configurar en Inspector:
   - `Grid World Size`: tamaño del área navegable (ej. 20×20)
   - `Node Radius`: 0.5 → celdas de 1×1 unidad
   - `Unwalkable Mask`: layer de los obstáculos
2. Crear otro `GameObject` llamado `Pathfinder`, asignarle `AStarPathfinder`.
3. Al agente que quiera navegar, asignarle `PathRequester` y configurar su `Target`.
4. Los obstáculos deben estar en la layer marcada en `Unwalkable Mask` y tener colisionador.

> **Extensión para el proyecto final:** añadir un float `moveCostMultiplier` a `Node` y multiplicarlo en `GetMoveCost()`. Las celdas oscuras tendrían `moveCostMultiplier = 3f` (mayor coste → A* las evita a menos que no haya alternativa).

---

## 3. Behavior Tree (BT)

**Carpeta:** `Ejercicio blackboard/BT/`

### Arquitectura de nodos

```
BTNode  (abstract)
  ├── Propiedades: Name (string), LastStatus (NodeStatus?)
  └── Método abstracto: Tick() → NodeStatus

NodeStatus  (enum): Running | Success | Failure

Nodos hoja:
  ├── Condition(Func<bool>)           → Success/Failure
  └── BTAction(Func<NodeStatus>)      → Running/Success/Failure

Nodos compuestos:
  ├── Selector(BTNode[])              → OR: devuelve el primer no-Failure
  ├── Sequence(BTNode[])              → AND: devuelve el primer no-Success
  └── Inverter(BTNode)               → invierte Success↔Failure

Todos guardan LastStatus para visualización en el editor.
```

### Reglas de evaluación

**Selector** (prioridad OR):
- Evalúa hijos de izquierda a derecha.
- Devuelve el estado del primer hijo que devuelva `Running` o `Success`.
- Si todos fallan → `Failure`.
- Uso: expresar prioridades (el comportamiento más urgente va primero).

**Sequence** (condición AND):
- Evalúa hijos de izquierda a derecha.
- Si alguno devuelve `Failure` o `Running` → la secuencia se detiene con ese estado.
- Solo devuelve `Success` si TODOS los hijos tienen éxito.
- Uso: `if (condición) { acción }` — el primer hijo es la condición, el segundo la acción.

**Inverter**:
- `Success` → `Failure`, `Failure` → `Success`, `Running` → `Running`.
- Uso: negar una condición (`if NOT CanSeePlayer → patrullar`).

### Enemigo_BT.cs

MonoBehaviour que **ya está completamente implementado** (es la solución del ejercicio). El árbol:

```
Selector (raíz)
├── Sequence "Huir si vida baja"
│   ├── Condition: LowHealth()         vida < 50%
│   └── BTAction:  Flee()
├── Sequence "Atacar si cerca"
│   ├── Condition: EstaCerca()         distancia < rangoAtaque
│   └── BTAction:  Attack()
├── Sequence "Perseguir si veo"
│   ├── Condition: CanSeePlayer()      distancia < rangoDeteccion
│   └── BTAction:  Chase()
├── Sequence "Investigar pista"
│   ├── Condition: HasLastKnownPosition()
│   └── BTAction:  Investigate()
└── Sequence "Patrullar (fallback)"
    └── BTAction:  Patrol()            siempre Running
```

Las condiciones y acciones son **métodos locales del MonoBehaviour** (no perciben mediante sensores externos). `_lastKnownPos` y `_hasLastKnownPos` son el "blackboard manual" interno.

---

## 4. Blackboard

**Carpeta:** `Ejercicio blackboard/Blackboard/`

### Concepto

El patrón Blackboard desacopla percepción de comportamiento:

```
Mundo → [Sensores] → Pizarra → [FSM / BT] → Acciones
```

Nadie se comunica directamente: los sensores escriben, los comportamientos leen.

### Blackboard.cs — `Dictionary<string, object>` genérico

Cuatro métodos a implementar:

```csharp
public void Set<T>(string key, T value)
    => _data[key] = value;

public T Get<T>(string key, T defaultValue = default)
{
    if (_data.TryGetValue(key, out object val)) return (T)val;
    return defaultValue;
}

public bool Has(string key) => _data.ContainsKey(key);

public void Remove(string key) => _data.Remove(key);
```

### BlackboardKeys.cs — `static class BB`

Constantes de tipo string que evitan errores de tipeo:

| Constante | Tipo | Escrita por |
|---|---|---|
| `BB.CanSeePlayer` | bool | VisionSensor |
| `BB.LastKnownPosition` | Vector3 | VisionSensor |
| `BB.HasClue` | bool | VisionSensor |
| `BB.Health` | float | HealthSensor |
| `BB.LowHealth` | bool | HealthSensor |
| `BB.HeardNoise` | bool | SoundSensor (bonus) |
| `BB.NoisePosition` | Vector3 | SoundSensor (bonus) |

Siempre usar `BB.NombreClave` en lugar de literales `"CanSeePlayer"`.

### Sensores — heredan de SensorBase

Cada sensor implementa `Sense()` y es llamado una vez por frame antes de que el comportamiento decida.

**VisionSensor.cs** — implementación:
```csharp
public override void Sense()
{
    if (_player == null) { _blackboard.Set<bool>(BB.CanSeePlayer, false); return; }
    bool inRange = Vector3.Distance(_origin.position, _player.position) < _range;
    _blackboard.Set<bool>(BB.CanSeePlayer, inRange);
    if (inRange)
    {
        _blackboard.Set<Vector3>(BB.LastKnownPosition, _player.position);
        _blackboard.Set<bool>(BB.HasClue, true);
    }
    // Al perder la visión: NO borrar LastKnownPosition ni HasClue
}
```

**HealthSensor.cs** — implementación:
```csharp
public override void Sense()
{
    float health = _getHealth();
    _blackboard.Set<float>(BB.Health, health);
    _blackboard.Set<bool>(BB.LowHealth, health < _maxHealth * 0.5f);
}
```

**SoundSensor.cs** — implementación (bonus):
```csharp
public override void Sense()
{
    if (_player == null) { _blackboard.Set<bool>(BB.HeardNoise, false); return; }
    bool makingNoise = Keyboard.current.eKey.isPressed;
    bool inRange = Vector3.Distance(_origin.position, _player.position) < _hearingRange;
    if (makingNoise && inRange)
    {
        _blackboard.Set<bool>(BB.HeardNoise, true);
        _blackboard.Set<Vector3>(BB.NoisePosition, _player.position);
        _blackboard.Set<Vector3>(BB.LastKnownPosition, _player.position);
        _blackboard.Set<bool>(BB.HasClue, true);
    }
    else
        _blackboard.Set<bool>(BB.HeardNoise, false);
}
```

### Enemigo_Blackboard.cs

FSM clásica (switch) que lee de la pizarra. Para completar `UpdateFSM()`:
```csharp
bool lowHealth    = _blackboard.Get<bool>(BB.LowHealth);
bool canSeePlayer = _blackboard.Get<bool>(BB.CanSeePlayer);
bool hasClue      = _blackboard.Get<bool>(BB.HasClue);
```

Y en `Start()`:
```csharp
_visionSensor = new VisionSensor(transform, player, detectionRange, _blackboard);
_healthSensor = new HealthSensor(() => health, maxHealth, _blackboard);
```

---

## 5. BT + Blackboard combinados

**Archivo:** `Enemigo_BT_Blackboard/Enemigo_BT_Blackboard.cs`

Es el sistema más completo: los **sensores** perciben el mundo y escriben en la pizarra; el **árbol BT** lee de la pizarra y decide. Las acciones también usan la pizarra (ej. `Chase()` lee `BB.LastKnownPosition` en lugar de acceder a `player.position` directamente).

Para completar `BuildTree()`:
```csharp
_tree = new Selector(
    new Sequence(new Condition(LowHealth, "VidaBaja?"), new BTAction(Flee, "Huir"))
        { Name = "Huir si vida baja" },
    new Sequence(new Condition(CanSeePlayer, "VeoJugador?"), new BTAction(Chase, "Perseguir"))
        { Name = "Perseguir si veo" },
    new Sequence(new Condition(HasClue, "TengoPista?"), new BTAction(Investigate, "Investigar"))
        { Name = "Investigar pista" },
    new Sequence(new BTAction(Patrol, "Patrullar"))
        { Name = "Patrullar (fallback)" }
) { Name = "Raíz (Selector)" };
```

Las condiciones leen de la pizarra:
```csharp
bool CanSeePlayer() => _blackboard.Get<bool>(BB.CanSeePlayer);
bool HasClue()      => _blackboard.Get<bool>(BB.HasClue);
```

**Diferencia clave** con `Enemigo_BT`: las condiciones ya no acceden al mundo directamente, solo a la pizarra.

---

## 6. Advanced BT — Conditional Aborts

**Carpeta:** `Unit5_AdvancedBT/`

### AbortType.cs

Define los tipos de interrupción que puede tener un nodo:

| Tipo | Comportamiento |
|---|---|
| `None` | Sin abort. Una vez en Running, sigue hasta terminar. |
| `Self` | La condición del propio nodo se reevalúa cada tick; aborta si falla. |
| `LowerPriority` | El Selector siempre reevalúa desde la rama de mayor prioridad. |
| `Both` | Combina Self y LowerPriority. |

### StickySelector.cs — Selector con cursor (NO reactivo)

Recuerda qué hijo estaba en `Running` y vuelve directamente a él, **sin reevaluar ramas de mayor prioridad**.

**Problema:** si mientras `Patrol` está en Running el enemigo recibe daño y `LowHealth` pasa a true, el árbol ignora `Flee` porque el cursor apunta a `Patrol`.

```
Frame 1: Patrol → Running, cursor = 2
Frame 2: LowHealth = true → va a cursor=2 (Patrol) → IGNORA Flee ← BUG
```

### Selector reactivo (Core/Selector.cs) — LowerPriority Abort

Siempre evalúa desde el hijo 0. Si una rama de alta prioridad se activa mientras una de baja prioridad estaba en `Running`, reacciona inmediatamente.

### ConditionalSequence.cs — Self Abort

En cada tick reevalúa el primer hijo (condición) antes de continuar con la acción. Si la condición falla, aborta la acción inmediatamente.

```
Frame 1: CanSeePlayer=true → Chase=Running
Frame 2: CanSeePlayer=false → Condition=Failure → Chase ABORTADA
```

### Enemigo_ConditionalAbort.cs

Permite alternar en el Inspector entre `StickySelector` y `Selector` reactivo en caliente (`useStickySelector`) para observar la diferencia de comportamiento.

---

## 7. Visualizador del árbol (Editor)

**Archivo:** `BehaviorTreeVisualización/BehaviorTreeInspector.cs`

`[CustomEditor(typeof(Enemigo_BT))]` — añade un panel al Inspector de `Enemigo_BT` que muestra el árbol en tiempo real durante Play Mode.

**Colores:**
- Ámbar → `Running`
- Verde → `Success`
- Rojo → `Failure`
- Gris → sin evaluar aún

Recorre el árbol recursivamente usando las propiedades `Children` (de `Selector` y `Sequence`) e `Inverter.Child`. Por eso los nodos del BT exponen estas propiedades con `IReadOnlyList<BTNode>`.

No requiere configuración: se activa automáticamente al seleccionar un GameObject con `Enemigo_BT` durante Play Mode.

---

## 8. Guía de implementación para el proyecto final

### Qué reutilizar del código de clase

| Sistema | Reutilizable | Modificación necesaria |
|---|---|---|
| `Node.cs` | ✅ Directo | Añadir `float moveCostMultiplier = 1f` para celdas oscuras |
| `GridManager.cs` | ✅ Directo | Implementar los 3 TODOs (ver sección 2) |
| `AStarPathfinder.cs` | ✅ Directo | Implementar los 5 TODOs (ver sección 2) |
| BT Core (`BTNode`, `Selector`, `Sequence`, etc.) | ✅ Directo | Ninguna |
| `Blackboard.cs` | ✅ Implementar | 4 métodos triviales |
| `BlackboardKeys.cs` | ✅ Ampliar | Añadir claves nuevas (`AlertLevel`, etc.) |
| Sensores | ✅ Implementar | `VisionSensor`, `HealthSensor`, `SoundSensor` |
| `Enemigo_BT_Blackboard.cs` | ✅ Base | Completar `BuildTree()` y ampliar |

### Arquitectura recomendada para el proyecto

```
GameObject "GridManager"
  └── GridManager (configura el mapa: walkable / obstacle / dark)

GameObject "Pathfinder"
  └── AStarPathfinder

GameObject "Enemy1" / "Enemy2"
  └── EnemyController  (MonoBehaviour principal)
      ├── crea Blackboard
      ├── crea VisionSensor + HealthSensor
      ├── construye el BT en Start()
      └── en Update(): Sense() → Tick() → mover con A*

GameObject "Player"
  └── PlayerMovement (WASD ya implementado)
```

### Cómo reemplazar NavMesh por A* en el movimiento del enemigo

El `PathRequester` actual mueve un objeto siguiendo el camino. Para el enemigo:

1. Llamar `AStarPathfinder.instance.FindPath(transform.position, destino)` → obtener `List<Node>`.
2. Avanzar nodo a nodo en `Update()` con `Vector3.MoveTowards`.
3. Recalcular cuando el destino cambia (jugador se mueve).

### Implementar celdas oscuras (mayor coste)

```csharp
// En Node.cs:
public float moveCostMultiplier = 1f;  // 1 = normal, 3 = oscuro

// En AStarPathfinder.GetMoveCost():
float GetMoveCost(Node a, Node b)
{
    float baseCost = (Mathf.Abs(a.gridX - b.gridX) == 1 &&
                      Mathf.Abs(a.gridY - b.gridY) == 1) ? 14f : 10f;
    return baseCost * b.moveCostMultiplier;
}

// En GridManager.CreateGrid(), después de crear cada Node:
if (Physics.CheckSphere(worldPoint, nodeRadius, darkZoneMask))
    _grid[x, y].moveCostMultiplier = 3f;
```

### Comunicación entre guardias (sistema multiagente)

El enfoque más simple y coherente con el código existente: usar un `EventBus` estático (ya existe en `Multiagentes/EventosComunicacion/EventBus.cs`) o una referencia directa entre los dos enemigos vía un manager.

Cuando `VisionSensor` detecta al jugador, el guardia alerta al otro escribiendo en la pizarra compartida del compañero:
```csharp
// En EnemyController, al detectar al jugador:
otherEnemy.blackboard.Set<bool>(BB.HasClue, true);
otherEnemy.blackboard.Set<Vector3>(BB.LastKnownPosition, playerPosition);
```

### Niveles de alerta progresivos (opcional)

Añadir a `BlackboardKeys.cs`:
```csharp
public const string AlertLevel = "AlertLevel";  // 0=Patrol, 1=Suspicious, 2=Alert, 3=Search
```

En `VisionSensor`, en lugar de booleano directo, incrementar el nivel según el tiempo de visión acumulado.
