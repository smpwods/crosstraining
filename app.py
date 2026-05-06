import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="CrossTraining Progress", layout="wide")

# Título con icono de CrossFit
st.title("🏋️ Mi Programación de CrossTraining")

# Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- IDENTIFICACIÓN ---
st.sidebar.header("Identificación")
usuario = st.sidebar.text_input("Nombre de Atleta", value="Sandra")

# --- FORMULARIO DE NUEVA SESIÓN ---
st.sidebar.divider()
st.sidebar.header("Nueva Sesión")

fecha = st.sidebar.date_input("Fecha")
main_exercises = st.sidebar.text_input("Índice (Ejercicios del día)")
warmup = st.sidebar.text_area("Warm-up")
part_a = st.sidebar.text_area("A. Fuerza/Skill")
part_b = st.sidebar.text_area("B. Metcon (WOD)")
part_c = st.sidebar.text_area("C. Accesorios/Mobility")

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
            # Lectura de la pestaña Sheet1
            old_data = conn.read(worksheet="Sheet1", ttl=0)
            updated_df = pd.concat([old_data, new_data], ignore_index=True)
            
            # Actualización en la pestaña Sheet1
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.sidebar.success("¡WOD guardado correctamente!")
            st.cache_data.clear()
        except Exception as e:
            st.sidebar.error(f"Error al conectar: {e}")
    else:
        st.sidebar.error("Por favor, escribe tu nombre arriba")

# --- TABLERO PRINCIPAL ---
st.subheader(f"Tablero de WODs: {usuario if usuario else 'Identifícate'}")

if usuario:
    try:
        # Lectura para mostrar datos en el tablero
        data = conn.read(worksheet="Sheet1", ttl=0)
        
        if not data.empty and 'Usuario' in data.columns:
            user_data = data[data['Usuario'] == usuario]
            
            if not user_data.empty:
                for _, row in user_data.sort_values(by="Fecha", ascending=False).iterrows():
                    with st.expander(f"📅 {row['Fecha']} - {row['Indice']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Warm-up:**")
                            st.write(row.get('Warmup', ''))
                            st.markdown("**A. Fuerza/Skill:**")
                            st.write(row.get('Fuerza', ''))
                        with col2:
                            st.markdown("**B. Metcon (WOD):**")
                            st.write(row.get('Metcon', ''))
                            st.markdown("**C. Accesorios:**")
                            st.write(row.get('Accesorios', ''))
            else:
                st.info(f"Aún no hay entrenamientos registrados para {usuario}")
        else:
            st.warning("La base de datos está vacía o no tiene el formato correcto.")
            
    except Exception:
        st.error("Esperando conexión con Google Sheets...")
