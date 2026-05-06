import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración inicial
st.set_page_config(page_title="CrossTraining Progress", layout="wide")
st.title("🏋️ Mi Programación de CrossTraining")

# 2. Conexión (Asegúrate de que los Secrets tengan la URL de edición)
conn = st.connection("gsheets", type=GSheetsConnection)

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
        except Exception as e:
            st.sidebar.error(f"Error al guardar: {e}")
    else:
        st.sidebar.error("Escribe tu nombre")

# 6. Tablero de Visualización
st.subheader(f"Tablero de WODs: {usuario if usuario else 'Identifícate'}")

if usuario:
    try:
        # Esta es la línea que fallaba en image_855e30.png
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
                st.info(f"No hay entrenamientos para {usuario}")
        else:
            st.warning("Configura las columnas en tu Excel: Usuario, Fecha, Indice, Warmup, Fuerza, Metcon, Accesorios")
            
    except Exception:
        # Si esto sale, revisa que el botón azul de compartir en Sheets diga "Editor"
        st.error("Esperando conexión con Google Sheets...")
