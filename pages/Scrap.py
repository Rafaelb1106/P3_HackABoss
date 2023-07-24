import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from pprint import pprint
import json
import re
import plotly as plt
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import random
from airtable import Airtable
import sys
import plotly.graph_objects as go


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
        for i in range(len(dft)):
            info = dft.iloc[i]
            dicc = {}         
            for camp in L_campos:
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

def listarDFtabla(BD, tabla, apikey):
    
    try:
        res = {}
        
        airtable_base_url = "https://api.airtable.com/v0"
        
        headers = {"Authorization" : f"Bearer {apikey}",
                   "Content-Type"  : "application/json"}
        
        endpoint = f"{airtable_base_url}/{BD}/{tabla}"
        
        params = {"fields"                : None, 
                  "maxRecords"            : None, 
                  "pageSize"              : None,
                  "returnFieldsByFieldId" : False}
        
        response = requests.get(url = endpoint, headers = headers, params = params)
        
        if response.status_code != 200:
            return res
        
        else:            
            return response.json()    
        
    except:
        return res
    
def creardfcontabla(info):
    dic_res1 = dic_res["records"]
    
    l_columns = list(dic_res1[0]["fields"].keys())
    
    df_listado = pd.DataFrame(columns = l_columns)
    
    warnings.filterwarnings('ignore')
    
    for x in range(0, len(dic_res1)):
        
        df_listado = df_listado.append(dic_res1[x]["fields"], ignore_index = True)
        
    return df_listado

##--##--##
def airtable_to_dataframe(BASE_ID, TABLE_ID, API_KEY):

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
    st.title("Web Scraping con Beautifulsoup")
    st.write("""
    Esta app ofrece una aplicación dinámica y potente para los amantes del cine que buscan análisis basados en datos de sus películas favoritas. Construido en Streamlit, 
    el sistema opera en dos modos complementarios para proporcionar visualizaciones de datos enriquecidas y personalizadas.
    
    El primer modo de funcionamiento permite al usuario ingresar una palabra clave y seleccionar un número de registros a obtener. 
    La aplicación, utilizando técnicas de web scraping, busca en tiempo real las películas relacionadas con esa búsqueda y presenta los resultados. 
    Con estos datos, se generan visualizaciones de datos interactivas que permiten al usuario explorar las tendencias y características de las películas seleccionadas.
    
    El segundo modo aprovecha nuestra extensa base de datos, la cual se encuentra alojada en Airtable, previamente construida con información recolectada por web scraping. Si el usuario selecciona una palabra clave de esta base de datos, 
    la aplicación recupera los datos y genera las visualizaciones de inmediato, sin necesidad de realizar un nuevo web scraping.
    
    Una característica inteligente de la aplicación es que, si el usuario ingresa una palabra clave en el primer modo de funcionamiento que ya existe en nuestra base de datos, 
    la aplicación cambiará automáticamente al segundo modo, mostrando los gráficos generados previamente. Esto optimiza la eficiencia y la velocidad de nuestras visualizaciones, 
    permitiendo a los usuarios acceder rápidamente a la información que buscan.

    ¿Cómo funciona?
    
    Si elige la opción 1:
    
    - Primer input: ingrese la palabra clave y haga submit
    
    - Segundo input: ingrese el número de registros y haga submit
    
    - Espere por favor

    Le rogamos paciencia, el proceso puede demorar unos segundos debido a la gran cantidad de datos a manejar, gracias.
    """)
    ttt = True
    numero = 1
    ban = 0 
    ban111 = 0
    opt = 0       
    airtable = Airtable(BASE_ID, TABLE_ID, API_KEY)
    boton1 = False
    menu_bus = []
    data_from_airtable = pd.DataFrame(airtable_to_dataframe(BASE_ID, TABLE_ID, API_KEY))    
    menu_bus = list(set(data_from_airtable["Busqueda"]))    
    col1, col2 = st.columns(2)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("1. Ingrese la palabra clave para explorar los datos de las películas mediante web scraping.")
    col1, col2 = st.columns(2)
    with col1:        
        busqueda = st.text_input(label="Busqueda", max_chars = 20, placeholder="Nombre Pelicula", label_visibility="collapsed")
    with col2:
        boton1 = st.button(label="Buscar", key="B1")
    ######
    if boton1:
        ttt = False
        headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                    }
        url = f"https://www.imdb.com/search/title/?title={busqueda.lower()}&count=25"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")                        
        sleep(2)
        divcant = soup.find('div', class_='desc')
        cant = divcant.find('span').text
        patron = r"\d+"
        coincidencias = re.findall(patron, cant)
        if coincidencias:
            numero = int(coincidencias[-1])            
        else:
            st.warning(f"No hay Concidencias en la busqueda")
            sys.exit()        
    st.write(f"2. Seleccione la cantidad máxima de registro a procesar donde el máximo valor que puede tomar es: {numero} Y presione buscar")
    texto1= "<p style='font-size: small;'>Tenga en cuenta que entre más registros a consultar, más lento es el proceso y no se debe superar el límite indicado.</p>"
    st.write(texto1, unsafe_allow_html=True)
    col111, col222 = st.columns(2)
    with col111:
        NumReg = st.number_input(label = "Cantidad de Registros", step= 1, label_visibility="collapsed",disabled=ttt)
    with col222:
        boton111 = st.button(label="Buscar", key="B11",disabled=ttt)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("Seleccione una búsqueda ya realizada para ver sus gráficas. En esta opción no se hace scraping")
    col11, col22 = st.columns(2)
    with col11:        
        busqueda1 = st.selectbox("Anteriores_Busquedas", options = menu_bus, label_visibility="collapsed")
    with col22:
        if st.button(label="Buscar", key="B3"):
            ban = 1
            opt = 1
    st.markdown("<hr>", unsafe_allow_html=True)
    texto2 = "Lamentablemente, debido a las restricciones de ejecución en el entorno de Streamlit Sharing, no es posible utilizar Selenium WebDriver para automatizar acciones en un navegador web. Esto significa que no se puede ejecutar el código que involucra la apertura de un navegador y realizar tareas como web scraping. En consecuencia, se utiliza Beautifulsoup para analizar el HTML. Se posee la opción de automatizar el navegador, pero solo se puede ejecutar en un entorno local"
    es_texto2 = st.empty()
    es_texto2.write(texto2)
    if boton111:        

        records = airtable.get_all(formula = f"FIND('{busqueda.lower()}', LOWER({{Busqueda}}))")
        # INPUT DE BÚSQUEDA
        if len(records) == 0:
            try:
                sleep(2)
                headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                            }
                url = f"https://www.imdb.com/search/title/?title={busqueda.lower()}&count={NumReg}"
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")                
                sleep(2)
                # Obtener los resultados de la búsqueda               
                lista_pelis = soup.find_all('h3', class_='lister-item-header')

                urls_pelis = []

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
                    headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                            }
              
                    try:
                        response = requests.get(i, headers=headers)
                        # Revision
                        sleep(3)
                        #html = browser.page_source
                        soup = BeautifulSoup(response.text, "html.parser")
                    except:
                        pass
                # EXTRACCIÓN DE DATOS DE CADA PÁGINA
                    try:
                        titulos.append(soup.find('h1').text)
                    except:

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
                        fecha.append('Sin datos')

                    try:
                        sinopsis.append(data['description'])
                    except:
                        sinopsis.append('Sin datos')

                    try:
                        idioma_original.append(data['review']['inLanguage'])
                    except:
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
                        genero.append('Sin datos')

                    try:
                        director.append([director['name'] for director in data['director']])
                    except:
                        director.append('Sin datos')

                    busqueda_input.append(busqueda)

                    try:
                        clasificasion.append(data['contentRating'])
                    except:
                        clasificasion.append('Sin datos')  

                    try:
                        url_trailer.append(data['trailer']['embedUrl'])
                    except:
                        url_trailer.append('Sin datos')

                    try:
                        actores.append([actor['name'] for actor in data['actor']])
                    except:
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
                
            
            except Exception as e:
                st.warning(f"Error: {str(e)}")
        else:
            st.warning('La palabra clave ya existe en nuestra Base de Datos, procedemos a las gráficas sin hacer scraping')                        
            ban = 1                        
    
    if ban == 1:
        es_texto2.empty()
        if opt == 1:
            busqueda = busqueda1  
        data_from_airtable = pd.DataFrame(airtable_to_dataframe(BASE_ID, TABLE_ID, API_KEY))
        select = busqueda.lower()
        #st.warning(f"La palabra seleccionada fue: {select}") 
        dfselec = data_from_airtable[data_from_airtable["Busqueda"].str.lower() == select ]        
        with st.expander(label = f"DataFrame - Peliculas por {select}", expanded = False):            
            st.dataframe(dfselec)

        ####Gráficas
        #### con ploty
        
        try:
            dfselec_copy_genre = dfselec.copy()            
            dfselec_copy_genre['Género'] = dfselec_copy_genre['Género'].fillna('')
            dfselec_copy_genre['Género'] = dfselec_copy_genre['Género'].apply(lambda x: x.split(', '))
            dfselec_copy_genre = dfselec_copy_genre.explode('Género')
            dfselec_copy_genre = dfselec_copy_genre.groupby(by = "Género", as_index = True)["Género"].count()            
            fig_pie = px.pie(data_frame = dfselec_copy_genre,
                     names      = dfselec_copy_genre.index,
                     values     = "Género",
                     title      = f'Número de películas por género con {select}')
            st.plotly_chart(figure_or_data = fig_pie, use_container_width = True)
        except:
            pass
        
        
        
        try:
            dfselec_duracion = dfselec.copy()
            dfselec_duracion = dfselec_duracion[dfselec_duracion['Duración'] > 10]
            dfselec_duracion = dfselec_duracion.groupby(by=["Duración"])["id"].count().reset_index()
            dfselec_duracion = dfselec_duracion.rename(columns={'id': 'Cantidad'})
    
            fig_bar = px.bar(data_frame=dfselec_duracion,
                             x="Duración",
                             y="Cantidad",
                             title=f'Distribución de duración de películas con {select}')
    
            st.plotly_chart(figure_or_data=fig_bar, use_container_width=True)

        except:
            pass
                   
        #-----Gráfico 1. Duración / cantidad pelis
        try:
            fig, ax = plt.subplots(figsize=(8, 4))
            dfselec_duracion = dfselec.copy()
            dfselec_duracion = dfselec[dfselec['Duración'] != 0]
            sns.histplot(data=dfselec_duracion, x='Duración', kde=True, bins=30, color='purple', ax=ax)
    
            ax.set_xlabel('Duración (minutos)', fontsize=12)
            ax.set_ylabel('Número de películas', fontsize=12)
            ax.set_title(f'Distribución de duración de películas por {select}', fontsize=14)
    
            st.pyplot(fig)
    
            fig_plotly = go.Figure(data=[go.Histogram(x=dfselec_duracion['Duración'], nbinsx=30)])

            fig_plotly.update_layout(
            title=f'Distribución de duración de películas por {select}',
            xaxis_title='Duración (minutos)',
            yaxis_title='Número de películas'
            )
           
            st.plotly_chart(fig_plotly)

        except:
            pass

        #-----Gráfico 2. Duración / rating
        try:  
            plt.clf()
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
            plt.clf()
            df_critica = dfselec[dfselec['Reseñas Usuarios'].notnull() & dfselec['Reseñas Críticos'].notnull()]
            df_critica = df_critica.replace('Sin datos', pd.NaT)
            # Elimina las filas que contienen NaN
            df_critica = df_critica.dropna()
            # Agrupa las películas por clasificación y calcula el promedio de rating y críticas de usuarios y críticos
            grouped = df_critica.groupby('Clasificación').agg({'Rating': 'mean', 'Reseñas Usuarios': 'mean', 'Reseñas Críticos': 'mean'})
            # Grafica las barras para las críticas de usuarios y críticos por clasificación
            grouped[['Reseñas Usuarios', 'Reseñas Críticos']].plot(kind='bar', stacked=True)
            st.pyplot(plt.gcf())
        except:
            pass

        #-----Gráfico 4. Idioma
        try:
            plt.clf()
            #fig, ax = plt.subplots(figsize=(8, 4))
            dfselec_idioma = dfselec["Idioma original"].value_counts()
            sns.barplot(y =  dfselec_idioma, x = dfselec_idioma.index)
            plt.title(f'Relación de idiomas originales de las peliculas con {select}')
            #ax.set_title(f'Relación de idiomas originales de las peliculas con {select}')
            #plt.show()            
            #st.pyplot(fig)
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 5. Géneros
        try:
            plt.clf()
            rr = []
            temm = [x for x in dfselec["Género"]]
            for x in temm:
                tt = str(x).split(",")
                for y in tt:
                    rr.append(y.strip())
            serie = pd.Series(rr)
            counts = serie.value_counts()
            sns.barplot(y=counts.index, x=counts)
            plt.title(f'Relación de Géneros de películas con {select}')
    
            st.pyplot(plt.gcf())

        except: 
            pass


        #-----Gráfico 6. Top 20 nominaciones
        try:
            plt.clf()
            dfselec_nomi = dfselec[dfselec["Nominaciones"] > 0][["Título", "Nominaciones"]]
            top20 = dfselec_nomi.nlargest(20, "Nominaciones")  # Obtener top 20 películas
            sns.barplot(y="Título", x="Nominaciones", data=top20)
            plt.title(f'Top 20 de películas por número de nominaciones con {select}')
    
            st.pyplot(plt.gcf())

        except:
            pass


        #-----Gráfico 7. Top 20 directores
        try:
            plt.clf()
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
            st.pyplot(plt)
        except:
            pass


        #-----Gráfico 8. Películas por género
        try:
            plt.clf()
            dfselec_copy_genre = dfselec.copy()
            
            dfselec_copy_genre['Género'] = dfselec_copy_genre['Género'].fillna('')
            dfselec_copy_genre['Género'] = dfselec_copy_genre['Género'].apply(lambda x: x.split(', '))
            dfselec_copy_genre = dfselec_copy_genre.explode('Género')

            sns.countplot(x='Género', data=dfselec_copy_genre)
            plt.xticks(rotation=90)
            plt.title("Número de películas por género")
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 9. Correlación variables numéricas
        try:
            plt.clf()
            corr = dfselec.corr()
            sns.heatmap(corr, annot=True, cmap="inferno")
            plt.title("Correlación entre variables numéricas")
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 10. Conteo películas por clasificación
        try:
            plt.clf()
            sns.countplot(x="Clasificación", data=dfselec)
            plt.xticks(rotation=90)
            plt.title("Conteo de películas por clasificación")
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 11. Premios por género
        try:
            plt.clf()
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
            st.pyplot(plt)
        except:
            pass

        #-----Gráfico 12. Top 10 género / rating
        try:
            plt.clf()
            df_top_genres["genre"] = df_top_genres["genre"].str.replace(" ","")
            fig = px.bar(df_top_genres, x="genre", y="Rating", color="Premios",
                        title="Top 10 Géneros por Rating",
                        labels={"genre": "Género", "Rating": "Rating", "Año": "Año"},
                        hover_data=["Título", "genre", "Rating"])
            st.pyplot(fig)
        except:
            pass

        #-----Gráfico 13. Distribución reseñas usuarios / género
        try:
            plt.clf()
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

            st.pyplot(fig)
        except:
            pass


        #-----Gráfico 14. Pairplot
        try:
            plt.clf()
            sns.pairplot(dfselec, hue = "Nominaciones")
            plt.suptitle(f'Matriz de gráficos de dispersión con Nominaciones de: {select}')
            st.pyplot(plt)
        except:
            pass
if __name__     == "__main__":
    main()
