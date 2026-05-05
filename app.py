import streamlit as st
import datetime

st.set_page_config(page_title="CrossFit Cloud", layout="wide")
st.title("🏋️‍♂️ Mi Programación de CrossTraining")

if 'wod_cards' not in st.session_state:
    st.session_state['wod_cards'] = {}

with st.sidebar:
    st.header("Nueva Sesión")
    new_date = st.date_input("Fecha", datetime.date.today())
    main_exercises = st.text_input("Índice (Ejercicios del día)", placeholder="Ej: Clean, Pull-ups, Box Jumps")
    st.divider()
    warmup = st.text_area("Warm-up")
    part_a = st.text_area("A. Fuerza/Skill")
    part_b = st.text_area("B. Metcon (WOD)")
    part_c = st.text_area("C. Accesorios")
    if st.button("Guardar Entrenamiento"):
        st.session_state['wod_cards'][str(new_date)] = {
            "index": main_exercises, "warmup": warmup,
            "parts": {"A": part_a, "B": part_b, "C": part_c}
        }
        st.success("¡Guardado!")

st.subheader("Tablero de WODs")
cols = st.columns(3)
for i, (date, data) in enumerate(reversed(list(st.session_state['wod_cards'].items()))):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"### 📅 {date}")
            st.warning(f"**Incluye:** {data['index']}")
            with st.expander("Abrir detalles y notas"):
                st.write("**Warm-up:**", data['warmup'])
                st.text_area("Notas Warm-up", key=f"nw_{date}")
                for letter, content in data['parts'].items():
                    st.markdown(f"**Parte {letter}:**")
                    st.info(content)
                    st.text_area(f"Anotaciones Parte {letter}", key=f"n_{letter}_{date}")
