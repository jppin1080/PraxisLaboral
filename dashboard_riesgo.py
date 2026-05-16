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

# 2. CSS EXTREMO PARA TEMA CLARO, KPIS, FILTROS Y BOTÓN CORPORATIVO
# Colores: 2D445D (Azul), A5D0B4 (Verde Praxis), A6764E (Marrón), EFEFF1 (Gris Claro), FFFFFF (Blanco)
st.markdown("""
    <style>
    /* Forzar fondo claro general */
    [data-testid="stAppViewContainer"], .stApp { background-color: #EFEFF1 !important; }
    [data-testid="stHeader"] { background-color: transparent !important; }
    p, span, div { color: #2D445D; }
    h1, h2, h3 { color: #2D445D !important; font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: bold; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 2px solid #2D445D !important; }
    
    /* Diseño de las Cajas KPI */
    [data-testid="stMetric"] { background-color: #FFFFFF !important; padding: 15px 20px !important; border-radius: 8px !important; box-shadow: 0 4px 10px rgba(0,0,0,0.08) !important; border-top: 5px solid #2D445D !important; }
    div[data-testid="stMetricLabel"] > div, div[data-testid="stMetricLabel"] p { color: #A6764E !important; font-size: 1.2rem !important; font-weight: 800 !important; letter-spacing: 0.5px !important; opacity: 1 !important; }
    div[data-testid="stMetricValue"] > div { color: #2D445D !important; font-size: 1.6rem !important; font-weight: 700 !important; }

    /* FORZAR COLORES CLAROS EN LOS MENÚS DESPLEGABLES (SELECTBOX) */
    div[data-baseweb="select"] > div { background-color: #FFFFFF !important; color: #2D445D !important; border: 1px solid #A5D0B4 !important; }
    div[data-baseweb="select"] span { color: #2D445D !important; }
    ul[data-baseweb="menu"] { background-color: #FFFFFF !important; }
    li[data-baseweb="menu-item"] { color: #2D445D !important; background-color: transparent !important; }
    li[data-baseweb="menu-item"]:hover { background-color: #EFEFF1 !important; }

    /* DISEÑO DEL BOTÓN DE DESCARGA: Verde Praxis Laboral */
    .stDownloadButton > button {
        background-color: #A5D0B4 !important; /* Verde Praxis */
        color: #FFFFFF !important; /* Letras Blancas */
        border: 2px solid #2D445D !important; /* Borde Azul Corporativo */
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: background-color 0.3s ease, color 0.3s ease; /* Efecto suave */
    }
    
    /* Efecto al pasar el mouse por encima (hover) */
    .stDownloadButton > button:hover {
        background-color: #FFFFFF !important; /* Fondo Blanco */
        color: #2D445D !important; /* Letras Azules Corporativas */
        border: 2px solid #A5D0B4 !important; /* Borde Verde Praxis */
    }
    </style>
""", unsafe_allow_html=True)

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
        marginacion_censo = np.random.choice([85, 55, 25], p=[0.3, 0.4, 0.3]) 
        desercion_escolar = np.random.uniform(5, 25) 
        jornada_abusiva_enoe = np.random.choice([1, 0], p=[0.35, 0.65]) 
        intermediario_enganche = np.random.choice([1, 0], p=[0.3, 0.7]) 
        retencion_docs_salario = np.random.choice([1, 0], p=[0.15, 0.85]) 
        alerta_usdol = 85 if sector in ['Agricultura y Agroindustria', 'Minería y Extracción', 'Manufactura Textil/Maquila'] else 30
        score_infantil_base = (alerta_usdol * 0.35 + marginacion_censo * 0.25 + (desercion_escolar * 4) * 0.25 + (75 if tamano in ['Micro', 'Pequeña'] else 30) * 0.15)
        score_eslabon = 90 if 'Tier 3' in eslabon else (70 if 'Tier 2' in eslabon else 40)
        coercion_oit = min((intermediario_enganche * 50) + (retencion_docs_salario * 50), 100) if ((intermediario_enganche * 50) + (retencion_docs_salario * 50)) > 0 else 20
        score_forzoso_base = (alerta_usdol * 0.25 + score_eslabon * 0.30 + coercion_oit * 0.30 + (85 if jornada_abusiva_enoe == 1 else 35) * 0.15)
        ruido = np.random.normal(0, 3)
        data.append({
            'ID_Proveedor': f"PRV-{i+1:04d}", 'Entidad_Federativa': estado, 'Sector_Industrial': sector, 'Eslabon_Cadena': eslabon, 'Tamano_Empresa': tamano,
            'Censo_Marginacion': marginacion_censo, 'Censo_Desercion': round(desercion_escolar, 1),
            'ENOE_Jornada_Abusiva': 'Sí' if jornada_abusiva_enoe == 1 else 'No', 'OIT_Enganche': 'Sí' if intermediario_enganche == 1 else 'No',
            'USDOL_Alerta': 'Sí' if alerta_usdol == 85 else 'No', 'Score_TI_Base': score_infantil_base, 'Score_TF_Base': score_forzoso_base,
            'Score_Trabajo_Infantil_Final': round(max(0, min(100, score_infantil_base + ruido)), 1), 'Score_Trabajo_Forzoso_Final': round(max(0, min(100, score_forzoso_base + ruido)), 1)
        })
    return pd.DataFrame(data)

df_raw = generar_dataset_avanzado_mexico()

# 4. ENCABEZADO PRINCIPAL
st.title("⚖️ PRAXIS LABORAL: Matriz de Diagnóstico y Análisis Operativo")
st.subheader("Evaluación Multidimensional de Riesgos de Derechos Humanos en Cadenas de Suministro")
st.markdown("---")

# 5. BARRA LATERAL (TÍTULOS REPLANTEADOS A TONO CONSULTOR)
st.sidebar.markdown("### 🎯 Dimensión de Derechos Humanos")
tema_seleccionado = st.sidebar.radio("Selecciona el fenómeno a evaluar:", ("Trabajo Infantil (Eje MIRTI / ENTI / Censo)", "Trabajo Forzoso (Eje OIT / Walk Free / ENOE)"))
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Estructura de la Cadena de Valor")

def agregar_todos(lista):
    res = ['Todos']
    res.extend(sorted(lista))
    return res

f_estado = st.sidebar.selectbox("Entidad Federativa", agregar_todos(df_raw['Entidad_Federativa'].unique()))
f_sector = st.sidebar.selectbox("Sector Industrial (SCIAN)", agregar_todos(df_raw['Sector_Industrial'].unique()))
f_eslabon = st.sidebar.selectbox("Eslabón de la Cadena (Tiers)", agregar_todos(df_raw['Eslabon_Cadena'].unique()))
f_tamano = st.sidebar.selectbox("Tamaño de la Unidad", agregar_todos(df_raw['Tamano_Empresa'].unique()))

df_filtrado = df_raw.copy()
if f_estado != 'Todos': df_filtrado = df_filtrado[df_filtrado['Entidad_Federativa'] == f_estado]
if f_sector != 'Todos': df_filtrado = df_filtrado[df_filtrado['Sector_Industrial'] == f_sector]
if f_eslabon != 'Todos': df_filtrado = df_filtrado[df_filtrado['Eslabon_Cadena'] == f_eslabon]
if f_tamano != 'Todos': df_filtrado = df_filtrado[df_filtrado['Tamano_Empresa'] == f_tamano]

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Calibración del Motor Estadístico")

if tema_seleccionado == "Trabajo Infantil (Eje MIRTI / ENTI / Censo)":
    w_usdol = st.sidebar.slider("Peso Alertas USDOL ILAB", 0.1, 1.0, 0.35)
    w_censo = st.sidebar.slider("Peso Indicadores Censo", 0.1, 1.0, 0.50)
    w_mirti = st.sidebar.slider("Peso Estructura (Tamaño/ENOE)", 0.1, 1.0, 0.15)
    suma = w_usdol + w_censo + w_mirti
    df_filtrado['Riesgo_Compuesto_Calculado'] = ((df_filtrado['USDOL_Alerta'].map({'Sí': 85, 'No': 30}) * (w_usdol/suma)) + (df_filtrado['Censo_Marginacion'] * (w_censo/suma)) + (df_filtrado['Score_TI_Base'] * (w_mirti/suma))).round(1)
else:
    w_usdol = st.sidebar.slider("Peso Criterios USDOL", 0.1, 1.0, 0.25)
    w_tier = st.sidebar.slider("Peso Eslabón (Tiers)", 0.1, 1.0, 0.30)
    w_oit = st.sidebar.slider("Peso Coerción (OIT/Walk Free)", 0.1, 1.0, 0.45)
    suma = w_usdol + w_tier + w_oit
    df_filtrado['Riesgo_Compuesto_Calculado'] = ((df_filtrado['USDOL_Alerta'].map({'Sí': 85, 'No': 30}) * (w_usdol/suma)) + (df_filtrado['Score_TF_Base'] * ((w_tier + w_oit)/suma))).round(1)

df_filtrado['Nivel_Riesgo'] = df_filtrado['Riesgo_Compuesto_Calculado'].apply(lambda x: '🔴 Crítico' if x >= 70 else ('🟡 Medio' if x >= 40 else '🟢 Bajo'))

# 6. KPIS PRINCIPALES
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric(label="Muestra Analizada", value=f"{len(df_filtrado):,}")
with c2: st.metric(label="Riesgo Promedio", value=f"{df_filtrado['Riesgo_Compuesto_Calculado'].mean():.1f} pts")
with c3: