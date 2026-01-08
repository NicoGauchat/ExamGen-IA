import streamlit as st
import requests
import json
import random      
import difflib


if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

st.set_page_config(
    page_title="ExamGen AI - Generador Inteligente de Exámenes",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
)

st.markdown("""
<style>

    
  
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    .block-container {
        max-width: 100% !important;
        padding-top: 2rem !important;
        padding-right: 2rem !important;
        padding-left: 2rem !important;
        padding-bottom: 2rem !important;
    }
            
         section[data-testid="stSidebar"][aria-expanded="true"] {
        width: 400px !important;
        min-width: 400px !important;
        max-width: 400px !important;
    }   
   section[data-testid="stSidebar"] {
        width: 400px;
    }
    /* Variables de tema */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --primary-light: #818cf8;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --neutral-50: #fafafa;
        --neutral-100: #f5f5f5;
        --neutral-200: #e5e5e5;
        --neutral-300: #d4d4d4;
        --neutral-700: #404040;
        --neutral-800: #262626;
        --neutral-900: #171717;
        --neutral-400: #a1a1aa; 
    }
    
    /* Estilos globales */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #fafafa 0%, #f0f0f5 100%);
    }
    
    /* Título principal*/
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em;
    }
    
    /* Subtítulos modernos */
    h2 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: var(--neutral-800) !important;
        font-size: 2rem !important;
        margin-top: 2rem !important;
        letter-spacing: -0.01em;
    }
    
    h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: var(--neutral-700) !important;
        font-size: 1.5rem !important;
        margin-top: 1.5rem !important;
    }
    

    .stContainer > div {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    
    .stContainer > div:hover {
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
   
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        border: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.01em;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-2px);
    }
    
    /* Fixed text color contrast for secondary buttons */
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: var(--neutral-700) !important;
        border: 2px solid var(--neutral-200) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: var(--neutral-50) !important;
        border-color: var(--primary) !important;
        color: var(--primary) !important;
    }
    
   
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 2px solid var(--neutral-200) !important;
        padding: 0.75rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
        background: white !important;
        color: var(--neutral-800) !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--neutral-400) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
 
    .stTextInput > label,
    .stTextArea > label {
        color: var(--neutral-700) !important;
        font-weight: 500 !important;
    }
    
 
    .stRadio > label {
        font-weight: 500 !important;
        color: var(--neutral-700) !important;
        font-size: 0.95rem !important;
    }
    
    .stRadio > div {
        gap: 0.75rem !important;
    }
    
 
    .stRadio > div > label {
        background: white !important;
        border: 2px solid var(--neutral-200) !important;
        border-radius: 10px !important;
        padding: 0.875rem 1.25rem !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
        color: #000000 !important;
    }
    
            .stRadio > div > label p {
        color: #000000 !important;
    }
            
    .stRadio > div > label:hover {
        border-color: var(--primary-light) !important;
        background: var(--neutral-50) !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        border-color: var(--primary) !important;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%) !important;
        font-weight: 600 !important;
        color: var(--primary) !important;
    }
    
 
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        padding: 1rem 1.25rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
  
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%) !important;
        border-left: 4px solid var(--success) !important;
        color: var(--neutral-800) !important;
    }
    

    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%) !important;
        border-left: 4px solid var(--danger) !important;
        color: var(--neutral-800) !important;
    }
    
   
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.05) 100%) !important;
        border-left: 4px solid var(--warning) !important;
        color: var(--neutral-800) !important;
    }
    
    /* Info messages */
    .stInfo {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(79, 70, 229, 0.05) 100%) !important;
        border-left: 4px solid var(--primary) !important;
        color: var(--neutral-800) !important;
    }
    
 
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.1) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: var(--neutral-800) !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--neutral-800) !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--neutral-700) !important;
    }
    
    
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px dashed rgba(99, 102, 241, 0.3) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(99, 102, 241, 0.6) !important;
        background: rgba(255, 255, 255, 0.7) !important;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15) !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: var(--neutral-800) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    [data-testid="stFileUploader"] section {
        background: transparent !important;
        border: none !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%) !important;
        border: 2px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: var(--neutral-600) !important;
        font-size: 0.875rem !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
   
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 10px !important;
        border: 2px solid var(--neutral-200) !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        transition: all 0.2s ease !important;
        color: var(--neutral-800) !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--primary) !important;
        background: var(--neutral-50) !important;
    }
    

    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, var(--neutral-300) 50%, transparent 100%) !important;
    }
    

    [data-testid="stMetric"] {
        background: white !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border: 2px solid var(--neutral-200) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--neutral-700) !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: var(--primary) !important;
    }
    

    .stSpinner > div {
        border-color: var(--primary) !important;
    }
    
  
    .question-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
    }
    

    .matching-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 2px solid var(--neutral-200);
        margin: 1rem 0;
    }
    
    .matching-header {
        font-weight: 600;
        color: var(--neutral-700);
        margin-bottom: 1rem;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
  
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stContainer > div {
        animation: fadeIn 0.4s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DEL SESSION STATE ---
if 'examen' not in st.session_state:
    st.session_state.examen = None
if 'respuestas_usuario' not in st.session_state:
    st.session_state.respuestas_usuario = {}
if 'corregido' not in st.session_state:
    st.session_state.corregido = False
if 'matching_pairs' not in st.session_state:
    st.session_state.matching_pairs = {}
if 'matching_selected_left' not in st.session_state:
    st.session_state.matching_selected_left = {}

# --- FUNCIONES AUXILIARES PARA ASOCIACIÓN ---
def init_matching_state(pregunta_id, items_izq, items_der):
    """Inicializa el estado de emparejamiento y MEZCLA las opciones"""
    if pregunta_id not in st.session_state.matching_pairs:
        st.session_state.matching_pairs[pregunta_id] = {}
    if pregunta_id not in st.session_state.matching_selected_left:
        st.session_state.matching_selected_left[pregunta_id] = None
    

    key_shuffled = f"shuffled_{pregunta_id}"
    if key_shuffled not in st.session_state:
      
        opciones_mezcladas = items_der.copy()
        random.shuffle(opciones_mezcladas)
        st.session_state[key_shuffled] = opciones_mezcladas
def select_left_item(pregunta_id, item):
    """Selecciona un ítem de la izquierda"""
    st.session_state.matching_selected_left[pregunta_id] = item

def create_pair(pregunta_id, item_left, item_right):
    """Crea un par entre ítem izquierdo y derecho"""
    if pregunta_id not in st.session_state.matching_pairs:
        st.session_state.matching_pairs[pregunta_id] = {}
    st.session_state.matching_pairs[pregunta_id][item_left] = item_right
    st.session_state.matching_selected_left[pregunta_id] = None

def remove_pair(pregunta_id, item_left):
    """Elimina un par formado"""
    if pregunta_id in st.session_state.matching_pairs:
        if item_left in st.session_state.matching_pairs[pregunta_id]:
            del st.session_state.matching_pairs[pregunta_id][item_left]

def render_matching_question(pregunta, pregunta_num):
    """Renderiza una pregunta de asociación con opciones mezcladas"""
    pregunta_id = pregunta['id']
    items_izq = pregunta.get('items_izquierda', [])
    items_der = pregunta.get('opciones', []) 
    
   
    init_matching_state(pregunta_id, items_izq, items_der)
    
  
    shuffled_right = st.session_state[f"shuffled_{pregunta_id}"]
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem; border-left: 4px solid #6366f1;'>
        <strong>Instrucciones:</strong> Haz clic en un concepto de la columna izquierda, luego selecciona 
        su definición correspondiente en la columna derecha para formar la pareja.
    </div>
    """, unsafe_allow_html=True)
    
   
    formed_pairs = st.session_state.matching_pairs.get(pregunta_id, {})
    selected_left = st.session_state.matching_selected_left.get(pregunta_id)
    
    
    paired_left = set(formed_pairs.keys())
    paired_right = set(formed_pairs.values())
    
    col_left, col_space, col_right = st.columns([5, 1, 5])
    
    with col_left:
        st.markdown("<div class='matching-header'>Conceptos</div>", unsafe_allow_html=True)
        for item in items_izq:
            if item in paired_left:
                st.button(
                    f"✓ {item}",
                    key=f"left_{pregunta_id}_{item}_paired",
                    disabled=True,
                    use_container_width=True,
                    type="secondary"
                )
            else:
                is_selected = (item == selected_left)
                if st.button(
                    item,
                    key=f"left_{pregunta_id}_{item}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    select_left_item(pregunta_id, item)
                    st.rerun()
    
    with col_space:
        st.markdown("<div style='text-align: center; padding-top: 30px; font-size: 1.5rem;'>→</div>", unsafe_allow_html=True)
    
    with col_right:
        st.markdown("<div class='matching-header'>Definiciones</div>", unsafe_allow_html=True)
        for item in shuffled_right:
            if item in paired_right:
                st.button(
                    f"✓ {item}",
                    key=f"right_{pregunta_id}_{item}_paired",
                    disabled=True,
                    use_container_width=True,
                    type="secondary"
                )
            else:
                if st.button(
                    item,
                    key=f"right_{pregunta_id}_{item}",
                    use_container_width=True,
                    type="secondary"
                ):
                    if selected_left:
                        create_pair(pregunta_id, selected_left, item)
                        st.rerun()
                    else:
                        st.warning("Primero selecciona un concepto de la columna izquierda")
    
    if formed_pairs:
        st.markdown("---")
        st.markdown("**Parejas Formadas:**")
        for left_item, right_item in formed_pairs.items():
            col1, col2 = st.columns([9, 1])
            with col1:
                st.success(f"{left_item}  →  {right_item}")
            with col2:
                if st.button("✕", key=f"undo_{pregunta_id}_{left_item}", help="Deshacer pareja"):
                    remove_pair(pregunta_id, left_item)
                    st.rerun()
    
    # Guardar en respuestas_usuario
    st.session_state.respuestas_usuario[pregunta_id] = formed_pairs.copy()

# --- ENCABEZADO PRINCIPAL ---
st.markdown("<h1>ExamGen AI</h1>", unsafe_allow_html=True)
st.markdown("**Generador Inteligente de Exámenes** • Sube tus apuntes y deja que la IA haga el resto")
st.markdown("---")

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("### Carga tu Material")
    st.caption("Sube un archivo PDF con tus apuntes o material de estudio")
    
    archivo_pdf = st.file_uploader("Selecciona tu PDF", type="pdf", label_visibility="collapsed")
    
    st.markdown("")  # Espaciado
    boton_generar = st.button("✨ Generar Examen", type="primary", use_container_width=True)
    
    if st.session_state.examen:
        st.markdown("---")
        num_preguntas = len(st.session_state.examen['preguntas'])
        st.metric("Total de Preguntas", num_preguntas)
        
        if st.session_state.examen.get('tema_principal'):
            st.markdown(f"**Tema Detectado**  \n{st.session_state.examen['tema_principal']}")
    
    st.markdown("---")
    st.markdown("### Acerca de ExamGen")
    st.caption("Plataforma de generación de exámenes impulsada por inteligencia artificial. Crea evaluaciones personalizadas en segundos.")

# --- GENERACIÓN DEL EXAMEN ---
if boton_generar and archivo_pdf:
    with st.spinner('Analizando el contenido y generando preguntas inteligentes...'):
        try:
            files = {"archivo": (archivo_pdf.name, archivo_pdf, "application/pdf")}
            response = requests.post("http://127.0.0.1:8000/generar-examen", files=files)
            
            if response.status_code == 200:
                st.session_state.examen = response.json()
                st.session_state.corregido = False
                st.session_state.respuestas_usuario = {}
                st.session_state.matching_pairs = {}
                st.session_state.matching_selected_left = {}
                st.session_state.sidebar_state = 'collapsed'
                st.success("Examen generado exitosamente")
                st.rerun()
            else:
                st.error(f"Error al generar el examen: {response.text}")
                
        except Exception as e:
            st.error(f"Error de conexión con el servidor. Verifica que el backend esté en ejecución.")

# --- MOSTRAR EXAMEN ---
if st.session_state.examen:
    examen = st.session_state.examen
    
    st.markdown(f"## {examen.get('titulo', 'Tu Examen')}")
    
    if examen.get('tema_principal'):
        st.info(f"**Tema Principal:** {examen['tema_principal']}")
    
    st.markdown("---")
    
    for i, pregunta in enumerate(examen['preguntas']):
        pregunta_id = pregunta['id']
        
        with st.container():
            # Badge de número de pregunta
            st.markdown(f"<div class='question-badge'>Pregunta {i+1} de {len(examen['preguntas'])}</div>", unsafe_allow_html=True)
            st.markdown(f"### {pregunta['enunciado']}")
            
            # Renderizar según el tipo
            if pregunta['tipo'] == 'multiple_choice':
                widget_key = f"preg_{pregunta_id}"
                respuesta = st.radio(
                    "Selecciona tu respuesta:",
                    pregunta['opciones'],
                    key=widget_key,
                    index=None,
                    label_visibility="visible"
                )
                st.session_state.respuestas_usuario[pregunta_id] = respuesta
            
            elif pregunta['tipo'] == 'verdadero_falso':
                widget_key = f"preg_{pregunta_id}"
                respuesta = st.radio(
                    "¿Verdadero o Falso?",
                    ["Verdadero", "Falso"],
                    key=widget_key,
                    index=None,
                    label_visibility="visible"
                )
                st.session_state.respuestas_usuario[pregunta_id] = respuesta
            
            elif pregunta['tipo'] == 'respuesta_corta':
                widget_key = f"preg_{pregunta_id}"
                respuesta = st.text_input(
                    "Escribe tu respuesta:",
                    key=widget_key,
                    placeholder="Ingresa tu respuesta aquí...",
                    label_visibility="visible"
                )
                st.session_state.respuestas_usuario[pregunta_id] = respuesta
            
            elif pregunta['tipo'] == 'asociacion':
                render_matching_question(pregunta, i+1)
            
            st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        if st.button("Enviar Examen para Corrección", type="primary", use_container_width=True):
            st.session_state.corregido = True
            st.rerun()

    # --- MOSTRAR RESULTADOS ---
    if st.session_state.corregido:
        st.markdown("---")
        st.markdown("## Resultados de tu Examen")
        
        aciertos = 0
        total_puntos = 0
        puntos_obtenidos = 0
        
        for i, pregunta in enumerate(examen['preguntas']):
            pregunta_id = pregunta['id']
            respuesta_user = st.session_state.respuestas_usuario.get(pregunta_id)
            respuesta_correcta = pregunta['respuesta_correcta']
            
            with st.container():
                st.markdown(f"<div class='question-badge'>Pregunta {i+1}</div>", unsafe_allow_html=True)
                st.markdown(f"**{pregunta['enunciado']}**")
                
                # Corrección según tipo de pregunta
                if pregunta['tipo'] == 'asociacion':
                    if isinstance(respuesta_user, dict) and isinstance(respuesta_correcta, dict):
                        pares_correctos = 0
                        total_pares = len(respuesta_correcta)
                        
                        st.markdown("**Tu respuesta:**")
                        for concepto, definicion in respuesta_user.items():
                            es_correcto = respuesta_correcta.get(concepto) == definicion
                            if es_correcto:
                                st.success(f"✓ {concepto}  →  {definicion}")
                                pares_correctos += 1
                            else:
                                st.error(f"✗ {concepto}  →  {definicion}")
                                st.info(f"**Corrección:** {concepto}  →  {respuesta_correcta.get(concepto, 'N/A')}")
                        
                        for concepto in respuesta_correcta:
                            if concepto not in respuesta_user:
                                st.warning(f"Sin responder: {concepto}  →  {respuesta_correcta[concepto]}")
                        
                        puntos_pregunta = pares_correctos
                        total_pregunta = total_pares
                        puntos_obtenidos += puntos_pregunta
                        total_puntos += total_pregunta
                        
                        st.metric("Pares Correctos", f"{pares_correctos} / {total_pares}")
                    else:
                        st.warning("Esta pregunta no fue completada")
                        total_puntos += len(respuesta_correcta) if isinstance(respuesta_correcta, dict) else 1
                
                else:
                    total_puntos += 1
                    
                    if respuesta_user is None:
                        st.warning("No respondiste esta pregunta")
                        st.info(f"**Respuesta correcta:** {respuesta_correcta}")
                    else:
                        # --- CORRECCIÓN RESPUESTA CORTA (USANDO SIMILITUD) ---
                        if pregunta['tipo'] == 'respuesta_corta':
                            similitud = difflib.SequenceMatcher(None, str(respuesta_user).lower().strip(), str(respuesta_correcta).lower().strip()).ratio()
                            
                            if similitud >= 0.85:
                                st.success(f"**Correcto** • Tu respuesta: {respuesta_user}")
                                puntos_obtenidos += 1
                                aciertos += 1
                            elif similitud >= 0.5:
                                st.warning(f"**Casi Correcto** (Similitud: {int(similitud*100)}%) • Tu respuesta: {respuesta_user}")
                                st.info(f"**La respuesta exacta era:** {respuesta_correcta}")
                                puntos_obtenidos += 0.5
                            else:
                                st.error(f"**Incorrecto** • Tu respuesta: {respuesta_user}")
                                st.info(f"**Respuesta correcta:** {respuesta_correcta}")
                        
                        # --- CORRECCIÓN MULTIPLE CHOICE Y VERDADERO/FALSO ---
                        else:
                            # Comparación directa exacta
                            if respuesta_user == respuesta_correcta:
                                st.success(f"**Correcto** • Tu respuesta: {respuesta_user}")
                                puntos_obtenidos += 1
                                aciertos += 1
                            else:
                                st.error(f"**Incorrecto** • Tu respuesta: {respuesta_user}")
                                st.info(f"**Respuesta correcta:** {respuesta_correcta}")
                if pregunta.get('explicacion'):
                    with st.expander("Ver explicación detallada"):
                        st.write(pregunta['explicacion'])
                
                st.markdown("---")
        
        if total_puntos > 0:
            nota = (puntos_obtenidos / total_puntos) * 10
        else:
            nota = 0
        
        st.markdown("### Calificación Final")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if nota >= 6:
                st.markdown(f"""
                <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
                            border-radius: 16px; border: 2px solid #10b981;'>
                    <h1 style='font-size: 4rem; margin: 0; color: #10b981;'>{nota:.1f}</h1>
                    <p style='font-size: 1.5rem; margin: 0.5rem 0 0 0; color: #059669;'>de 10</p>
                    <p style='margin-top: 1rem; color: #047857; font-weight: 600;'>¡Excelente trabajo!</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            elif nota >= 5:
                st.markdown(f"""
                <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.05) 100%);
                            border-radius: 16px; border: 2px solid #f59e0b;'>
                    <h1 style='font-size: 4rem; margin: 0; color: #f59e0b;'>{nota:.1f}</h1>
                    <p style='font-size: 1.5rem; margin: 0.5rem 0 0 0; color: #d97706;'>de 10</p>
                    <p style='margin-top: 1rem; color: #b45309; font-weight: 600;'>Buen intento</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
                            border-radius: 16px; border: 2px solid #ef4444;'>
                    <h1 style='font-size: 4rem; margin: 0; color: #ef4444;'>{nota:.1f}</h1>
                    <p style='font-size: 1.5rem; margin: 0.5rem 0 0 0; color: #dc2626;'>de 10</p>
                    <p style='margin-top: 1rem; color: #b91c1c; font-weight: 600;'>Sigue practicando</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.caption(f"Puntos obtenidos: {puntos_obtenidos} de {total_puntos}")
        
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 3, 2])
        with col2:
            if st.button("Intentar de Nuevo", use_container_width=True, type="primary"):
                st.session_state.corregido = False
                st.session_state.respuestas_usuario = {}
                st.session_state.matching_pairs = {}
                st.session_state.matching_selected_left = {}
                st.rerun()

else:
    st.markdown("""
    <div style='text-align: center; padding: 3rem 1rem; background: white; border-radius: 16px; 
                border: 2px solid var(--neutral-200); margin: 2rem 0;'>
        <h2 style='color: var(--neutral-800); margin-bottom: 1rem;'>Bienvenido a ExamGen AI</h2>
        <p style='font-size: 1.1rem; color: var(--neutral-600); max-width: 600px; margin: 0 auto;'>
            Sube un archivo PDF desde la barra lateral para comenzar a generar tu examen personalizado
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Cómo funciona ExamGen AI"):
        st.markdown("""
        ### Proceso Simple en 4 Pasos
        
        1. **Carga tu Material** 📄  
           Sube un archivo PDF con tus apuntes, libro de texto o material de estudio
        
        2. **Generación Inteligente** 🤖  
           Nuestra IA analiza el contenido y genera preguntas relevantes automáticamente
        
        3. **Completa el Examen** ✏️  
           Responde todas las preguntas a tu propio ritmo
        
        4. **Recibe Feedback** 📊  
           Obtén tu calificación instantánea con explicaciones detalladas
        
        ---
        
        ### Tipos de Preguntas Soportadas
        
        - **Opción Múltiple** • Selecciona la respuesta correcta entre varias opciones
        - **Verdadero/Falso** • Determina la veracidad de una afirmación
        - **Respuesta Corta** • Escribe tu respuesta con tus propias palabras
        - **Asociación** • Empareja conceptos con sus definiciones correspondientes
        """)
