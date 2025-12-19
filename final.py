
import streamlit as st
import random
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------
st.set_page_config(
    page_title="Calidad del Agua - Monitoreo",
    page_icon="💧",
    layout="wide"
)

# -----------------------------
# FUNCIÓN: generar muestras
# -----------------------------
def generar_muestras(n=10):
    datos = {'Fecha': [], 'pH': [], 'Turbidez': [], 'DQO': []}
    for i in range(n):
        fecha = datetime.date.today() - datetime.timedelta(days=i)
        ph = round(random.uniform(5.5, 9.5), 2)
        turbidez = round(random.uniform(1, 15), 2)
        dqo = round(random.uniform(30, 300), 2)
        datos['Fecha'].append(fecha)
        datos['pH'].append(ph)
        datos['Turbidez'].append(turbidez)
        datos['DQO'].append(dqo)
    return pd.DataFrame(datos)

# -----------------------------
# TÍTULO PRINCIPAL
# -----------------------------
st.title("💧 Monitoreo de Calidad del Agua")
st.markdown(
    """
    Aplicación interactiva para **simular y analizar parámetros de calidad del agua**, 
    comparándolos con **ECA y LMP ambientales**.
    """
)

# -----------------------------
# BARRA LATERAL
# -----------------------------
st.sidebar.header("⚙️ Configuración")

n_muestras = st.sidebar.slider(
    "Número de muestras",
    min_value=5,
    max_value=30,
    value=10
)

generar = st.sidebar.button("🔄 Generar muestras")

# -----------------------------
# GENERAR DATOS
# -----------------------------
if generar or "df" not in st.session_state:
    st.session_state.df = generar_muestras(n_muestras)

df = st.session_state.df

# -----------------------------
# MÉTRICAS CLAVE
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("pH promedio", f"{df['pH'].mean():.2f}")
col2.metric("Turbidez promedio (NTU)", f"{df['Turbidez'].mean():.2f}")
col3.metric("DQO promedio (mg/L)", f"{df['DQO'].mean():.2f}")

# -----------------------------
# TABLA DE DATOS
# -----------------------------
st.subheader("📋 Datos simulados")
st.dataframe(df, use_container_width=True)

# -----------------------------
# GRÁFICOS
# -----------------------------
st.subheader("📈 Análisis gráfico")

col_g1, col_g2 = st.columns(2)

# ---- Gráfico pH y Turbidez
with col_g1:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(df['Fecha'], df['pH'], marker='o', label='pH')
    ax.plot(df['Fecha'], df['Turbidez'], marker='s', label='Turbidez')

    # Límites
    ax.axhline(6.5, linestyle='--', color='gray', label='LMP pH mín')
    ax.axhline(8.5, linestyle='--', color='gray', label='LMP pH máx')
    ax.axhline(5, linestyle='--', color='red', label='ECA Turbidez')

    ax.set_title("pH y Turbidez")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Valor")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ---- Gráfico DQO
with col_g2:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(df['Fecha'], df['DQO'], marker='^', color='purple', label='DQO')

    ax.axhline(200, linestyle='--', color='black', label='LMP DQO')

    ax.set_title("Demanda Química de Oxígeno (DQO)")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("mg/L")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# -----------------------------
# INTERPRETACIÓN
# -----------------------------
st.subheader("🧠 Interpretación rápida")

if df['DQO'].mean() > 200:
    st.error("⚠️ La DQO promedio supera el LMP → posible contaminación orgánica.")
else:
    st.success("✅ La DQO promedio cumple el LMP.")

if df['Turbidez'].mean() > 5:
    st.warning("⚠️ Turbidez elevada → tratamiento adicional requerido.")
else:
    st.success("✅ Turbidez dentro del ECA.")

st.caption("Proyecto educativo")
