import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Praxis Laboral - Diagnóstico Avanzado de Riesgo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INYECCIÓN ABSOLUTA DE CSS (Forzar Tema Claro en Inputs, Dropdowns y Componentes)
st.markdown("""
    <style>
    /* Forzar fondo claro general e inyectar variables de la paleta */
    html, body, [data-testid="stAppViewContainer"], .stApp, :root {
        background-color: #EFEFF1 !important;
        --primary-color: #A6764E !important;
        --background-color: #EFEFF1 !important;
        --secondary-background-color: #FFFFFF !important;
        --text-color: #2D445D !important;
    }
    
    [data-testid="stHeader"] { background-color: transparent !important; }
    p, span, div, label { color: #2D445D !important; }
    h1, h2, h3 { color: #2D445D !important; font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: bold; }
    
    /* Barra Lateral */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important; 
        border-right: 2px solid #2D445D !important; 
    }

    /* Rediseño Completo de Cajas KPI */
    [data-testid="stMetric"] { 
        background-color: #FFFFFF !important; 
        padding: 15px 20px !important; 
        border-radius: 8px !important; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.08) !important; 
        border-top: 5px solid #2D445D !important; 
    }
    div[data-testid="stMetricLabel"] > div, div[data-testid="stMetricLabel"] p { 
        color: #A6764E !important; 
        font-size: 1.2rem !important; 
        font-weight: 800 !important; 
        letter-spacing: 0.5px !important; 
    }
    div[data-testid="stMetricValue"] > div { 
        color: #2D445D !important; 
        font-size: 1.6rem !important; 
        font-weight: 700 !important; 
    }

    /* HACK PARA DROPDOWNS Y MENÚS SELECTORES: Contraste total */
    div[data-baseweb="select"] > div { 
        background-color: #FFFFFF !important; 
        color: #2D445D !important; 
        border: 1px solid #A5D0B4 !important; 
    }
    div[data-baseweb="select"] * { color: #2D445D !important; }
    
    /* Forzar los contenedores flotantes de las opciones */
    div[data-baseweb="popover"] *, div[role="listbox"] *, ul[data-baseweb="menu"] *, div[role="option"] {
        background-color: #FFFFFF !important;
        color: #2D445D !important;
    }
    div[role="option"]:hover, li[data-baseweb="menu-item"]:hover { 
        background-color: #EFEFF1 !important; 
    }

    /* ESTILOS DE LA TABLA HTML CORPORATIVA DE PRAXIS */
    .praxis-table-container {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    table.praxis-table {
        width: 100%;
        border-collapse: collapse;
        color: #2D445D;
        font-family: Arial, sans-serif;
        font-size: 14px;
    }
    table.praxis-table th {
        background-color: #2D445D;
        color: #FFFFFF !important;
        font-weight: bold;
        text-align: left;
        padding: 12px;
        border-bottom: 3px solid #A6764E;
    }
    table.praxis-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #EFEFF1;
        background-color: #FFFFFF;
    }
    table.praxis-table tr:hover td {
        background-color: #F9F9FB;
    }

    /* BOTÓN DE DESCARGA VERDE PRAXIS */
    .stDownloadButton > button {
        background-color: #A5D0B4 !important;
        color: #FFFFFF !important;
        border: 2px solid #2D445D !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease;
    }
    .stDownloadButton > button:hover {
        background-color: #FFFFFF !important;
        color: #2D445D !important;
        border: 2px solid #A5D0B4 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Paleta Estricta Praxis para mapeos de gráficos
palette_map_praxis = {
    'Critico': '#2D445D', 
    'Medio': '#A6764E',   
    'Bajo': '#A5D0B4'    
}

# 3. MOTOR DE GENERACIÓN DE DATOS SIMULADOS
@st.cache_data
def generar_dataset_avanzado_mexico():
    np.random.seed(2026)
    n_registros = 2000
    estados = ['Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 'Chiapas', 'Chihuahua', 'Ciudad de México', 'Coahuila', 'Colima', 'Durango', 'Estado de México', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán', 'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán', 'Zacatecas']
    sectores = ['Agricultura y Agroindustria', 'Minería y Extracción', 'Manufactura Textil/Maquila', 'Construcción', 'Comercio Mayorista', 'Servicios Domésticos y Hotelería']
    eslabones = ['Tier 3 - Materia Prima', 'Tier 2 - Procesamiento/Maquila', 'Tier 1 - Ensamblaje Final', 'Logística y Distribución']
    tamanos = ['Micro', 'Pequeña', 'Mediana', 'Grande']
    data = []
    for i in range(n_registros):
        estado = np.random.choice(estados)
        sector = np.random.choice(sectores)
        eslabon = np.random.choice(eslabones)
        tamano = np.random.choice(tamanos)
        marginacion_censo = np.random.