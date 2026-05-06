import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración
st.set_page_config(page_title="CrossTraining", layout="wide")
st.title("🏋️ Mi Programación")

# 2. Conexión simplificada
conn = st.connection("gsheets", type=GSheetsConnection)

# Intentamos leer los datos de la primera hoja disponible
try:
    data = conn.read(ttl=0)
except Exception:
    data = pd.DataFrame()

# 3. Formulario lateral
st.sidebar.header("Nueva Sesión")
usuario = st.sidebar.text_input("Atleta", value="Sandra")
fecha = st.sidebar.date_input("Fecha")
indice = st.sidebar.text_input("Ejercicio principal")
warmup = st.sidebar.text_area("Warm-up")
fuerza = st.sidebar.text_area("Fuerza")
metcon = st.sidebar.text_area("WOD")
acc = st.sidebar.text_area("Accesorios")

if st.sidebar.button("Guardar en mi Diario"):
    new_row = pd.DataFrame([{
        "Usuario": usuario, "Fecha": str(fecha), "Indice": indice,
        "Warmup": warmup, "Fuerza": fuerza, "Metcon": metcon, "Accesorios": acc
    }])
    try:
        # Buscamos datos actuales y añadimos la nueva fila
        current_data = conn.read(ttl=0)
        updated_df = pd.concat([current_data, new_row], ignore_index=True)
        # Actualizamos la hoja
        conn.update(data=updated_df)
        st.sidebar.success("¡Guardado correctamente!")
        st.balloons()
        st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# 4. Tabla central
st.divider()
if not data.empty:
    st.dataframe(data.sort_index(ascending=False), use_container_width=True)
else:
    st.info("Introduce un entrenamiento para empezar.")
