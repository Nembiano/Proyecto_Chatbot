import streamlit as st
import os
from dotenv import load_dotenv
import time
from openai import OpenAI

# Cargar variables de entorno
load_dotenv()

# Configuración de OpenAI
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
client = OpenAI(api_key=api_key)

# CSS personalizado para un tema similar al de la imagen
css = """
<style>
    /* Fondo degradado azul oscuro */
    .stApp {
        background: linear-gradient(to bottom, #0a1745, #152a5a);
    }
    
    /* Estilo para el contenedor principal */
    .main-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Estilo para el encabezado */
    .header {
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Estilo para el logo */
    .logo {
        width: 120px;
        height: 120px;
        margin: 0 auto;
        background-color: white;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(73, 160, 255, 0.5);
    }
    
    /* Estilo para el título */
    .title {
        color: white;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    /* Estilo para la descripción */
    .description {
        color: #d0d8e8;
        font-size: 16px;
        margin-bottom: 25px;
        text-align: center;
    }
    
    /* Estilo para las tarjetas de preguntas */
    .question-card {
        background-color: rgba(20, 40, 90, 0.7);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        color: white;
        cursor: pointer;
        transition: all 0.3s;
        border-left: 3px solid #ff6b00;
        font-weight: 500;
    }
    
    .question-card:hover {
        background-color: rgba(30, 50, 100, 0.9);
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(255, 107, 0, 0.2);
    }
    
    /* Estilo para el bullet point en las tarjetas */
    .bullet {
        color: #ff6b00;
        font-weight: bold;
        margin-right: 5px;
    }
    
    /* Estilo para el área de chat */
    .chat-area {
        background-color: rgba(15, 30, 70, 0.4);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .chat-container {
        border-radius: 10px;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid rgba(73, 160, 255, 0.2);
        background-color: rgba(10, 25, 60, 0.6);
        padding: 15px;
        margin-bottom: 15px;
    }
    
    /* Estilos para los mensajes */
    .user-message {
        background-color: rgba(37, 99, 235, 0.3);
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 3px solid #4a72f5;
        position: relative;
        color: white;
    }
    
    .assistant-message {
        background-color: rgba(255, 107, 0, 0.2);
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 3px solid #ff6b00;
        position: relative;
        color: white;
    }
    
    /* Estilo para la barra de entrada de texto */
    .input-container {
        margin-top: 15px;
    }
    
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 1px solid rgba(73, 160, 255, 0.3) !important;
        background-color: rgba(10, 25, 60, 0.6) !important;
    }
    
    .stChatInputContainer textarea {
        color: white !important;
    }
    
    /* Animación de carga */
    @keyframes pulse {
        0% { opacity: 0.4; }
        50% { opacity: 1; }
        100% { opacity: 0.4; }
    }
    
    .loading-animation {
        display: flex;
        align-items: center;
        color: #ff6b00;
        font-weight: bold;
    }
    
    .loading-dot {
        width: 8px;
        height: 8px;
        margin: 0 3px;
        border-radius: 50%;
        background-color: #ff6b00;
        display: inline-block;
        animation: pulse 1.4s infinite ease-in-out;
    }
    
    .loading-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .loading-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    /* Estilo para el pie de página */
    .footer {
        text-align: center;
        color: #d0d8e8;
        font-size: 12px;
        margin-top: 30px;
        padding-top: 10px;
        border-top: 1px solid rgba(73, 160, 255, 0.2);
    }
    
    /* Esconder el header de streamlit */
    header {
        visibility: hidden;
    }
    
    /* Remover espacio extra y padding de Streamlit */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    .stButton button {
        display: none;
    }
    
    /* Eliminar espacio sobrante */
    .st-emotion-cache-1544thi {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    .st-emotion-cache-1vbkxwb {
        gap: 0.5rem !important;
    }
</style>
"""

# Función para generar un ícono de ciberseguridad en SVG (estilo reloj)
def get_cyber_icon():
    return """
    <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="40" cy="40" r="38" fill="white"/>
        <circle cx="40" cy="40" r="35" stroke="#FF6B00" stroke-width="2"/>
        <path d="M40 15V40L48 48" stroke="#FF6B00" stroke-width="3"/>
        <circle cx="40" cy="40" r="3" fill="#FF6B00"/>
    </svg>
    """

# Animación de carga
def loading_animation():
    return """
    <div class="loading-animation">
        Procesando
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
    </div>
    """

# Configuración de la página
st.set_page_config(
    page_title="CyberSec Assistant",
    page_icon="🔒",
    layout="wide"
)

# Inyectar CSS personalizado
st.markdown(css, unsafe_allow_html=True)

# Inicialización de variables de sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    # Crear un thread nuevo
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

# Función para enviar mensaje
def send_message(prompt):
    if prompt:
        # Agregar mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Activar indicador de carga
        st.session_state.is_loading = True
        st.rerun()

# Contenedor principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Encabezado
st.markdown('<div class="header">', unsafe_allow_html=True)
st.markdown(f'<div class="logo">{get_cyber_icon()}</div>', unsafe_allow_html=True)
st.markdown('<div class="title">Bienvenido a CyberSec Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Consulta toda la información sobre legislación en ciberseguridad o escribe tu consulta.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Verificar si estamos en modo carga
if st.session_state.is_loading:
    # Procesamiento de la respuesta del asistente
    last_user_message = st.session_state.messages[-1]["content"]
    
    # Agregar mensaje al thread
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=last_user_message
    )
    
    # Crear una ejecución del asistente
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )
    
    # Mostrar el área de chat con los mensajes y la animación de carga
    st.markdown('<div class="chat-area">', unsafe_allow_html=True)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Mostrar mensajes previos
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Mostrar animación de carga
    st.markdown(loading_animation(), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Campo de entrada desactivado durante la carga
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.chat_input("Esperando respuesta...", disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Cierre del área de chat
    
    # Esperar a que el asistente complete la respuesta
    while run.status in ["queued", "in_progress"]:
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id
        )
    
    # Obtener la respuesta
    messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id
    )
    
    # Agregar mensaje del asistente al historial
    assistant_response = messages.data[0].content[0].text.value
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Desactivar el indicador de carga
    st.session_state.is_loading = False
    st.rerun()
else:
    # Mostrar interfaz normal
    if not st.session_state.messages:
        # Mostrar solo las 2 preguntas específicas
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("""
            <div class="question-card" onclick="
            document.querySelector('.stChatInputContainer textarea').value = '¿De qué habla la ley marco en ciberseguridad?';
            document.querySelector('.stChatInputContainer textarea').dispatchEvent(new Event('input', { bubbles: true }));
            document.querySelector('.stChatInputContainer button').click();">
            <span class="bullet">•</span> ¿De qué habla la ley marco en ciberseguridad?
            </div>
            """, unsafe_allow_html=True)
        
        with col_right:
            st.markdown("""
            <div class="question-card" onclick="
            document.querySelector('.stChatInputContainer textarea').value = '¿De qué habla la ley de protección de datos?';
            document.querySelector('.stChatInputContainer textarea').dispatchEvent(new Event('input', { bubbles: true }));
            document.querySelector('.stChatInputContainer button').click();">
            <span class="bullet">•</span> ¿De qué habla la ley de protección de datos?
            </div>
            """, unsafe_allow_html=True)
    
    # Área de chat si hay mensajes
    if st.session_state.messages:
        st.markdown('<div class="chat-area">', unsafe_allow_html=True)
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        prompt = st.chat_input("Escribe tu mensaje aquí...")
        if prompt:
            send_message(prompt)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # Cierre del área de chat
    else:
        # Solo mostrar el campo de entrada para usuarios nuevos
        prompt = st.chat_input("Escribe tu mensaje aquí...")
        if prompt:
            send_message(prompt)

# Pie de página
st.markdown('<div class="footer">Desarrollado por CyberSec Team</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Cierre del contenedor principal 