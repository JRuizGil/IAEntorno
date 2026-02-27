using UnityEngine;
using UnityEngine.UI; // Necesario para controlar el Scrollbar o Slider

public class EnemyLife : MonoBehaviour
{
    [Header("Configuración de Vida")]
    public float maxHealth = 100f;
    public float currentHealth;

    [Header("Interfaz de Usuario")]
    public Scrollbar healthBar; // Arrastra aquí tu Scrollbar desde el Inspector

    [Header("Ajustes de Prueba")]
    public KeyCode damageKey = KeyCode.K;

    void Start()
    {
        currentHealth = maxHealth;
        UpdateUI(); // Inicializar la barra al empezar
    }

    void Update()
    {
        if (Input.GetKeyDown(damageKey))
        {
            ApplyPercentageDamage(25f);
        }
    }

    public void ApplyPercentageDamage(float percentage)
    {
        float damageAmount = maxHealth * (percentage / 100f);
        TakeDamage(damageAmount);
    }

    public void TakeDamage(float amount)
    {
        currentHealth -= amount;
        currentHealth = Mathf.Clamp(currentHealth, 0f, maxHealth);

        UpdateUI(); // Actualizar la barra cada vez que reciba daño

        if (currentHealth <= 0)
        {
            Die();
        }
    }

    // Método para actualizar visualmente el Scrollbar
    void UpdateUI()
    {
        if (healthBar != null)
        {
            // El valor del Scrollbar (size) va de 0 a 1
            healthBar.size = currentHealth / maxHealth;
        }
    }

    void Die()
    {
        Destroy(gameObject);
    }
}