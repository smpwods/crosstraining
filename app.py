import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

st.set_page_config(page_title="CrossFit Cloud", layout="wide")
st.title("🏋️ Mi Programación de CrossTraining")

# Conexión
conn = st.connection("gsheets", type=GSheetsConnection)

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
        if usuario:
            new_data = pd.DataFrame([{
                "Usuario": usuario,
                "Fecha": new_date.strftime("%Y-%m-%d"),
                "Indice": main_exercises,
                "Warmup": warmup,
                "Fuerza": part_a,
                "Metcon": part_b,
                "Accesorios": part_c
            }])
            # Lectura sin parámetros para maximizar compatibilidad
            old_data = conn.read(worksheet="Sheet1", ttl=0)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.cache_data.clear()
        else:
            st.error("Por favor, escribe tu nombre arriba")

# --- TABLERO PRINCIPAL ---
st.subheader(f"Tablero de WODs: {usuario if usuario else 'Identifícate'}")

if usuario:
    try:
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
                            st.markdown("**Fuerza:**")
                            st.write(row.get('Fuerza', ''))
                        with col2:
                            st.markdown("**Metcon:**")
                            st.write(row.get('Metcon', ''))
                            st.markdown("**Accesorios:**")
                            st.write(row.get('Accesorios', ''))
            else:
                st.info(f"Hola {usuario}, aún no hay WODs registrados a tu nombre.")
        else:
            st.warning("Estructura del Excel detectada. Si ves este mensaje, refresca la página.")
    except Exception as e:
        st.error("Esperando conexión con Google Sheets...")
