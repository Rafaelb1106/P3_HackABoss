import streamlit as st
from pages.pages import plots, recomend

df_Beer = recomend.df_Beer

def main():
    # Mostrar enlaces para elegir entre plots.py y app.py
    opcion = st.radio("Seleccione una opción:", ["App", "Gráficos"])

    if opcion == "App":
        recomend.main()
    elif opcion == "Gráficos":
        plots.main()

if __name__ == '__main__':
    main()
