# Recapitulación del estado del proyecto

Fecha última actualización: 2026-05-29 · Unity 6000.0.59f2 (URP 17.0.4, Input System 1.14.2, AI Navigation 2.0.9)

---

## Trabajo realizado en esta sesión

1. **Limpieza de Scripts/Added**: eliminados duplicados y versiones antiguas.
   - Borrado: `BehaviorTree/` completo (esqueleto sin implementar, versión más antigua).
   - Borrado: `BehaviorTreeVisualización/BT/` (copia exacta de `Ejercicio blackboard/BT/`).
   - Borrado: todas las carpetas `__MACOSX/` y archivos `._*` (basura de macOS).
   - Conservado: `BehaviorTreeVisualización/BehaviorTreeInspector.cs` (archivo único).

2. **Documentación técnica** generada: `DOCUMENTACION_ADDED.md` con:
   - Funcionamiento completo de A*, BT, Blackboard, BT+Blackboard, Advanced BT.
   - Implementaciones de todos los TODOs del código de clase.
   - Guía de integración para el proyecto final.

---

## Estructura actual del proyecto

```
Assets/
  Scripts/
    Damage.cs                 (vacío)
    Enemy/
      EnemyAI.cs              (vacío)
      EnemyLife.cs            (vida + Scrollbar + tecla K debug) ✅
    Player/
      PlayerMovement.cs       (WASD + salto + gravedad) ✅
      PlayerCamera.cs         (follow con Lerp + LookAt) ✅
      PlayerAttack.cs         (vacío)
      PlayerLIfe.cs           (vacío) [typo: "LIfe"]
    States/                   (FSM sobre NavMesh — reemplazar por BT + A*)
      IState.cs / StateMachine.cs / PatrolState.cs / ChaseState.cs
      IdleState.cs / AttackState.cs (vacío) / FleeState.cs (vacío)

  Scripts/Added/              ← biblioteca de clase, referencia para implementar
    AStar/AStar/
      Node.cs                 ✅ completo
      GridManager.cs          ⚠️ CreateGrid, NodeFromWorldPoint, GetNeighbours → TODO
      AStarPathfinder.cs      ⚠️ GetMoveCost, RetracePath, 3 heurísticas → TODO
      PathRequester.cs        ✅ completo (seguidor de camino)

    Ejercicio blackboard/
      BT/Core/                ✅ BTNode, NodeStatus, BTAction, Condition,
                                 Selector, Sequence, Inverter — todos completos
      BT/Enemigo_BT.cs        ✅ árbol completo (Flee→Attack→Chase→Investigate→Patrol)
      Blackboard/Core/
        Blackboard.cs         ⚠️ Set/Get/Has/Remove → TODO (triviales)
        BlackboardKeys.cs     ✅ constantes BB.*
      Blackboard/Sensors/
        SensorBase.cs         ✅ clase base abstracta
        VisionSensor.cs       ⚠️ Sense() → TODO
        HealthSensor.cs       ⚠️ Sense() → TODO
        SoundSensor.cs        ⚠️ Sense() → TODO (bonus)
      Blackboard/Enemigo_Blackboard.cs  ⚠️ conectar sensores y pizarra → TODO

    Enemigo_BT_Blackboard/
      Enemigo_BT_Blackboard.cs  ⚠️ BuildTree + condiciones → TODO (esqueleto)

    BehaviorTreeVisualización/
      BehaviorTreeInspector.cs  ✅ inspector editor en tiempo real del BT

    Unit5_AdvancedBT/
      AbortType.cs / ConditionalSequence.cs / StickySelector.cs  ✅ completos
      Enemigo_ConditionalAbort.cs  ✅ demo StickySelector vs Selector reactivo

  Scenes/EntornoPruebas.unity   (modificada, sin commit)
  Resources/Materials/          (Enemy, PatrolPoints, Plane, Player, Visor)
  Settings/                     (URP PC + Mobile)
```

---

## Estado vs. enunciado

| Requisito | Estado |
|---|---|
| **Grid A\* propio (sin navmesh)** | ❌ Esqueleto en Added/. TODOs documentados. |
| Casillas navegables / obstáculo / **oscuras (mayor coste)** | ❌ Requiere `moveCostMultiplier` en Node + LayerMask extra |
| 2 enemigos con **Behavior Tree + Blackboard** | ❌ Solo hay FSM. Referencia completa en Added/. |
| **Alerta entre guardias** | ❌ Sin comunicación multiagente |
| Jugador movimiento libre | ✅ WASD implementado |
| Jugador **evita detección en zonas oscuras** | ❌ Sin lógica de ocultación |
| Ataque enemigo / daño al jugador | ❌ Attack() y PlayerLife vacíos |

### Opcionales
- Niveles de alerta progresivos ❌
- Pathfinding asíncrono ❌
- Costes dinámicos luz/oscuridad ❌

---

## Decisión de implementación (de DOCUMENTACION_ADDED.md)

El proyecto debe:
1. Implementar los TODOs de `GridManager` y `AStarPathfinder` (soluciones en DOCUMENTACION_ADDED.md §2).
2. Implementar `Blackboard`, los 3 sensores, y `BuildTree()` de `Enemigo_BT_Blackboard` (soluciones en §4 y §5).
3. Reemplazar `StateMachine.cs` (NavMesh + FSM) por `Enemigo_BT_Blackboard` usando A* para moverse.
4. Añadir `moveCostMultiplier` a `Node` para celdas oscuras.
5. Comunicación entre guardias: escritura cruzada en la pizarra del compañero al detectar al jugador.

## Archivos de documentación generados

- `RECAP.md` — este archivo
- `DOCUMENTACION_ADDED.md` — referencia técnica completa con implementaciones
