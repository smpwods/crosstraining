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
    # AQUÍ ESTÁ EL RECUADRO QUE FALTA:
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
                "Fecha": new_date.strftime("%Y-%m-%d"),
                "Usuario": usuario,
                "Indice": main_exercises,
                "Warmup": warmup,
                "Fuerza": part_a,
                "Metcon": part_b,
                "Accesorios": part_c
            }])
            old_data = conn.read(worksheet="Sheet1")
            updated_df = pd.concat([old_data, new_data], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success("¡Entrenamiento guardado!")
            st.cache_data.clear()
        else:
            st.error("Por favor, escribe tu nombre arriba")

# --- TABLERO PRINCIPAL ---
st.subheader(f"Tablero de WODs: {usuario if usuario else 'Identifícate'}")

if usuario:
    data = conn.read(worksheet="Sheet1")
    user_data = data[data['Usuario'] == usuario]
    
    if not user_data.empty:
        for _, row in user_data.sort_values(by="Fecha", ascending=False).iterrows():
            with st.expander(f"📅 {row['Fecha']} - {row['Indice']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Warm-up:**")
                    st.write(row['Warmup'])
                    st.markdown("**Fuerza:**")
                    st.write(row['Fuerza'])
                with col2:
                    st.markdown("**Metcon:**")
                    st.write(row['Metcon'])
                    st.markdown("**Accesorios:**")
                    st.write(row['Accesorios'])
    else:
        st.info("No hay entrenamientos guardados para este atleta.")
