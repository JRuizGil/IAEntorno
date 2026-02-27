using UnityEngine;

public class PlayerCamera : MonoBehaviour
{
    public Transform target;        // El transform del jugador
    public float smoothSpeed = 0.125f; // Suavizado (0 a 1)
    public Vector3 offset;          // Distancia de separación (ej: 0, 5, -10)

    void LateUpdate()
    {
        // Calculamos la posición deseada sumando el offset al jugador
        Vector3 desiredPosition = target.position + offset;

        // Interpolación lineal para un movimiento fluido
        Vector3 smoothedPosition = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed);

        // Actualizamos la posición de la cámara
        transform.position = smoothedPosition;

        // Hacemos que la cámara siempre mire al jugador
        transform.LookAt(target);
    }
}