import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(page_title="Generador de Exámenes IA", page_icon="🎓")

st.title("🎓 Generador de Exámenes con IA")
st.write("Sube tus apuntes (PDF) y la IA generará un examen para ti.")

# --- BARRA LATERAL (Uploader) ---
with st.sidebar:
    st.header("1. Cargar Archivo")
    archivo_pdf = st.file_uploader("Sube tu PDF aquí", type="pdf")
    
    boton_generar = st.button("Generar Examen 🚀", type="primary")

# --- LÓGICA DE ESTADO (Memoria) ---
# Usamos session_state para que el examen no se borre al interactuar con la página
if 'examen' not in st.session_state:
    st.session_state.examen = None
if 'respuestas_usuario' not in st.session_state:
    st.session_state.respuestas_usuario = {}
if 'corregido' not in st.session_state:
    st.session_state.corregido = False

# --- LÓGICA PRINCIPAL ---
if boton_generar and archivo_pdf:
    with st.spinner('Leyendo PDF y generando preguntas... (Esto puede tardar unos segundos)'):
        try:
            # 1. Preparamos el archivo para enviarlo a FastAPI
            files = {"archivo": (archivo_pdf.name, archivo_pdf, "application/pdf")}
            
            # 2. Hacemos la petición al Backend (asegúrate que la URL sea correcta)
            response = requests.post("http://127.0.0.1:8000/generar-examen", files=files)
            
            if response.status_code == 200:
                st.session_state.examen = response.json()
                st.session_state.corregido = False
                st.session_state.respuestas_usuario = {} # Reseteamos respuestas
                st.success("¡Examen generado con éxito!")
            else:
                st.error(f"Error del servidor: {response.text}")
                
        except Exception as e:
            st.error(f"Error de conexión: {e}. ¿Está el backend encendido?")

# --- MOSTRAR EXAMEN ---
if st.session_state.examen:
    examen = st.session_state.examen
    st.header(f"📝 {examen.get('titulo', 'Examen Generado')}")
    st.info(f"Tema: {examen.get('tema_principal', 'General')}")
    
    # Formulario para las respuestas
    with st.form("form_examen"):
        for i, pregunta in enumerate(examen['preguntas']):
            st.markdown(f"### {i+1}. {pregunta['enunciado']}")
            
            # ID único para cada widget
            widget_key = f"preg_{pregunta['id']}"
            
            # Renderizar según el tipo
            if pregunta['tipo'] == 'multiple_choice':
                st.radio(
                    "Elige una opción:",
                    pregunta['opciones'],
                    key=widget_key
                )
            
            elif pregunta['tipo'] == 'verdadero_falso':
                st.radio(
                    "¿Verdadero o Falso?",
                    ["Verdadero", "Falso"],
                    key=widget_key
                )
                
            elif pregunta['tipo'] == 'respuesta_corta':
                st.text_input("Tu respuesta:", key=widget_key)
            
            st.divider()
        
        # Botón de corrección
        enviado = st.form_submit_button("Corregir Examen ✅")
        
        if enviado:
            st.session_state.corregido = True

    # --- MOSTRAR RESULTADOS ---
    if st.session_state.corregido:
        st.subheader("📊 Resultados")
        aciertos = 0
        total = len(examen['preguntas'])
        
        for i, pregunta in enumerate(examen['preguntas']):
            widget_key = f"preg_{pregunta['id']}"
            respuesta_user = st.session_state.get(widget_key)
            respuesta_correcta = pregunta['respuesta_correcta']
            
            st.markdown(f"**Pregunta {i+1}:** {pregunta['enunciado']}")
            
            # Comparación simple (OJO: en respuesta corta debería ser más flexible)
            es_correcto = str(respuesta_user).strip().lower() == str(respuesta_correcta).strip().lower()
            
            if es_correcto:
                st.success(f"✅ Correcto. Tu respuesta: {respuesta_user}")
                aciertos += 1
            else:
                st.error(f"❌ Incorrecto. Tu respuesta: {respuesta_user}")
                st.info(f"👉 Respuesta correcta: {respuesta_correcta}")
                st.warning(f"💡 Explicación: {pregunta['explicacion']}")
            
            st.divider()
            
        nota = (aciertos / total) * 10
        st.metric(label="Calificación Final", value=f"{nota:.1f} / 10")
        if nota >= 6:
            st.balloons()