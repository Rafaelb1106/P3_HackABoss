### HACK A BOSS ###
### BOOTCAMP DATA SCIENCE - dsb02rt ### 
### PROYECTO 1 ### 
### GRUPO D ### 
### RAFAEL BALLESTEROS, JESÚS TRIGO, JULIO MENDOZA ### 

### NOTA ###
### Para hacer prueba sin web scrapping, escribir la palabra matrix ###

####### IMPORT #######

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from time import sleep
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import helium
from pprint import pprint
import json
import re
import warnings
import plotly as plt
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import random
from airtable import Airtable # para las funciones de Airtable
import streamlit as st




    

####### CONEXIÓN A AIRTABLE #######

API_KEY = "keyd2qZkAIAcDVhux" # Usuario
BASE_ID = "app0qw5QLhMPyPXJs" # Base: Tabla API
TABLE_ID = "tblEop10joaI8QrXL" # Tabla: Ensaladas API
BASE_URL = 'https://api.airtable.com/v0/'

headers = {"Authorization" : f"Bearer {API_KEY}",
           "Content-Type"  : "application/json"}

if 'ban2' not in st.session_state:    
    st.session_state['ban2'] = 5

####### funciones #######

def insertardf(dft , BD, tabla, apikey):
    try:
        airtable_base_url = "https://api.airtable.com/v0"
        headers = {"Authorization" : f"Bearer {apikey}",
                   "Content-Type"  : "application/json"}
        endpoint = f"{airtable_base_url}/{BD}/{tabla}"
        L_campos = list(dft.columns)
        datos = []
                                  # Revision
        for i in range(len(dft)): # df.shape[0]
            info = dft.iloc[i]
            dicc = {}              # Revision 
            for camp in L_campos: # list(dft.columns)
                if (info[camp] != 'Sin datos') & (info[camp] != 0.0):
                    if type(info[camp]) == list:
                        dicc[camp] = ", ".join(info[camp]) 
                    else: 
                        dicc[camp] = info[camp]
                        
            record = {"fields": dicc}
            
            datos.append(record)
            
        dict_pelis = {"records": datos}
 
        for record in dict_pelis["records"]:
        
            data = {"fields": record["fields"]}
            
            response = requests.post(url=endpoint, json=data, headers=headers)

        return True
    
    except:
        
        return False

def listarDFtabla(BD, tabla, apikey): # airtable_to_dataframe
    # Revision
    # res = {}
    
    try:
        res = {} # Sacar del try
        
        airtable_base_url = "https://api.airtable.com/v0"
        
        headers = {"Authorization" : f"Bearer {apikey}",
                   "Content-Type"  : "application/json"}
        
        endpoint = f"{airtable_base_url}/{BD}/{tabla}"
        
        params = {"fields"                : None, 
                  "maxRecords"            : None, 
                  "pageSize"              : None,
                  "returnFieldsByFieldId" : False}
        
        response = requests.get(url = endpoint, headers = headers, params = params)
        
        #pprint(response.json(), sort_dicts = False)
        
        if response.status_code != 200:
            return res
        
        else:            
            return response.json()    
        
    except:
        return res
    
def creardfcontabla(info): # info
    
    # Revision
    # dic_res
    
    dic_res1 = dic_res["records"]
    
    l_columns = list(dic_res1[0]["fields"].keys())
    
    df_listado = pd.DataFrame(columns = l_columns)
    
    warnings.filterwarnings('ignore')
    
    for x in range(0, len(dic_res1)):
        
        df_listado = df_listado.append(dic_res1[x]["fields"], ignore_index = True)
        
    return df_listado

##--##--##
def airtable_to_dataframe(BASE_ID, TABLE_ID, API_KEY):
    
    # Revision
    
    header = {'Authorization': 'Bearer ' + API_KEY} # format
    
    data = []
    
    offset = ''
    
    while True:
        
        r = requests.get(BASE_URL + BASE_ID + '/' + TABLE_ID, headers=header, params={'offset': offset}) # format
        
        for x in r.json().get('records'):
            
            x.update(x.get('fields'))
            x.pop('fields')
            data.append(x)
            
        if 'offset' in r.json():
            
            offset = r.json()['offset']
            
        else:
            
            break
            
    df = pd.json_normalize(data)
    
    return df


def main():
    st.title("Web Scraping con Selenium Python.")
    st.write("Seleccione cualquiera de los dos siguientes opciones ")
    st.write("Nota: es necesario Chrome para el correcto funcionamiento.")
    ban = 0 
    opt = 0       
    airtable = Airtable(BASE_ID, TABLE_ID, API_KEY)
    boton1 = False
    menu_bus = []
    data_from_airtable = pd.DataFrame(airtable_to_dataframe(BASE_ID, TABLE_ID, API_KEY))    
    menu_bus = list(set(data_from_airtable["Busqueda"]))    
    col1, col2 = st.columns(2)

    st.write("Digite la palabra clave para explorar los datos de las películas mediante scraping.")
    col1, col2 = st.columns(2)
    with col1:        
        busqueda = st.text_input(label="Busqueda", max_chars = 20, placeholder="Nombre Pelicula", label_visibility="collapsed")
    with col2:
        boton1 = st.button(label="Buscar", key="B1")

    st.write("Seleccione una búsqueda ya realizada para ver sus graficas en esta opción no se hace scraping")
    col11, col22 = st.columns(2)
    with col11:        
        busqueda1 = st.selectbox("Anteriores_Busquedas", options = menu_bus, label_visibility="collapsed")
    with col22:
        if st.button(label="Buscar", key="B3"):
            ban = 1
            opt = 1
    
    if boton1:        
        
        #busqueda = input("Digite la palabra clave para explorar los datos de las películas: ")
        records = airtable.get_all(formula = f"FIND('{busqueda.lower()}', LOWER({{Busqueda}}))")
        # INPUT DE BÚSQUEDA

        #se controla si la palabra de búsqueda existe no vuelva a buscar
        if len(records) == 0:
            
            ####### WEB SCRAPPING IMDB #######
            ####### OBTENER REGISTROS #######
            browser = webdriver.Chrome(ChromeDriverManager().install())
            browser.get("https://imdb.com")
            browser.maximize_window()
            sleep(2)
            buscador  = browser.find_element_by_xpath('//*[@id="suggestion-search"]')
            sleep(1)
            buscador.clear()
            sleep(3)
            buscador.clear()
            sleep(3)
            buscador.send_keys(busqueda)
            sleep(3)
            buscador.submit()
            sleep(3)

            # ENCONTRAR BOTÓN MÁS RESULTADOS

            boton = browser.find_element_by_css_selector(".find-see-more-title-btn > button:nth-child(1)")

            element = browser.find_element_by_xpath("//h3[contains(text(),'Títulos')]")

            # BUCLE CON CLICS AL BOTÓN MÁS RESULTADOS

            for y in range(0,2):
                try:
                    browser.execute_script("arguments[0].scrollIntoView(true);", boton)
                    sleep(3)
                    boton.click()
                except:
                    pass

            # CREACIÓN DE LISTA CON URLS DE LOS LINKS EN RESULTADOS

            soup = BeautifulSoup(browser.page_source, "html.parser")

            lista_pelis = soup.find_all('li', class_= 'ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click find-result-item find-title-result')

            urls_pelis = list()

            for i in lista_pelis:
                pelis = i.find('a')
                urls = 'https://www.imdb.com' + pelis['href']
                urls_pelis.append(urls)

            # CREACIÓN DE LISTAS VACÍAS PARA USAR EN EL SCRAPPING POR PÁGINA

            titulos = list()
            fecha = list()
            sinopsis = list()
            idioma_original = list()
            rating = list()
            ratingCount = list()
            genero = list()
            director = list()
            busqueda_input = list()
            mejor_calificacion = list()
            peor_calificacion = list()

            url_trailer = []
            actores = []
            duracion = []
            clasificasion = []

            score = []
            resena_critic =[]
            resena_user = []
            premios = []
            nominaciones = []

            # BUCLE QUE RECORRE CADA PÁGINA EN LA LISTA DE URLS

            for i in urls_pelis:

                try:
                    browser.get(i)
                    # Revision
                    # sleep(1)
                    html = browser.page_source
                    soup = BeautifulSoup(html, "html.parser")
                except:
                    pass

            # EXTRACCIÓN DE DATOS DE CADA PÁGINA

                try:
                    titulos.append(soup.find('h1').text)
                except:
                    # Revision
                    # titulos.append(np.nan)
                    titulos.append('Sin datos')

                try:
                    duracion_find = soup.find('ul', class_='ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt')
                    duracion_list = duracion_find.find_all('li', class_='ipc-inline-list__item')
                    duracion_3 = duracion_list[2]
                    duracion_text = duracion_3.text
                    
                    if 'h' in duracion_text and 'min' in duracion_text:
                        
                        partes = duracion_text.split()
                        horas = int(partes[0].replace('h', ''))
                        minutos = int(partes[1].replace('min', ''))
                        
                    elif 'h' in duracion_text:
                        
                        horas = int(duracion_text.replace('h', ''))
                        minutos = 0
                        
                    elif 'min' in duracion_text:
                        
                        horas = 0
                        minutos = int(duracion_text.replace('min', ''))
                        
                    else:
                        horas = 0
                        minutos = 0
                        
                    duracion_total = horas*60 + minutos
                    duracion.append(duracion_total)
                    
                except:
                    
                    duracion.append(0)
                    # Revision
                    # duracion.append(np.nan)

                try:
                    premios_find = soup.find('span', {'class': 'ipc-metadata-list-item__list-content-item'})
                    premios_text = premios_find.text
                    premios_list = premios_text.split()
                                                    
                    if 'premios' in premios_list or 'premio' in premios_list:
                        
                        if 'premios' in premios_list:
                            
                            premios_index = premios_list.index('premios') - 1
                            
                        elif 'premio' in premios_list:
                            
                            premios_index = premios_list.index('premio') - 1
                            
                        premios.append(int(premios_list[premios_index]))
                        
                    else:
                        premios.append(0)
                        
                except:
                    
                    premios.append(0)
                    
                try:
                    nominaciones_find = soup.find('span', {'class': 'ipc-metadata-list-item__list-content-item'})
                    nominaciones_text = nominaciones_find.text
                    nominaciones_list = nominaciones_text.split()
                    
                    # Se puede simplificar el if
                    
                    if 'nominaciones' in nominaciones_list or 'nominación' in nominaciones_list or 'nominacion' in nominaciones_list:
                        if 'nominaciones' in nominaciones_list:
                            nominaciones_index = nominaciones_list.index('nominaciones') - 1
                            nominaciones.append(int(nominaciones_list[nominaciones_index]))
                        elif 'nominación' in nominaciones_list:
                            nominaciones_index = nominaciones_list.index('nominación') - 1
                            nominaciones.append(int(nominaciones_list[nominaciones_index]))
                        elif 'nominacion' in nominaciones_list:
                            nominaciones_index = nominaciones_list.index('nominacion') - 1
                            nominaciones.append(int(nominaciones_list[nominaciones_index]))
                    else:
                        nominaciones.append(0)
                except:
                    nominaciones.append(0)

                try:
                    script = soup.find('script', type='application/ld+json').string
                except:
                    pass

                data = json.loads(script)

                try:
                    fecha.append(data['datePublished'])
                except:
                    # Revision
                    # np.nan
                    fecha.append('Sin datos')

                try:
                    sinopsis.append(data['description'])
                except:
                    # Revision
                    # np.nan
                    sinopsis.append('Sin datos')

                try:
                    idioma_original.append(data['review']['inLanguage'])
                except:
                    # Revision
                    # np.nan
                    idioma_original.append('Sin datos')

                try:
                    rating.append(data['aggregateRating']['ratingValue'])
                except:
                    rating.append(0)

                try:
                    ratingCount.append(data['aggregateRating']['ratingCount'])
                except:
                    ratingCount.append(0)

                try:
                    genero.append(data['genre']) 
                except:
                    # Revision
                    # np.nan
                    genero.append('Sin datos')

                try:
                    director.append([director['name'] for director in data['director']])
                except:
                    # Revision
                    # np.nan
                    director.append('Sin datos')

                busqueda_input.append(busqueda)

                try:
                    clasificasion.append(data['contentRating'])
                except:
                    # Revision
                    # np.nan
                    clasificasion.append('Sin datos')  

                try:
                    url_trailer.append(data['trailer']['embedUrl'])
                except:
                    # Revision
                    # np.nan
                    url_trailer.append('Sin datos')

                try:
                    actores.append([actor['name'] for actor in data['actor']])
                except:
                    # Revision
                    # np.nan
                    actores.append('Sin datos')

                reviews = soup.select('ul[data-testid="reviewContent-all-reviews"] li')
                has_user_review = False
                has_critic_review = False

                for review in reviews:
                    label = review.select_one('.label').text.strip()
                    score = review.select_one('.score').text.strip()

                    if label == "Reseñas de usuarios":
                        resena_user.append(score)
                        has_user_review = True

                    elif label == "Reseñas de críticos":
                        resena_critic.append(score)
                        has_critic_review = True

                if not has_user_review:
                    resena_user.append(0)

                if not has_critic_review:
                    resena_critic.append(0)

            # CONVERTIR STRING DE RESEÑAS EN NÚMERO

            for i in range(len(resena_user)):
                try:
                    if resena_user[i][-1] == 'K':
                        resena_user[i] = float(resena_user[i][:-1]) * 1000
                    elif resena_user[i][-1] == 'M':
                        resena_user[i] = float(resena_user[i][:-1]) * 1000000
                    elif resena_user[i] == 'Sin datos':
                        resena_user[i] = 0
                    else:
                        resena_user[i] = float(resena_user[i])
                except TypeError:
                    pass


            # CREACIÓN DEL DATAFRAME                          
            data_pelis = pd.DataFrame()

            data_pelis['Título'] = titulos #str
            data_pelis['Busqueda'] = busqueda_input #str
            data_pelis['Fecha'] = fecha #datetime
            data_pelis['Género'] = genero #str
            data_pelis['Director'] = director #str
            data_pelis['Reparto'] = actores #str
            data_pelis['Sinopsis'] = sinopsis #str
            data_pelis['Duración'] = duracion #int
            data_pelis['Idioma original'] = idioma_original #str
            data_pelis['Rating'] = rating #float
            data_pelis['Votos rating'] = ratingCount #int
            data_pelis['URL Trailer'] = url_trailer #float
            data_pelis['Clasificación'] = clasificasion #str
            data_pelis['Reseñas Usuarios'] = resena_user #int
            data_pelis['Reseñas Críticos'] = resena_critic #int
            data_pelis['Premios'] = premios
            data_pelis['Nominaciones'] = nominaciones

            # NORMALIZACIÓN DE COLUMNAS NUMÉRICAS

            data_pelis['Duración'] = data_pelis['Duración'].apply(float)
            data_pelis['Rating'] = data_pelis['Rating'].apply(float)
            data_pelis['Votos rating'] = data_pelis['Votos rating'].apply(float)
            data_pelis['Clasificación'] = data_pelis['Clasificación'].apply(str)
            data_pelis['Reseñas Críticos'] = data_pelis['Reseñas Críticos'].apply(float)
            data_pelis['Premios'] = data_pelis['Premios'].apply(float)
            data_pelis['Nominaciones'] = data_pelis['Nominaciones'].apply(float)


            ###### BUCLE PARA CREAR EL JSON A PARTIR DEL DATAFRAME ######

            #### INSERTA EL DF EN AIRTABLE
            if insertardf(data_pelis , BASE_ID, TABLE_ID, API_KEY):
                print("Exito")
                ban = 1
            else:
                print("Fallo")        
            browser.quit()
        else:
            st.warning('La palabra clave ya existe en nuestra Base de Datos, procedemos a las gráficas sin hacer scraping')                        
            ban = 1                        
    
    if ban == 1:
        if opt == 1:
            busqueda = busqueda1  
        data_from_airtable = pd.DataFrame(airtable_to_dataframe(BASE_ID, TABLE_ID, API_KEY))
        select = busqueda.lower()
        #st.warning(f"La palabra seleccionada fue: {select}") 
        dfselec = data_from_airtable[data_from_airtable["Busqueda"].str.lower() == select ]        
        with st.expander(label = f"DataFrame - Peliculas por {select}", expanded = False):            
            st.dataframe(dfselec)

        ####Gráficas
        #-----Gráfico 1. Duración / cantidad pelis
        try:
            fig, ax = plt.subplots(figsize=(8, 4))
            dfselec_duracion = dfselec[dfselec['Duración'] != 0]
            sns.histplot(data=dfselec_duracion, x='Duración', kde=True, bins=30, color='purple', ax=ax)
            # Configurar ejes y título
            ax.set_xlabel('Duración (minutos)', fontsize=12)
            ax.set_ylabel('Número de películas', fontsize=12)
            ax.set_title(f'Distribución de duración de películas por {select}', fontsize=14)            
            st.pyplot(fig)
        except:
            pass

        #-----Gráfico 2. Duración / rating
        try:  
            dfselec_dur_2 = dfselec[dfselec['Duración'] != 0]
            plt.scatter(dfselec_dur_2['Duración'], dfselec_dur_2['Rating'])
            plt.xlabel('Duración')
            plt.ylabel('Rating')
            plt.title(f'Relación entre el rating y la duración de películas {select}')
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 3. Reseñas usuarios / críticos

        # Filtra las películas que tienen críticas de usuarios y críticos
        try:
            df_critica = dfselec[dfselec['Reseñas Usuarios'].notnull() & dfselec['Reseñas Críticos'].notnull()]
            df_critica = df_critica.replace('Sin datos', pd.NaT)
            # Elimina las filas que contienen NaN
            df_critica = df_critica.dropna()
            # Agrupa las películas por clasificación y calcula el promedio de rating y críticas de usuarios y críticos
            grouped = df_critica.groupby('Clasificación').agg({'Rating': 'mean', 'Reseñas Usuarios': 'mean', 'Reseñas Críticos': 'mean'})
            # Grafica las barras para las críticas de usuarios y críticos por clasificación
            grouped[['Reseñas Usuarios', 'Reseñas Críticos']].plot(kind='bar', stacked=True)
            #plt.show()
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 4. Idioma
        try:
            dfselec_idioma = dfselec["Idioma original"].value_counts()
            sns.barplot(y =  dfselec_idioma, x = dfselec_idioma.index)
            plt.title(f'Relación de idiomas originales de las peliculas con {select}')
            #plt.show()
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 5. Géneros
        try:
            rr = []
            temm = [ x for x in dfselec["Género"] ]
            for x in temm:
                tt = str(x).split(",")
                for y in tt:
                    rr.append(y.strip())    
            serie = pd.Series(rr)
            serie.value_counts()
            sns.barplot(y =  serie, x = serie.index)
            plt.title(f'Relación de Géneros de peliculas con {select}')
            #plt.show()
            st.pyplot(plt)
        except:
            pass


        #-----Gráfico 6. Top 20 nominaciones
        try:
            dfselec_nomi = dfselec[dfselec["Nominaciones"] > 0][["Título","Nominaciones"]]
            top20 = dfselec_nomi.nlargest(20, "Nominaciones") # Obtener top 20 películas
            sns.barplot(y = "Título", x = "Nominaciones", data = top20)
            plt.title(f'Top 20 de películas por número de nominaciones con {select}')
            #plt.show()
            st.pyplot(plt)
        except:
            pass


        #-----Gráfico 7. Top 20 directores
        try:
            dfselec_copy_dir = dfselec.copy()
            dfselec_copy_dir['Director'] = dfselec_copy_dir['Director'].str.split(', ')
            dfselec_copy_dir = dfselec_copy_dir.dropna(subset=['Director'])
            directores_unicos = set()
            for lista_directores in dfselec_copy_dir['Director']:
                for director in lista_directores:
                    directores_unicos.add(director)
            # Crear un diccionario para contar el número de películas dirigidas por cada director
            peliculas_por_director = {}
            for director in directores_unicos:
                peliculas_por_director[director] = 0
            for lista_directores in dfselec_copy_dir['Director']:
                for director in lista_directores:
                    peliculas_por_director[director] += 1
            # Crear una lista de pares (director, número de películas) ordenada por el número de películas
            peliculas_por_director = [(k, v) for k, v in peliculas_por_director.items()]
            peliculas_por_director.sort(key=lambda x: x[1], reverse=True)
            # Tomar los 20 primeros directores (mayor número de películas dirigidas)
            top_directores = peliculas_por_director[:20]
            nombres_directores = [x[0] for x in top_directores]
            num_peliculas = [x[1] for x in top_directores]
            # Graficar los resultados usando Matplotlib
            plt.figure(figsize=(10, 10))
            plt.pie(num_peliculas, labels=nombres_directores)
            plt.title(f'Top 20 directores por número de películas dirigidas con {select}')
            #plt.show()
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 8. Películas por género
        try:
            
            dfselec_copy_genre = dfselec.copy()
            
            dfselec_copy_genre['Género'] = dfselec_copy_genre['Género'].fillna('')
            dfselec_copy_genre['Género'] = dfselec_copy_genre['Género'].apply(lambda x: x.split(', '))
            dfselec_copy_genre = dfselec_copy_genre.explode('Género')

            sns.countplot(x='Género', data=dfselec_copy_genre)
            plt.xticks(rotation=90)
            plt.title("Número de películas por género")
            #plt.show()
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 9. Correlación variables numéricas
        try:
            corr = dfselec.corr()
            sns.heatmap(corr, annot=True, cmap="inferno")
            plt.title("Correlación entre variables numéricas")
            #plt.show()
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 10. Conteo películas por clasificación
        try:
            sns.countplot(x="Clasificación", data=dfselec)
            plt.xticks(rotation=90)
            plt.title("Conteo de películas por clasificación")
            #plt.show()
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 11. Premios por género
        try:
            # Reemplazar los valores nulos por una cadena vacía en la columna "Género"
            dfselec["Género"].fillna("", inplace=True)

            # Crear una nueva columna con el género más frecuente para cada película
            dfselec["genre"] = dfselec["Género"].str.split(",").apply(lambda x: max(set(x), key=x.count))

            # Seleccionar los 10 géneros más comunes
            top_genres = dfselec["genre"].value_counts()[:10].index.tolist()

            # Crear un nuevo DataFrame con las películas que pertenecen a los géneros más comunes
            df_top_genres = dfselec[dfselec["genre"].isin(top_genres)]

            # Eliminar espacios en blanco al principio y al final de los géneros
            df_top_genres["genre"] = df_top_genres["genre"].str.strip()

            # Agrupar por género y sumar los premios
            top_genres_awards = df_top_genres.groupby("genre")[["Premios"]].sum()

            # Crear un gráfico de barras
            sns.barplot(x=top_genres_awards.index, y="Premios", data=top_genres_awards)
            plt.xticks(rotation=90)
            plt.xlabel("Género")
            plt.title("Películas con más premios ganados por género")
            #plt.show()
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 12. Top 10 género / rating
        try:
            df_top_genres["genre"] = df_top_genres["genre"].str.replace(" ","")
            fig = px.bar(df_top_genres, x="genre", y="Rating", color="Premios",
                        title="Top 10 Géneros por Rating",
                        labels={"genre": "Género", "Rating": "Rating", "Año": "Año"},
                        hover_data=["Título", "genre", "Rating"])
            #fig.show()
            st.pyplot(fig)
        except:
            pass

        #-----Gráfico 13. Distribución reseñas usuarios / género
        try:
            top_genres = dfselec["Género"].str.split(",", expand=True).stack().value_counts()[:10].index.tolist()
            df_top_genres = dfselec[dfselec["Género"].str.split(",", expand=True).isin(top_genres).any(axis=1)]
            df_top_genres.loc[:, "Género"] = df_top_genres["Género"].str.strip().str.split(",", expand=True)[0]
            df_filtered = df_top_genres[df_top_genres['Reseñas Usuarios'] != 0]

            fig = px.pie(df_filtered, values='Reseñas Usuarios', names='Género', 
                        title="Distribución de Reseñas de Usuarios por Género",
                        labels={"Género": "Género", "Reseñas Usuarios": "Reseñas de Usuarios"}, 
                        hover_data={'Título': True},
                        custom_data=['Título'])

            fig.update_traces(hovertemplate='<b>%{label}</b><br>Reseñas: %{value}')

            #fig.show()
            st.pyplot(fig)
        except:
            pass


        #-----Gráfico 14. Pairplot
        sns.pairplot(dfselec, hue = "Nominaciones")
        #plt.show()
        st.pyplot(plt)

if __name__ == "__main__":
    main()