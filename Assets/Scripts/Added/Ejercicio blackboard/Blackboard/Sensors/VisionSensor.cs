// ============================================================
//  EJERCICIO: BLACKBOARD — Parte 2a (Ampliación)
// ============================================================
//
//  VisionSensor simula los "ojos" del enemigo.
//  Cada frame comprueba si el jugador está en rango y
//  escribe el resultado en la pizarra.
//
//  CLAVES QUE DEBES ESCRIBIR:
//    BB.CanSeePlayer      (bool)    → true si el jugador está en rango
//    BB.LastKnownPosition (Vector3) → posición del jugador cuando es visible
//    BB.HasClue           (bool)    → true en cuanto se ha visto al jugador
//
//  REGLA IMPORTANTE:
//    Cuando el jugador SALE del rango, pon BB.CanSeePlayer = false,
//    pero NO borres BB.LastKnownPosition ni BB.HasClue.
//    Esos datos son la "memoria" que usará el estado Investigate.
//
//  REFLEXIÓN:
//    Compara esta solución con ChaseState.OnExit() de la FSM:
//
//      // ChaseState.cs (Enemigo_FSM):
//      public override void OnExit()
//      {
//          enemy.lastKnownPlayerPos = enemy.jugador.position;
//      }
//
//    Con la pizarra + sensor, ya no hace falta capturar la posición
//    en OnExit(): el sensor la actualiza continuamente y la conserva
//    automáticamente al perder la visión.
//
// ============================================================

using UnityEngine;

public class VisionSensor : SensorBase
{
    readonly Transform _origin;
    readonly Transform _player;
    readonly float     _range;
    readonly UnityEngine.LayerMask _darkZoneMask;

    public VisionSensor(Transform origin, Transform player, float range, Blackboard blackboard,
        UnityEngine.LayerMask darkZoneMask = default)
        : base(blackboard)
    {
        _origin       = origin;
        _player       = player;
        _range        = range;
        _darkZoneMask = darkZoneMask;
    }

    public override void Sense()
    {
        if (_player == null)
        {
            _blackboard.Set<bool>(BB.CanSeePlayer, false);
            return;
        }

        // Reduce el rango si el jugador está en zona oscura (stealth)
        float effectiveRange = _range;
        if (_darkZoneMask.value != 0 &&
            UnityEngine.Physics.CheckSphere(_player.position, 0.3f, _darkZoneMask))
            effectiveRange *= 0.3f;

        bool inRange = UnityEngine.Vector3.Distance(_origin.position, _player.position) < effectiveRange;
        _blackboard.Set<bool>(BB.CanSeePlayer, inRange);

        if (inRange)
        {
            _blackboard.Set<UnityEngine.Vector3>(BB.LastKnownPosition, _player.position);
            _blackboard.Set<bool>(BB.HasClue, true);
        }
    }
}
