using UnityEngine;

public class PatrolState : IState
{
    private StateMachine enemy;

    public PatrolState(StateMachine enemy) => this.enemy = enemy;

    public void OnEnter()
    {        
        Debug.Log("Entrando a Patrulla");
    } 
    public void OnUpdate()
    {        
        enemy.Patrol();
    }
    public void OnExit() { }

}
