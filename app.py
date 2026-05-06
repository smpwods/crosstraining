import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="CrossFit Cloud", layout="wide")
st.title("🏋️ Mi Programación de CrossTraining")

# Recuperamos la URL de los Secrets
try:
    sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
except Exception:
    sheet_url = ""

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Identificación")
    usuario = st.text_input("Nombre de Atleta", placeholder="Tu nombre aquí")
    
    st.divider()
    st.header("Nueva Sesión")
    new_date = st.date_input("Fecha", datetime.date.today())
    main_exercises = st.text_input("Índice (Ejercicios del día)")
    
    warmup = st.text_area("Warm-up")
    part_a = st.text_area("A. Fuerza/Skill")
    part_b = st.text_area("B. Metcon (WOD)")
    part_c = st.text_area("C. Accesorios")
    
    if st.button("Guardar en mi Diario"):
        st.error("Para guardar entrenamientos, necesitamos usar la API completa. Primero estabilicemos la lectura con este código.")

# --- TABLERO PRINCIPAL ---
st.subheader(f"Tablero de WODs: {usuario if usuario else 'Identifícate'}")

if not sheet_url:
    st.error("Falta configurar la URL en los Secrets de Streamlit.")
elif usuario:
    try:
        # Lee directamente el CSV de Google Sheets de forma ultra-rápida y sin errores de HTTP
        data = pd.read_csv(sheet_url)
        
        if not data.empty and 'Usuario' in data.columns:
            user_data = data[data['Usuario'] == usuario]
            
            if not user_data.empty:
                for _, row in user_data.sort_values(by="Fecha", ascending=False).iterrows():
                    with st.expander(f"📅 {row['Fecha']} - {row['Indice']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Warm-up:**")
                            st.write(row.get('Warmup', ''))
                            st.markdown("**Fuerza:**")
                            st.write(row.get('Fuerza', ''))
                        with col2:
                            st.markdown("**Metcon:**")
                            st.write(row.get('Metcon', ''))
                            st.markdown("**Accesorios:**")
                            st.write(row.get('Accesorios', ''))
            else:
                st.info("No hay entrenamientos guardados para este atleta.")
        else:
            st.warning("La estructura del Excel no es correcta. Asegúrate de tener las columnas: Usuario, Fecha, Indice, Warmup, Fuerza, Metcon, Accesorios")
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
