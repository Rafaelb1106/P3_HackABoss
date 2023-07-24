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
from pages.pages import recomend

img = './images/beer.png'
df_Beer = recomend.df_Beer

def main():
    def intro():
        st.title("Gráficos recomendador de cervezas")
        st.write("""
        A continuación se muestran una serie de gráficos que relacionan diversas variables de la base de datos.
        """)

    def get_top_25_beer_styles(df_Beer):
        return df_Beer['beer/style'].value_counts().head(25).index

    def plot_most_common_beer_bar(df_Beer):
        beer_counts = df_Beer['beer/style'].value_counts().nlargest(25)

        fig = go.Figure(data=[go.Bar(
            x=beer_counts.values,
            y=beer_counts.index,
            orientation='h'
        )])
        fig.update_layout(
            title="25 tipos de cerveza más comunes",
            xaxis_title="Cantidad",
            yaxis_title="Tipo de cerveza",
            template='plotly_white'
        )
        st.plotly_chart(fig)

    def plot_beer_wordcloud(df_Beer):
        beer_counts = df_Beer['beer/name'].value_counts()
        beer_mask = np.array(Image.open(img))
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100, mask=beer_mask, contour_width=3, contour_color='black')
        wordcloud.generate_from_frequencies(beer_counts)
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        fig.tight_layout()
        st.pyplot(fig)

    def plot_most_common_beer_treemap(df_Beer):
        beer_counts = df_Beer['beer/style'].value_counts().nlargest(25).reset_index()
        beer_counts.columns = ['Beer Style', 'Count']

        fig = px.treemap(beer_counts, path=['Beer Style'], values='Count', title='Distribución de las 25 cervezas más comunes por tipo (Treemap)')
        fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))

        st.plotly_chart(fig)

    def plot_most_reviewed_beers(df_Beer):
        top_beers = df_Beer['beer/name'].value_counts().head(10)

        fig = go.Figure(data=[go.Pie(labels=top_beers.index, values=top_beers.values)])

        fig.update_layout(
            title='Las 10 cervezas más revisadas',
            height=600,
            width=800,
        )

        st.plotly_chart(fig)
        plt.title("Nube de palabras de nombres de cervezas")

    def plot_sentiment_distribution(df_Beer):
        fig = go.Figure(data=[go.Histogram(x=df_Beer['sentiment'].dropna(), nbinsx=30)])
        fig.update_layout(title='Distribución de los sentimientos',
                            xaxis_title='Sentimiento',
                            yaxis_title='Frecuencia')

        st.plotly_chart(fig)

    def plot_review_features_correlation(df_Beer):
        review_features = ['review/appearance', 'review/aroma', 'review/palate', 'review/taste']
        corr = df_Beer[review_features].corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Correlación entre las características de las reseñas')
        st.pyplot(fig)

    def plot_sentiment_beer_style_bubble(df_Beer):
        sentiment_counts = df_Beer.groupby(['beer/style', 'sentiment_label']).size().reset_index(name='counts')
        sentiment_counts['review_count'] = sentiment_counts.groupby(['beer/style', 'sentiment_label'])['counts'].transform('sum')
        top_25_beer_styles = get_top_25_beer_styles(df_Beer)
        sentiment_counts_top_25 = sentiment_counts[sentiment_counts['beer/style'].isin(top_25_beer_styles)]
        fig = px.scatter(sentiment_counts_top_25, x='beer/style', y='sentiment_label', size='review_count', color='sentiment_label', hover_name='beer/style', title='Relación de sentimientos por Top 25 estilos de cerveza (bubble scatter plot)')
        fig.update_layout(xaxis_tickangle=-45, xaxis_title='Beer Style', yaxis_title='Sentiment')
        st.plotly_chart(fig)

    def plot_abv_beer_style_box(df_Beer):
        top_25_beer_styles = df_Beer[df_Beer['beer/style'].isin(get_top_25_beer_styles(df_Beer))]

        filtered_beer_styles = top_25_beer_styles[(top_25_beer_styles['beer/ABV'] >= 3.5) & (top_25_beer_styles['beer/ABV'] <= 14)]

        fig = px.box(filtered_beer_styles, x='beer/style', y='beer/ABV', title='Distribución de ABV por estilo de cerveza')

        fig.update_layout(xaxis_tickangle=-45, xaxis_title='Estilo de cerveza', yaxis_title='ABV')

        st.plotly_chart(fig)

    def plot_3d_scatter_aroma_palate_abv(df_Beer):
        top_10_beer_styles = df_Beer['beer/style'].value_counts().index[:10]
        df_top_10 = df_Beer[df_Beer['beer/style'].isin(top_10_beer_styles)]
    
        fig = px.scatter_3d(df_top_10, x='review/aroma', y='review/palate', z='beer/ABV', color='beer/style',
                            range_z=[2, 20])
        fig.update_layout(title='Relación entre Aroma, Palate y Contenido de Alcohol por Volumen')
    
        st.plotly_chart(fig)

    intro()
    plot_most_common_beer_bar(df_Beer)
    plot_most_common_beer_treemap(df_Beer)
    plot_most_reviewed_beers(df_Beer)
    plot_sentiment_distribution(df_Beer)
    plot_review_features_correlation(df_Beer)
    plot_sentiment_beer_style_bubble(df_Beer)
    plot_abv_beer_style_box(df_Beer)
    plot_3d_scatter_aroma_palate_abv(df_Beer)
    plot_beer_wordcloud(df_Beer)

if __name__ == "__main__":
    main()
    
