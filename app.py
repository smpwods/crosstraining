import streamlit as st
import pandas as pd
import gspread

# 1. Configuración
st.set_page_config(page_title="CrossTraining", layout="wide")
st.title("🏋️ Mi Programación")

# 2. Conexión directa (Sin usar st.connection que es lo que falla)
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
gc = gspread.public_api() # Esto permite leer hojas públicas
sh = gc.open_by_url(url)
worksheet = sh.get_worksheet(0)

# Intentamos leer
try:
    data = pd.DataFrame(worksheet.get_all_records())
except Exception:
    data = pd.DataFrame()

# 3. Formulario
st.sidebar.header("Nueva Sesión")
usuario = st.sidebar.text_input("Atleta", value="Sandra")
fecha = st.sidebar.date_input("Fecha")
indice = st.sidebar.text_input("Ejercicio")
warmup = st.sidebar.text_area("Warm-up")
fuerza = st.sidebar.text_area("Fuerza")
metcon = st.sidebar.text_area("WOD")
acc = st.sidebar.text_area("Accesorios")

# El botón de guardar ahora usará un enlace de formulario o aviso
if st.sidebar.button("Guardar en mi Diario"):
    st.sidebar.warning("Para escribir en el Excel de forma pública, Google requiere un paso extra. ¿Has pensado en usar un Google Form para esta parte? Es 100% fiable.")
    # Nota: gspread public solo permite lectura. 
    # Para escritura REAL sin errores, lo más rápido para ti ahora es:
    st.sidebar.markdown(f"[👉 Pincha aquí para abrir tu Excel y anotar el WOD]({url})")

# 4. Tabla central
st.divider()
if not data.empty:
    st.dataframe(data.sort_index(ascending=False), use_container_width=True)
else:
    st.info("Conectado al Excel. Introduce datos directamente en la hoja para verlos aquí.")
