using UnityEngine;

public class FleeState : IState
{
    private StateMachine enemy;

    public FleeState(StateMachine enemy) => this.enemy = enemy;

    public void OnEnter() => Debug.Log("Entrando a Al Huir");
    public void OnUpdate() => enemy.Flee();
    public void OnExit() { }
}
