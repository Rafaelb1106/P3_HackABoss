# Importación de las librerías necesarias
import streamlit as st
import pandas as pd
import numpy as np
import random

# Desactivar advertencias de desaprobación de Streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)

# Función para cargar los datos desde una URL. Esta función está decorada con st.cache_data
# En las ejecuciones subsiguientes, se cargará una versión en caché de los datos.

@st.cache_data
def read_csv_streamlit():
    url = "https://drive.google.com/u/0/uc?id=1ePhuTPZWNkW4Nw634dXxV21fneJRgNWo&export=download&confirm=t&uuid=61491d58-19cc-11ee-be56-0242ac120002"
    df = pd.read_csv(url)
    return df
    
df_Beer = read_csv_streamlit()

def main():

     # Imprimimos mensajes en la interfaz de usuario
    st.title("Recomendador Inteligente de Cervezas")
    st.write("""
    Este proyecto se centra en la creación de un sistema de recomendación personalizado para los amantes de la cerveza. 
    Este sistema utiliza técnicas de aprendizaje automático para analizar tus preferencias de cerveza y generar recomendaciones que se alinean con tus gustos individuales.
    
    Para empezar, los usuarios seleccionan cinco tipos de cerveza que han probado previamente y proporcionan calificaciones para cada una de ellas. 
    Esta información inicial nos ayuda a entender las preferencias del usuario y a construir su perfil de sabor.
    
    Posteriormente, nuestro algoritmo compara este perfil de sabor con nuestra base de datos de cientos de miles de reseñas de cervezas proporcionadas por otros usuarios. 
    Al considerar las similitudes en las preferencias de cerveza entre los usuarios, nuestro sistema puede identificar y sugerir nuevas cervezas que el usuario probablemente disfrutará.

    Lo más destacado de este código es cómo se maneja la selección de la cerveza recomendada. En lugar de simplemente elegir la cerveza con la puntuación más alta, 
    selecciona al azar una de las cinco cervezas con mayor puntuación. Esto se hace para introducir variedad en las recomendaciones.
    """)
    st.write(' ')

    # Mostramos un avance de los datos en la interfaz de usuario
    df_display = df_Beer.head()
    st.subheader("Vista previa del DataFrame:")
    st.write(df_display)
    st.write(' ')

    # Creamos una tabla pivote de los datos
    matriz_df = df_Beer.pivot_table(
        values='review/overall',
        index='review/profileName',
        columns='beer/style',
        aggfunc='max'
    )

    # Obtenemos una lista de todas las cervezas
    all_beers = matriz_df.columns.tolist()

    # Preparamos las opciones para la selección de cerveza
    beer_choices = ["Selecciona una cerveza..."] + all_beers

    # Preparamos un diccionario vacío para almacenar las calificaciones del usuario
    user_ratings = {}

    # Solicitamos al usuario que seleccione y califique 5 cervezas
    for i in range(1, 6):
        beer_choice = st.selectbox(f'Selecciona tu {i}º estilo de cerveza:', beer_choices, key=f"beer{i}")
        rating = st.slider(f'Califica el {i}º estilo de cerveza:', 0.0, 5.0, step=0.5, key=f"rating{i}")

        # Solo guardamos las calificaciones de las cervezas que el usuario realmente seleccionó
        if beer_choice != "Selecciona una cerveza...":
            user_ratings[beer_choice] = rating

    # Proporcionamos un botón para enviar las calificaciones
    submit_button = st.button('Submit')

    # Si el usuario presiona el botón de enviar, realizamos el cálculo de las recomendaciones
    if submit_button:
        st.subheader("Los estilos seleccionados y sus calificaciones son:")
        st.write(user_ratings)

        nuevo_usuario_serie = pd.Series(user_ratings, name='Nuevo Usuario')
        matriz_df.loc['Nuevo Usuario'] = nuevo_usuario_serie

        cervezas_calificadas = list(user_ratings.keys())
        usuarios_similares = matriz_df.dropna(subset=cervezas_calificadas)
        usuarios_similares = usuarios_similares.apply(pd.to_numeric, errors='coerce')

        nuevo_usuario_ratings = usuarios_similares.loc['Nuevo Usuario']
        correlaciones = usuarios_similares.apply(lambda row: row.corr(nuevo_usuario_ratings), axis=1)

        correlaciones_df = pd.DataFrame(correlaciones, columns=['correlation'])
        usuarios_similares['corr'] = correlaciones_df['correlation']

        rating_matrix_subset = usuarios_similares.drop("Nuevo Usuario").drop(usuarios_similares.dropna(axis=1).columns, axis=1)
        correlaciones_ajustadas = correlaciones_df.loc[rating_matrix_subset.index].values.reshape(-1, 1)

        weighted_rating_matrix = rating_matrix_subset.values * correlaciones_ajustadas
        weighted_rating_matrix_sum = np.nansum(weighted_rating_matrix, axis=0)
        similarity_sum = np.nansum(np.abs(correlaciones_df), axis=0)

        predicted_ratings = weighted_rating_matrix_sum / similarity_sum

        # Obtenemos los índices de las 5 cervezas con mayor puntuación predicha
        top_5_beer_indices = np.argsort(-predicted_ratings)[:5]

        # Seleccionamos al azar un índice entre los 5 principales. 
        # Esto introduce variedad en las recomendaciones, en lugar de simplemente seleccionar la cerveza con mayor puntuación cada vez.
        recommended_beer_index = random.choice(top_5_beer_indices)

        # Obtenemos el nombre de la cerveza recomendada
        recommended_beer = matriz_df.columns[recommended_beer_index]

        # Obtenemos todas las cervezas del estilo recomendado
        beers_of_recommended_style = df_Beer[df_Beer['beer/style'] == recommended_beer]

        # Obtenemos las cervezas de mayor puntuación dentro del estilo recomendado
        highest_rated_beers = beers_of_recommended_style[beers_of_recommended_style['review/overall'] == beers_of_recommended_style['review/overall'].max()]

        # Seleccionamos al azar una cerveza entre las de mayor puntuación. 
        # Esto introduce variedad en las recomendaciones, en lugar de simplemente seleccionar la cerveza de mayor puntuación cada vez.
        highest_rated_beer = random.choice(highest_rated_beers['beer/name'].tolist())

        # Imprimimos la recomendación en la interfaz de usuario
        st.markdown(
            f'Según tus preferencias, la recomendación por _Estilo de Cerveza_ que debes probar es:<br><b>{recommended_beer}</b> '
            f'<br><br>La _Cerveza_ recomendada es:<br><b>{highest_rated_beer}</b>.',
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
