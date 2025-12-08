from pydantic import BaseModel
from typing import List, Optional, Literal

# Modelo para una opción (usado en Multiple Choice)
class Opcion(BaseModel):
    id: str
    texto: str

# Modelo base para una pregunta
class Pregunta(BaseModel):
    id: int
    tipo: Literal['multiple_choice', 'ordenamiento', 'respuesta_corta', 'verdadero_falso', 'asociacion']
    enunciado: str
    # Opciones es opcional porque 'respuesta_corta' no tiene opciones visibles
    opciones: Optional[List[str]] = None 
    # Para ordenamiento, la respuesta correcta es la lista ordenada
    # Para choice, es el texto de la correcta
    respuesta_correcta: str | List[str] 
    explicacion: str

# Modelo para el examen completo
class ExamenGenerado(BaseModel):
    titulo: str
    tema_principal: str
    preguntas: List[Pregunta]