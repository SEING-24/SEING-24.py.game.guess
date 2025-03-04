import os
import requests
import json
import random

# Función que muestra instrucciones al jugador
def mostrar_instrucciones():
    print("¡Bienvenido al juego Adivina un Número!")
    print("Debes adivinar un número secreto entre 1 y 100.")
    print("Después de cada intento, te diremos si el número es mayor o menor.")
    print("Si necesitas ayuda, el juego te dará una pista especial usando inteligencia artificial.")
    print("¡Buena suerte!\n")

# Función que consulta al modelo de GitHub Models en Azure
def obtener_pista_creativa(intentos, numero_secreto):
    endpoint = "https://models.inference.ai.azure.com"
    api_key = os.environ["GITHUB_TOKEN"]  # <- Reemplazar con clave real de Azure

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    mensajes = [
        {"role": "system", "content": "Eres un asistente experto en juegos de adivinanzas."},
        {"role": "user", "content": f"Estoy jugando a adivinar un número entre 1 y 100. Llevo {intentos} intentos y el número secreto es {numero_secreto}. Sin revelar el número exacto, dame una pista creativa para ayudarme a adivinarlo."}
    ]

    payload = {
        "model": "gpt-4o",  # O ajusta según el modelo habilitado en el endpoint
        "messages": mensajes,
        "temperature": 0.7
    }

    try:
        response = requests.post(f"{endpoint}/v1/chat/completions", headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            respuesta = response.json()
            return respuesta['choices'][0]['message']['content'].strip()
        else:
            return f"No se pudo obtener una pista (Código {response.status_code})."
    except Exception as e:
        return f"Error al consultar al modelo: {e}"

# Función para ejecutar una partida completa
def jugar_partida():
    numero_secreto = random.randint(1, 100)
    intentos = 0
    adivinado = False

    while not adivinado:
        try:
            intento = int(input("Introduce un número entre 1 y 100: "))
            if intento < 1 or intento > 100:
                print("Número fuera de rango, intenta de nuevo.")
                continue

            intentos += 1

            if intento < numero_secreto:
                print("El número secreto es mayor.")
            elif intento > numero_secreto:
                print("El número secreto es menor.")
            else:
                print(f"¡Felicidades! Adivinaste el número en {intentos} intentos.")
                adivinado = True

            # Cada 3 intentos fallidos, obtener una pista de la IA
            if not adivinado and intentos % 3 == 0:
                print("\n🤖 Consultando una pista especial...")
                pista = obtener_pista_creativa(intentos, numero_secreto)
                print(f"🔎 Pista IA: {pista}\n")

        except ValueError:
            print("Entrada inválida. Por favor, introduce un número válido.")

# Función principal para controlar el flujo general
def main():
    mostrar_instrucciones()
    while True:
        jugar_partida()
        jugar_de_nuevo = input("¿Quieres jugar otra vez? (s/n): ").strip().lower()
        if jugar_de_nuevo != 's':
            print("¡Gracias por jugar! Hasta la próxima.")
            break

# Ejecutar el juego
if __name__ == "__main__":
    main()
