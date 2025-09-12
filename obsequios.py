import streamlit as st
import random

# Configuración inicial
st.set_page_config(page_title="Dinámica Solidaria CBDL - ELA", layout="wide")

# Colores
COLOR_FONDO = "#551128"   # rgba(85,17,40,255)
COLOR_TEXTO = "#fafbf9"
COLOR_CAJA = "#c0a151"

# CSS personalizado
st.markdown(
    f"""
    <style>
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: {COLOR_FONDO};
            color: {COLOR_TEXTO};
            font-family: "Comic Sans MS", "Comic Neue", cursive, sans-serif;
        }}
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        [data-testid="stSidebar"] {{display: none;}}

        .caja-premio {{
            background-color: {COLOR_CAJA};
            color: black;
            font-size: 60px;
            font-weight: bold;
            border-radius: 15px;
            padding: 30px;
            margin: 30px auto;
            text-align: center;
            width: 80%;
        }}
        .caja-ganador {{
            background-color: {COLOR_CAJA};
            color: black;
            font-size: 80px;
            font-weight: bold;
            border-radius: 15px;
            padding: 30px;
            margin: 20px auto;
            text-align: center;
            width: 80%;
        }}
        .mensaje {{
            font-size: 32px;
            color: {COLOR_TEXTO};
            margin-top: 15px;
            text-align: center;
        }}
        div.stButton > button {{
            color: black !important;
            font-weight: bold;
            font-size: 20px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Función para resetear
def resetear_dinamica():
    st.session_state.regalos = []
    st.session_state.participantes = []
    st.session_state.asignaciones = []
    st.session_state.indice_regalo = 0
    st.session_state.en_progreso = False
    st.session_state.ganador_actual = None
    st.session_state.mostrar_ganador = False

# Estado inicial
if "en_progreso" not in st.session_state:
    resetear_dinamica()

# Pantalla inicial: pegar listas
if not st.session_state.en_progreso:
    st.title("🎁 Dinámica Solidaria ELA")
    st.subheader("Gala XXXV Aniversario CAMBALADA")
    st.markdown("---")

    st.markdown("### 📋 Pegue la lista de **obsequios** (uno por línea):")
    regalos_input = st.text_area("Obsequios", height=200, placeholder="Ejemplo:\nCesta de Navidad\nJamón Ibérico\nBotella de Vino")

    st.markdown("### 👤 Pegue la lista de **participantes** (uno por línea):")
    participantes_input = st.text_area("Participantes", height=200, placeholder="Ejemplo:\nMaría\nJuan\nLucía")

    if st.button("🚀 Iniciar dinámica"):
        if regalos_input.strip() and participantes_input.strip():
            st.session_state.regalos = [r.strip() for r in regalos_input.splitlines() if r.strip()]
            st.session_state.participantes = [p.strip() for p in participantes_input.splitlines() if p.strip()]
            random.shuffle(st.session_state.participantes)
            st.session_state.en_progreso = True
            st.rerun()
        else:
            st.error("Debe introducir al menos un obsequio y un participante.")

# Pantalla principal
else:
    st.title("🎁 Agradecimiento Donaciones ELA")
    st.subheader("Gala XXXV Aniversario Cambalada")
    st.markdown("---")

    if st.session_state.indice_regalo < len(st.session_state.regalos):
        premio_actual = st.session_state.regalos[st.session_state.indice_regalo]

        # Mostrar el premio actual
        st.markdown(f"<div class='caja-premio'>🎁 {premio_actual}</div>", unsafe_allow_html=True)

        # Si ya se seleccionó el ganador, mostrarlo
        if st.session_state.mostrar_ganador and st.session_state.ganador_actual:
            st.markdown(f"<div class='caja-ganador'>🏆 {st.session_state.ganador_actual}</div>", unsafe_allow_html=True)
            st.markdown("<div class='mensaje'>¡Gracias por tu aportación! 💜</div>", unsafe_allow_html=True)

            # Botón para pasar al siguiente premio
            if st.button("➡️ Siguiente premio"):
                st.session_state.indice_regalo += 1
                st.session_state.ganador_actual = None
                st.session_state.mostrar_ganador = False
                st.rerun()
        else:
            # Botón para elegir ganador
            if st.button("🎲 Seleccionar ganador"):
                if st.session_state.participantes:
                    ganador = st.session_state.participantes.pop(0)
                    st.session_state.asignaciones.append((premio_actual, ganador))
                    st.session_state.ganador_actual = ganador
                    st.session_state.mostrar_ganador = True
                    st.balloons()
                    st.rerun()
                else:
                    st.error("No quedan participantes suficientes para asignar más obsequios.")

        # Mostrar agradecimientos anteriores
        if st.session_state.asignaciones:
            st.markdown("### 🏆 Agradecimientos anteriores")
            for reg, gan in st.session_state.asignaciones[:-1]:
                st.markdown(f"<div class='caja-premio'>{reg} → {gan}</div>", unsafe_allow_html=True)

    else:
        st.success("🎉 ¡FIN DE LA DINÁMICA! Todos los obsequios han sido repartidos.")
        st.markdown("### 🏆 Resultado final")
        for reg, gan in st.session_state.asignaciones:
            st.markdown(f"<div class='caja-premio'>{reg} → {gan}</div>", unsafe_allow_html=True)

        if st.button("🔄 Nueva dinámica"):
            resetear_dinamica()
            st.rerun()
