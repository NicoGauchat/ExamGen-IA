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
    
 
    system_prompt = """
    Eres un profesor experto y creativo creando exámenes universitarios.
    
    TU OBJETIVO:
    Generar un examen exhaustivo basado EXCLUSIVAMENTE en el texto proporcionado.
    
    REGLAS ESTRICTAS:
    1. CANTIDAD: Genera AL MENOS 50 preguntas (o tantas como el texto permita sin inventar).
    2. VARIEDAD: Mezcla tipos de preguntas (multiple_choice, verdadero_falso, asociacion, respuesta_corta).
    3. TIPO "ASOCIACIÓN": 
       - 'items_izquierda': Lista de conceptos.
       - 'opciones': Lista de definiciones (desordenadas).
       - 'respuesta_correcta': Un objeto JSON que mapee cada concepto con su definición correcta.
    4. OPCIÓN "NINGUNA DE LAS ANTERIORES": En las preguntas 'multiple_choice', incluye esta opción aleatoriamente.
    5. ALEATORIEDAD: No repitas patrones.
    
    ESTRUCTURA DEL JSON (Ejemplos de cómo deben verse los distintos tipos):
    {
        "titulo": "Título del Examen",
        "tema_principal": "Tema General",
        "preguntas": [
            {
                "id": 1,
                "tipo": "asociacion",
                "enunciado": "Une los conceptos con sus definiciones correspondientes",
                "items_izquierda": ["Concepto A", "Concepto B"],
                "opciones": ["Definición para B", "Definición para A"],
                "respuesta_correcta": {"Concepto A": "Definición para A", "Concepto B": "Definición para B"},
                "explicacion": "Justificación de la unión."
            },
            {
                "id": 2,
                "tipo": "multiple_choice",
                "enunciado": "¿Cuál es la capital de Francia?",
                "opciones": ["Madrid", "París", "Berlín"],
                "respuesta_correcta": "París",
                "explicacion": "París es la capital de Francia."
            }
        ]
    }
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
                    # Añadimos una instrucción extra al final para reforzar la unicidad
                    "content": f"Genera un examen completamente nuevo y diferente a los habituales para este texto. Texto: {text[:30000]}"
                }
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}, 
            
            # SUBIMOS LA TEMPERATURA PARA MAYOR VARIEDAD (Antes 0.3 -> Ahora 0.7 o 0.8)
            temperature=0.7, 
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