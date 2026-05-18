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

# 2. INYECCIÓN CRÍTICA DE VARIABLES GLOBALES (Forzar Tema Claro Corporativo)
# Colores: 2D445D (Azul), A5D0B4 (Verde Praxis), A6764E (Marrón), EFEFF1 (Gris Claro)
st.markdown("""
    <style>
    /* HACK DE VARIABLES DE RAÍZ: Obliga a tablas y dropdowns a volverse claros */
    html, body, [data-testid="stAppViewContainer"], :root {
        --primary-color: #A6764E !important;
        --background-color: #EFEFF1 !important;
        --secondary-background-color: #FFFFFF !important;
        --text-color: #2D445D !important;
    }
    
    /* Contenedor general */
    .stApp { background-color: #EFEFF1 !important; }
    [data-testid="stHeader"] { background-color: transparent !important; }
    p, span, div { color: #2D445D !important; }
    h1, h2, h3 { color: #2D445D !important; font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: bold; }
    
    /* Forzar Barra Lateral en Blanco */
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

    /* FORZAR MENÚS DESPLEGABLES EN BLANCO LUMINOSO */
    div[data-baseweb="select"] > div { background-color: #FFFFFF !important; color: #2D445D !important; border: 1px solid #A5D0B4 !important; }
    div[role="listbox"], ul[data-baseweb="menu"] { background-color: #FFFFFF !important; }
    div[role="option"], li[data-baseweb="menu-item"] { color: #2D445D !important; background-color: #FFFFFF !important; }
    div[role="option"]:hover, li[data-baseweb="menu-item"]:hover { background-color: #EFEFF1 !important; }

    /* BOTÓN DE DESCARGA VERDE PRAXIS */
    .stDownloadButton > button {
        background-color: #A5D0B4 !important;
        color: #FFFFFF !important;
        border: 2px solid #2D445D !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    .stDownloadButton > button:hover {
        background-color: #FFFFFF !important;
        color: #2D445D !important;
        border: 2px solid #A5D0B4 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Paleta Estricta Praxis para mapeos discretos
palette_map_praxis = {
    'Critico': '#2D445D', 
    'Medio': '#A6764E',   
    'Bajo': '#A5D0B4'    
}

# 3. MOTOR DE GENERACIÓN DE DATOS
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

# 4. ENCABEZADO
st.title("⚖️ PRAXIS LABORAL: Matriz de Diagnóstico y Análisis Operativo")
st.subheader("Evaluación Multidimensional de Riesgos de Derechos Humanos en Cadenas de Suministro")
st.markdown("---")

# 5. BARRA LATERAL (TÍTULOS REPLANTEADOS)
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

# Clasificación limpia sin emojis de semáforo
def clasificar_espectro_completo(score):
    if score >= 70: return 'Critico'
    elif score >= 40: return 'Medio'
    else: return 'Bajo'

df_filtrado['Nivel_Riesgo'] = df_filtrado['Riesgo_Compuesto_Calculado'].apply(clasificar_espectro_completo)

# 6. KPIS PRINCIPALES
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric(label="Muestra Analizada", value=f"{len(df_filtrado):,}")
with c2: st.metric(label="Riesgo Promedio", value=f"{df_filtrado['Riesgo_Compuesto_Calculado'].mean():.1f} pts")
with c3: 
    pct_medios = (len(df_filtrado[df_filtrado['Nivel_Riesgo'] == 'Medio']) / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0
    st.metric(label="Proporción Medio", value=f"{pct_medios:.1f}%")
with c4: 
    pct_criticos = (len(df_filtrado[df_filtrado['Nivel_Riesgo'] == 'Critico']) / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0
    st.metric(label="Proporción Crítico", value=f"{pct_criticos:.1f}%")

st.markdown("### 📊 Mapeo Estratégico y Correlación de Factores")

# 7. GRÁFICOS INTERACTIVOS (CON ESCALA EXCLUSIVA DE PRAXIS LABORAL)
col_g1, col_g2 = st.columns(2)
custom_continuous_praxis = ["#A5D0B4", "#A6764E", "#2D445D"] # Verde -> Marrón -> Azul Marino

with col_g1:
    if f_estado == 'Todos':
        st.markdown("**Riesgo Estructural Promedio por Entidad Federativa (Nacional)**")
        df_plot = df_filtrado.groupby('Entidad_Federativa')['Riesgo_Compuesto_Calculado'].mean().reset_index().sort_values(by='Riesgo_Compuesto_Calculado', ascending=False)
        y_column = 'Entidad_Federativa'
        y_title = 'Estado'
    else:
        st.markdown(f"**Desglose de Riesgo por Sector Industrial en {f_estado}**")
        df_plot = df_filtrado.groupby('Sector_Industrial')['Riesgo_Compuesto_Calculado'].mean().reset_index().sort_values(by='Riesgo_Compuesto_Calculado', ascending=False)
        y_column = 'Sector_Industrial'
        y_title = 'Sector Industrial'

    # Escala continua usando estrictamente la paleta Praxis (Cero semáforo original)
    fig_bar = px.bar(
        df_plot, x='Riesgo_Compuesto_Calculado', y=y_column, orientation='h',
        color='Riesgo_Compuesto_Calculado',
        color_continuous_scale=custom_continuous_praxis, 
        labels={'Riesgo_Compuesto_Calculado': 'Puntaje Promedio', y_column: y_title}
    )
    fig_bar.update_layout(height=700, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#2D445D'))
    fig_bar.update_xaxes(tickfont=dict(color='#2D445D'), title_font=dict(color='#2D445D'), showgrid=True, gridcolor='rgba(45,68,93,0.1)')
    fig_bar.update_yaxes(tickfont=dict(color='#2D445D'), title_font=dict(color='#2D445D'))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_g2:
    st.markdown("**Matriz Analítica Integral (Intersección de Riesgos Específicos)**")
    fig_scat = px.scatter(
        df_filtrado, x='Score_Trabajo_Infantil_Final', y='Score_Trabajo_Forzoso_Final', 
        color='Nivel_Riesgo', size='Riesgo_Compuesto_Calculado', 
        color_discrete_map=palette_map_praxis, 
        hover_data=['ID_Proveedor', 'Sector_Industrial', 'Eslabon_Cadena', 'USDOL_Alerta'], 
        labels={'Score_Trabajo_Infantil_Final': 'Riesgo Trabajo Infantil', 'Score_Trabajo_Forzoso_Final': 'Riesgo Trabajo Forzoso', 'Nivel_Riesgo': 'Nivel de Riesgo'}
    )
    fig_scat.update_layout(height=700, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#2D445D'))
    fig_scat.update_xaxes(tickfont=dict(color='#2D445D'), title_font=dict(color='#2D445D'), showgrid=True, gridcolor='rgba(45,68,93,0.1)')
    fig_scat.update_yaxes(tickfont=dict(color='#2D445D'), title_font=dict(color='#2D445D'), showgrid=True, gridcolor='rgba(45,68,93,0.1)')
    st.plotly_chart(fig_scat, use_container_width=True)

# 8. TABLA DE DIAGNÓSTICO
st.markdown("### 📋 Resultados Holísticos del Diagnóstico de Suministro")
df_lista = df_filtrado.sort_values(by='Riesgo_Compuesto_Calculado', ascending=False).copy()

def pauta_debida_diligencia_avanzada(row):
    if 'Critico' in row['Nivel_Riesgo']: return "ALERTA PRIORITARIA: Auditoría física urgente en sitio." if "Infantil" not in tema_seleccionado else "ALERTA MIRTI: Riesgo de deserción escolar. Verificación de actas."
    return "Monitoreo Preventivo: Solicitar reportes de nóminas." if 'Medio' in row['Nivel_Riesgo'] else "Cumplimiento Estándar: Actualización bianual."

df_lista['Recomendación Praxis Laboral'] = df_lista.apply(pauta_debida_diligencia_avanzada, axis=1)
df_vista = df_lista[['ID_Proveedor', 'Entidad_Federativa', 'Sector_Industrial', 'Eslabon_Cadena', 'Riesgo_Compuesto_Calculado', 'Nivel_Riesgo', 'Recomendación Praxis Laboral']]

st.dataframe(df_vista, hide_index=True, use_container_width=True)

# BOTÓN DE DESCARGA
csv_buffer = df_vista.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 Descargar Reporte de Hallazgos Filtrados (Excel / CSV)",
    data=csv_buffer,
    file_name="reporte_debida_diligencia_praxis.csv",
    mime="text/csv"
)

# 9. DOCUMENTACIÓN
st.markdown("---")
st.markdown("## 📚 Documentación Metodológica y Desagregación de Puntajes")
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.markdown("### 🛡️ Marco Conceptual Compartido (USDOL ILAB)\nAmbos modelos integran como variable transversal la **Lista de Bienes Producidos con Trabajo Infantil o Forzoso (USDOL)**. Si el sector coincide, se inyecta un riesgo base de 85 puntos.\n\n### ⛓️ Desagregación por Eslabón (Tiers)\nPenaliza la opacidad corporativa:\n* **Tier 3 (Materia Prima):** Suma **90 puntos base** (aislamiento geográfico).\n* **Tier 2 (Procesamiento/Maquila):** Asigna **70 puntos base**.\n* **Tier 1 (Ensamble Final):** Reduce a **40 puntos base**.")
with col_m2:
    if "Trabajo Infantil" in tema_seleccionado:
        st.markdown("### 📊 Puntaje de Trabajo Infantil (MIRTI + Censo)\n1. **Alerta Sectorial USDOL (35%):** Presente en lista ILAB = **85 pts**.\n2. **Marginación del Entorno - Censo (25%):** Rezago Alto = **85 pts**, Medio = **55 pts**, Bajo = **25 pts**.\n3. **Deserción Escolar - Censo (25%):** Tasa real multiplicada por 4.\n4. **Vulnerabilidad Operativa - ENOE (15%):** Micro empresas a destajo = **75 pts**.")
    else:
        st.markdown("### ⛓️ Puntaje de Trabajo Forzoso (OIT / Walk Free / ENOE)\n1. **Indicador de Coerción OIT (30%):** Intermediarios = **+50 pts**. Retención salarios/documentos = **+50 pts**.\n2. **Opacidad del Eslabón (30%):** Tier 3 = **90 pts**, Tier 2 = **70 pts**.\n3. **Alertas Comerciales USDOL (25%):** Sectores penalizados T-MEC = **85 pts base**.\n4. **Jornada Abusiva - ENOE (15%):** Predominio de jornadas >48 horas = **85 pts**.")