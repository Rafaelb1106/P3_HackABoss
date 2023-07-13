import matplotlib.pyplot as plt
import seaborn as sns
import squarify
from PIL import Image
from wordcloud import WordCloud
import plotly.express as px
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def intro():
    st.header("Gráficos recomendador de cervezas")
    st.write("""
    A continuación de muestran una serie de gráficos que relacionan diversas variables de la base de datos
    
    """)

# Función para obtener los 25 estilos de cerveza más comunes en el conjunto de datos
def get_top_25_beer_styles(df_Beer):
    # Contar cuántas veces aparece cada tipo de cerveza y devolver los 25 primeros
    return df_Beer['beer/style'].value_counts().head(25).index
    
# Función para crear un gráfico de barras con los 25 tipos de cerveza más comunes
def plot_most_common_beer_bar(df_Beer):
    # Contar cuántas veces aparece cada tipo de cerveza y seleccionar los 25 primeros
    beer_counts = df_Beer['beer/style'].value_counts().nlargest(25)
    
    # Crear la figura del gráfico de barras
    fig = go.Figure(data=[go.Bar(
        x=beer_counts.values,
        y=beer_counts.index,
        orientation='h'
    )])
    fig.update_layout(
        title="25 tipos de cerveza más comunes",
        xaxis_title="Tipo de cerveza",
        yaxis_title="Cantidad",
        template='plotly_white'
    )
    st.plotly_chart(fig) 
        
    
# Función para crear un gráfico de treemap con los 25 tipos de cerveza más comunes
      
def plot_most_common_beer_treemap(df_Beer):
    # Contar cuántas veces aparece cada tipo de cerveza y seleccionar los 25 primeros
    beer_counts = df_Beer['beer/style'].value_counts().nlargest(25).reset_index()
    beer_counts.columns = ['Beer Style', 'Count']
        
    # Crear el gráfico de treemap interactivo con plotly
    fig = px.treemap(beer_counts, path=['Beer Style'], values='Count', title='Distribución de las 25 cervezas más comunes por tipo (Treemap)')
    fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))
        
    # Mostrar el gráfico interactivo en Streamlit
    st.plotly_chart(fig)
    
# Función para crear un gráfico de barras con las 10 cervezas más revisadas
def plot_most_reviewed_beers(df_Beer):
    # Contar cuántas veces aparece cada nombre de cerveza y seleccionar los 10 primeros
    top_beers = df_Beer['beer/name'].value_counts().head(10)
        
    # Crear la figura del gráfico circular
    fig = go.Figure(data=[go.Pie(labels=top_beers.index, values=top_beers.values)])
        
    # Configurar el diseño del gráfico
    fig.update_layout(
        title='Las 10 cervezas más revisadas',
        height=600,
        width=800,
    )
        
    # Mostrar el gráfico interactivo
    st.plotly_chart(fig)
    ax.set_title("Nube de palabras de nombres de cervezas")
    
# Función para crear un histograma con la distribución de los sentimientos
def plot_sentiment_distribution(df_Beer):
    # Crear el histograma interactivo con plotly
    fig = go.Figure(data=[go.Histogram(x=df_Beer['sentiment'].dropna(), nbinsx=30)])
    fig.update_layout(title='Distribución de los sentimientos',
                        xaxis_title='Sentimiento',
                        yaxis_title='Frecuencia')
        
        # Mostrar el histograma interactivo
    st.plotly_chart(fig)
    
   # Función para crear un heatmap con la correlación entre las características de las reseñas
def plot_review_features_correlation(df_Beer):
    # Definir las características de la reseña que se van a correlacionar
    review_features = ['review/appearance', 'review/aroma', 'review/palate', 'review/taste']
    # Calcular la correlación entre estas características
    corr = df_Beer[review_features].corr()
    # Crear una nueva figura de tamaño 10x6
    fig, ax = plt.subplots(figsize=(10, 6))
    # Crear un heatmap de las correlaciones
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    # Título del gráfico
    ax.set_title('Correlación entre las características de las reseñas')
    # Mostrar el gráfico
    st.pyplot(fig)
    
    
# Función para crear un gráfico de burbujas con el sentimiento por estilo de cerveza
def plot_sentiment_beer_style_bubble(df_Beer):
    # Contar cuántas veces aparece cada combinación de estilo de cerveza y etiqueta de sentimiento
    sentiment_counts = df_Beer.groupby(['beer/style', 'sentiment_label']).size().reset_index(name='counts')
    # Crear una nueva columna 'review_count' que contenga la suma total de reseñas para cada combinación de estilo de cerveza y etiqueta de sentimiento
    sentiment_counts['review_count'] = sentiment_counts.groupby(['beer/style', 'sentiment_label'])['counts'].transform('sum')
    # Obtener los 25 estilos de cerveza más comunes
    top_25_beer_styles = get_top_25_beer_styles(df_Beer)
    # Filtrar el dataframe para incluir solo los 25 estilos de cerveza más comunes
    sentiment_counts_top_25 = sentiment_counts[sentiment_counts['beer/style'].isin(top_25_beer_styles)]
    # Crear un gráfico de burbujas con los estilos de cerveza en el eje x, las etiquetas de sentimiento en el eje y, el tamaño de las burbujas correspondiente al número de reseñas y el color de las burbujas correspondiente a la etiqueta de sentimiento
    fig = px.scatter(sentiment_counts_top_25, x='beer/style', y='sentiment_label', size='review_count', color='sentiment_label', hover_name='beer/style', title='Relación de sentimientos por Top 25 estilos de cerveza (bubble scatter plot)')
    # Actualizar las etiquetas de los ejes y el ángulo de las etiquetas del eje x
    fig.update_layout(xaxis_tickangle=-45, xaxis_title='Beer Style', yaxis_title='Sentiment')
    # Mostrar el gráfico
    st.plotly_chart(fig)
    
    
# Función para crear un boxplot con la distribución de ABV (alcohol por volumen) por estilo de cerveza
def plot_abv_beer_style_box(df_Beer):
    # Filtrar el dataframe para incluir solo los 25 estilos de cerveza más comunes
    top_25_beer_styles = df_Beer[df_Beer['beer/style'].isin(get_top_25_beer_styles(df_Beer))]
        
     # Filtrar los estilos de cerveza dentro del rango de ABV de 3.5 a 14
    filtered_beer_styles = top_25_beer_styles[(top_25_beer_styles['beer/ABV'] >= 3.5) & (top_25_beer_styles['beer/ABV'] <= 14)]
        
    # Crear el gráfico de caja interactivo con plotly
    fig = px.box(filtered_beer_styles, x='beer/style', y='beer/ABV', title='Distribución de ABV por estilo de cerveza')
        
    # Actualizar las etiquetas de los ejes y el ángulo de las etiquetas del eje x
    fig.update_layout(xaxis_tickangle=-45, xaxis_title='Estilo de cerveza', yaxis_title='ABV')
        
    # Mostrar el gráfico interactivo en Streamlit
    st.plotly_chart(fig)
    
def plot_3d_scatter_overall_palate_taste(df_Beer):
    # Gráfico de dispersión 3D de calificación general, paladar y sabor para los 10 estilos de cerveza más comunes
    top_10_beer_styles = df_Beer['beer/style'].value_counts().index[:10]
    df_top_10 = df_Beer[df_Beer['beer/style'].isin(top_10_beer_styles)]
    fig = px.scatter_3d(df_top_10, x='review/overall', y='review/palate', z='review/taste', color='beer/style')
    fig.update_layout(title='Relación entre Calificación General, Paladar y Sabor')
    # Mostrar el gráfico
    st.plotly_chart(fig)

# Función para crear una nube de palabras con los nombres de las cervezas

def plot_beer_wordcloud(df_Beer):
    # Contar cuántas veces aparece cada nombre de cerveza
    beer_counts = df_Beer['beer/name'].value_counts()
    # Cargar una máscara con la forma de una cerveza
    beer_mask = np.array(Image.open('/app/final/FinalPr/pages/recomend/images/beer.png'))
    # Crear una nube de palabras con la máscara de la cerveza y otras configuraciones
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100, mask=beer_mask, contour_width=3, contour_color='black')
    # Generar la nube de palabras a partir de las frecuencias de los nombres de las cervezas
    wordcloud.generate_from_frequencies(beer_counts)
    # Crear una nueva figura de tamaño 10x10
    fig, ax = plt.subplots(figsize=(10, 10))
    # Mostrar la nube de palabras
    ax.imshow(wordcloud, interpolation='bilinear')
    # Quitar los ejes
    ax.axis('off')
    # Asegurarse de que el gráfico se ajuste bien a la figura
    fig.tight_layout()
    # Mostrar el gráfico utilizando st.image()
    st.image(wordcloud.to_image())
