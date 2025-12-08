import os
import json
from groq import Groq
from dotenv import load_dotenv
from fastapi import HTTPException

# Cargamos las variables de entorno
load_dotenv()

# Inicializamos el cliente de Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def generate_exam_questions(text: str):
    """
    Envía el texto a Groq (Llama 3) y recibe un JSON estructurado.
    """
    
    system_prompt = """
    Eres un profesor experto y estricto creando exámenes técnicos universitarios.
    
    TU OBJETIVO:
    Generar un examen basado EXCLUSIVAMENTE en el texto proporcionado.
    
    FORMATO DE SALIDA:
    Debes responder ÚNICAMENTE con un objeto JSON válido. No escribas introducciones como "Aquí tienes el JSON", solo el JSON.
    
    ESTRUCTURA DEL JSON:
    {
        "titulo": "Título descriptivo del examen",
        "tema_principal": "Tema central del texto",
        "preguntas": [
            {
                "id": 1,
                "tipo": "multiple_choice",
                "enunciado": "¿Pregunta?",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "La opción correcta exacta",
                "explicacion": "Breve justificación."
            },
            {
                "id": 2,
                "tipo": "verdadero_falso",
                "enunciado": "Afirmación.",
                "respuesta_correcta": "Verdadero", 
                "explicacion": "Justificación."
            },
            {
                "id": 3,
                "tipo": "respuesta_corta",
                "enunciado": "Pregunta de respuesta breve.",
                "respuesta_correcta": "Respuesta (máx 3 palabras)",
                "explicacion": "Contexto."
            }
        ]
    }
    
    REGLAS:
    1. Genera 5 preguntas mezclando los tipos.
    2. Si el texto es técnico, las preguntas deben ser difíciles.
    3. Asegúrate de que el JSON esté bien formado.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"Genera el examen para este texto: {text[:20000]}"
                }
            ],
            # Usamos Llama 3.3 Versatile (Rápido, inteligente y maneja bien JSON)
            model="llama-3.3-70b-versatile",
            
            # Esto fuerza a la IA a devolver JSON sí o sí
            response_format={"type": "json_object"}, 
            
            temperature=0.3,
        )

        # Procesamos la respuesta
        exam_content = chat_completion.choices[0].message.content
        exam_json = json.loads(exam_content)
        
        return exam_json

    except json.JSONDecodeError:
        # A veces la IA falla en cerrar un corchete, esto nos avisa
        raise HTTPException(status_code=500, detail="La IA generó un formato inválido. Intenta de nuevo.")
    except Exception as e:
        print(f"Error en Groq: {e}")
        raise HTTPException(status_code=500, detail=f"Error al conectar con la IA: {str(e)}")