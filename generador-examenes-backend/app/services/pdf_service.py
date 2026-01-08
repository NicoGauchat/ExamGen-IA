from pypdf import PdfReader
from fastapi import UploadFile, HTTPException

def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Recibe un archivo PDF subido y extrae todo su texto.
    """
    try:
        # Creamos el lector de PDF usando el archivo en memoria
        pdf_reader = PdfReader(file.file)
        
        text = ""
        # Recorremos cada página y extraemos el texto
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        
        # Validación básica
        if not text.strip():
            raise HTTPException(status_code=400, detail="No se pudo extraer texto del PDF. Asegúrate de que no sea una imagen escaneada.")
            
        return text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {str(e)}")