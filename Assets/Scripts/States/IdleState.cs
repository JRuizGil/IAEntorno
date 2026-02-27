using UnityEngine;

public class IdleState : IState
{
    private StateMachine enemy;

    public IdleState(StateMachine enemy) => this.enemy = enemy;

    public void OnEnter()
    {
        Debug.Log("Iniciando espera...");
        enemy.waitTimer = 0f; // Resetear el tiempo cada vez que entramos en Idle
        enemy.agent.isStopped = true; // Detener el movimiento del NavMesh
    }    
    public void OnUpdate() => enemy.Idle();
    public void OnExit() { }
}
