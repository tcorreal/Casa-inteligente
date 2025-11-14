# app.py
# Aplicación Streamlit para "Casa inteligente multimodal"
# - Interfaz gráfica
# - Control por texto
# - Control por gestos usando modelo de Teachable Machine

import streamlit as st
from typing import Optional
import re
import numpy as np
from PIL import Image, ImageOps

# Import de TensorFlow se hace cuando se carga el modelo TM para no romper la app si falta
# El decorador @st.cache_resource cachingará el objeto del modelo entre reruns.
# (Streamlit >= 1.18)
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except Exception:
    TF_AVAILABLE = False

st.set_page_config(page_title="Casa inteligente multimodal", layout="wide")

# -----------------------
# Inicializar session_state
# -----------------------
def init_state():
    if "sala" not in st.session_state:
        st.session_state["sala"] = {
            "luz": False,        # True = encendida
            "brillo": 50,        # 0-100
            "ventilador": 0,     # 0-3
            "puerta": False,     # False = cerrada, True = abierta
            "presencia": False,  # Sensor simulado
        }
    if "habitacion" not in st.session_state:
        st.session_state["habitacion"] = {
            "luz": False,
            "brillo": 50,
            "ventilador": 0,
            "puerta": False,
            "presencia": False,
        }
    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "Panel general"

init_state()

# -----------------------
# Función para cargar modelo TM (gestos)
# -----------------------
@st.cache_resource
def load_tm_model():
    """
    Carga el modelo de Teachable Machine desde tm_model/gestos.h5.
    Devuelve el modelo o None si no pudo cargarse.
    """
    if not TF_AVAILABLE:
        # No queremos fallar si tensorflow no está importable
        return None
    try:
        model = tf.keras.models.load_model("tm_model/gestos.h5", compile=False)
        return model
    except Exception as e:
        # Registramos en sesión para poder mostrar el error sin romper la app
        st.session_state["_tm_load_error"] = str(e)
        return None

# Lista fija de clases esperadas por el modelo
TM_CLASSES = ["luz_on", "luz_off", "ventilador_on", "ventilador_off"]

# -----------------------
# Utilidades
# -----------------------
def seleccionar_ambiente_mejor(comando: str) -> Optional[str]:
    """Detecta si el comando menciona 'sala' o 'habitacion'. Devuelve 'sala'|'habitacion'|None"""
    texto = comando.lower()
    if "sala" in texto o...