using UnityEngine;
using UnityEngine.AI;

public class StateMachine : MonoBehaviour
{
    // Referencias a los estados
    public PatrolState patrolState;
    public ChaseState chaseState;
    public IdleState idleState;
    public AttackState attackState;
    public FleeState fleeState;

    private IState currentState;

    [Header("Detección")]
    public float sightRange = 10f;
    public bool playerInSightRange;
    [Header("Detección Ataque")]
    public float attackSightRange = 1.5f;
    public bool playerInAttackRange;
    [Header("Ruta de Patrulla")]
    public Transform[] waypoints; // Arrastra aquí tus 4 objetos
    private int currentWaypointIndex = 0;
    public float waitTime = 2f;    // Tiempo que se queda en Idle en cada punto
    public float waitTimer;
    private bool isWaiting;
    [Header("Navmesh & PlayerTransform")]
    public NavMeshAgent agent;
    private Transform player;
    public LayerMask whatIsPlayer;
    [Header("EnemyComponents")]
    private EnemyLife enemyLife;
    private void Awake()
    {
        enemyLife = GetComponent<EnemyLife>();
        agent = GetComponent<NavMeshAgent>();
        player = GameObject.FindGameObjectWithTag("Player").transform;
        isWaiting = false;

    }
    private void Start()
    {
        // Inicializamos los estados
        patrolState = new PatrolState(this);
        chaseState = new ChaseState(this);
        idleState = new IdleState(this);
        attackState = new AttackState(this);
        fleeState = new FleeState(this);

        // Estado inicial
        ChangeState(patrolState);
    }
    private void Update()
    {
        // 1. Lógica de transición
        bool playerInSight = Physics.CheckSphere(transform.position, sightRange, whatIsPlayer);
        bool playerInAttackSight = Physics.CheckSphere(transform.position, attackSightRange, whatIsPlayer);

        if (playerInSight && currentState != chaseState)
            ChangeState(chaseState);
        else if (!playerInSight && currentState == chaseState)
            ChangeState(patrolState);
        
            // 2. Ejecutar el Update del estado actual
            currentState?.OnUpdate();
    }
    public void ChangeState(IState newState)
    {
        currentState?.OnExit();
        currentState = newState;
        currentState.OnEnter();
    }
    public void Patrol()
    {    
        GoToNextWaypoint();
        if (!agent.pathPending && agent.remainingDistance < 0.5f)
        {            
            ChangeState(idleState);
        }
        // que cambie de siguiente punto de patrulla.
    }
    public void GoToNextWaypoint()
    {
        // Incrementamos el índice y volvemos a 0 si llegamos al final
        currentWaypointIndex = (currentWaypointIndex + 1) % waypoints.Length;
        agent.SetDestination(waypoints[currentWaypointIndex].position);
    }
    public void Chase()
    {
        // Interrumpir el Idle si ve al jugador
        agent.SetDestination(player.position);
    }
    public void Idle()
    {
        waitTimer += Time.deltaTime;
        if (waitTimer >= waitTime)
        {            
            ChangeState(patrolState);            
        }
    }
    public void Attack()
    {

    }
    public void Flee()
    {

    }
    private void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, sightRange);
    }
}
