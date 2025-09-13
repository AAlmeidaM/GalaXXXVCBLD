import streamlit as st
import random

# Configuración inicial
st.set_page_config(page_title="Bingo Solidario", layout="wide")

# Colores
COLOR_FONDO = "#551128"   # equivale a rgba(85,17,40,255)
COLOR_TEXTO = "#fafbf9"
COLOR_SALIDOS = "#c0a151"

# CSS personalizado
st.markdown(
    f"""
    <style>
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: {COLOR_FONDO};
            color: {COLOR_TEXTO};
        }}
        /* Ocultar menú, footer y barra lateral */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        [data-testid="stSidebar"] {{display: none;}}

        .numero-actual {{
            background-color: {COLOR_SALIDOS};
            color: black;
            font-size: 100px;
            font-weight: bold;
            border-radius: 15px;
            padding: 30px;
            margin: 20px auto;
            text-align: center;
            width: 200px;
        }}
        .numero-anterior {{
            background-color: {COLOR_SALIDOS};
            color: black;
            font-size: 40px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
            display: inline-block;
            width: 80px;
            text-align: center;
        }}
        .numero {{
            display: inline-block;
            width: 50px;
            height: 50px;
            margin: 3px;
            text-align: center;
            line-height: 50px;
            border-radius: 5px;
            font-weight: bold;
            background-color: white;
            color: black;
        }}
        .numero-salido {{
            background-color: {COLOR_SALIDOS} !important;
            color: black !important;
        }}
        /* Botones con texto negro */
        div.stButton > button {{
            color: black !important;
            font-weight: bold;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Función para reiniciar el bingo
def resetear_bingo():
    st.session_state.numeros = list(range(1, 91))
    random.shuffle(st.session_state.numeros)
    st.session_state.salidos = []

# Estado inicial
if "numeros" not in st.session_state or "salidos" not in st.session_state:
    resetear_bingo()

# Encabezado
st.title("Bingo Solidario Cambalada - ELA")
st.subheader("Gala XXXV Aniversario ELA")

st.markdown("---")

# Botones
col_btn1, col_btn2 = st.columns([1,1])
with col_btn1:
    if st.button("🎱 Sacar número"):
        if st.session_state.numeros:
            nuevo = st.session_state.numeros.pop()
            st.session_state.salidos.append(nuevo)

with col_btn2:
    if st.button("🔄 Resetear Bingo"):
        resetear_bingo()

# Layout en columnas
col1, col2 = st.columns([1, 2])

# Columna izquierda: número actual + últimos 3
with col1:
    if st.session_state.salidos:
        st.markdown(
            f"<div class='numero-actual'>{st.session_state.salidos[-1]}</div>",
            unsafe_allow_html=True,
        )

    if len(st.session_state.salidos) > 1:
        ultimos = st.session_state.salidos[-4:-1]  # últimos 3 en orden de salida
        st.markdown("#### Últimos 3 números")
        for n in ultimos:
            st.markdown(f"<div class='numero-anterior'>{n}</div>", unsafe_allow_html=True)

# Columna derecha: tablero de bingo
with col2:
    st.markdown("### Tablero de Bingo")
    tablero = ""
    for i in range(1, 91):
        clase = "numero"
        if i in st.session_state.salidos:
            clase += " numero-salido"
        tablero += f"<div class='{clase}'>{i}</div>"
        if i % 10 == 0:
            tablero += "<br>"
    st.markdown(tablero, unsafe_allow_html=True)



