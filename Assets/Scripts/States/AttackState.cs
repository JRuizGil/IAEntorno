using UnityEngine;

public class AttackState : IState
{
    private StateMachine enemy;

    public AttackState(StateMachine enemy) => this.enemy = enemy;

    public void OnEnter() => Debug.Log("Entrando a Al Ataque");
    public void OnUpdate() => enemy.Attack();
    public void OnExit() { }
}
