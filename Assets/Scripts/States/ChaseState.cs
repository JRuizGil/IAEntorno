using UnityEngine;

public class ChaseState : IState
{
    private StateMachine enemy;

    public ChaseState(StateMachine enemy) => this.enemy = enemy;

    public void OnEnter() => Debug.Log("Entrando a Al Seguir");
    public void OnUpdate() => enemy.Chase();
    
    public void OnExit() { }
}
