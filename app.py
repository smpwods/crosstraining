import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración inicial
st.set_page_config(page_title="CrossTraining Progress", layout="wide")
st.title("🏋️ Mi Programación de CrossTraining")

# 2. Conexión
conn = st.connection("gsheets", type=GSheetsConnection)
# Esta línea es la que te falta y es fundamental:
data = conn.read(ttl=0)
# 3. Identificación en el lateral
st.sidebar.header("Identificación")
usuario = st.sidebar.text_input("Nombre de Atleta", value="Sandra")

st.sidebar.divider()
st.sidebar.header("Nueva Sesión")

# 4. Entradas de datos
fecha = st.sidebar.date_input("Fecha")
main_exercises = st.sidebar.text_input("Índice (Ejercicios del día)")
warmup = st.sidebar.text_area("Warm-up")
part_a = st.sidebar.text_area("A. Fuerza/Skill")
part_b = st.sidebar.text_area("B. Metcon (WOD)")
part_c = st.sidebar.text_area("C. Accesorios/Mobility")

# 5. Lógica para Guardar
if st.sidebar.button("Guardar en mi Diario"):
    if usuario:
        new_data = pd.DataFrame([{
            "Usuario": usuario,
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Indice": main_exercises,
            "Warmup": warmup,
            "Fuerza": part_a,
            "Metcon": part_b,
            "Accesorios": part_c
        }])

try:
            # Leemos y actualizamos usando explícitamente "Sheet1"
            old_data = conn.read(worksheet="Sheet1", ttl=0)
            updated_df = pd.concat([old_data, new_data], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.sidebar.success("¡WOD guardado!")
            st.cache_data.clear()
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error al guardar: {e}")

# --- ESTO VA PEGADO AL BORDE IZQUIERDO (SIN ESPACIOS) ---
st.divider()
if not data.empty:
    st.dataframe(data.sort_index(ascending=False), use_container_width=True)
else:
    st.info("No hay entrenamientos registrados aún.")
        
    st.info("No hay entrenamientos registrados aún.")
