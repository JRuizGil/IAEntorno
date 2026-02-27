using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public CharacterController controller;

    public float speed = 12f;       // Velocidad de movimiento
    public float gravity = -19.62f; // Gravedad (el doble de la real se siente mejor en juegos)
    public float jumpHeight = 3f;   // Altura del salto

    public Transform groundCheck;   // Un objeto vacío a los pies del jugador
    public float groundDistance = 0.4f;
    public LayerMask groundMask;    // Capa para identificar qué es "suelo"

    Vector3 velocity;
    bool isGrounded;

    void Update()
    {
        // 1. Verificamos si estamos tocando el suelo
        isGrounded = Physics.CheckSphere(groundCheck.position, groundDistance, groundMask);

        if (isGrounded && velocity.y < 0)
        {
            velocity.y = -2f; // Mantiene al jugador pegado al suelo
        }

        // 2. Obtener inputs (Teclas WASD / Flechas)
        float x = Input.GetAxis("Horizontal");
        float z = Input.GetAxis("Vertical");

        // 3. Calcular dirección relativa al jugador
        Vector3 move = transform.right * x + transform.forward * z;

        controller.Move(move * speed * Time.deltaTime);

        // 4. Lógica de Salto
        if (Input.GetButtonDown("Jump") && isGrounded)
        {
            // Fórmula física: v = sqrt(h * -2 * g)
            velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);
        }

        // 5. Aplicar Gravedad
        velocity.y += gravity * Time.deltaTime;
        controller.Move(velocity * Time.deltaTime);
    }
}