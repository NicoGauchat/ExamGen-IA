from fastapi import FastAPI, UploadFile, File, HTTPException
from app.models import ExamenGenerado
from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import generate_exam_questions # Importamos el servicio de IA

app = FastAPI(
    title="Generador de Exámenes con IA",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "El servidor está corriendo correctamente 🚀"}

@app.post("/generar-examen", response_model=ExamenGenerado) 
async def generar_examen(archivo: UploadFile = File(...)):
    """
    Flujo completo: PDF -> Texto -> IA -> Examen JSON
    """
    # 1. Validar PDF
    if not archivo.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

    # 2. Extraer texto
    texto_pdf = extract_text_from_pdf(archivo)

    # 3. Generar examen con IA
    examen = generate_exam_questions(texto_pdf)
    
    return examen