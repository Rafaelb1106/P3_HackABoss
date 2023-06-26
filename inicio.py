import streamlit as st
import numpy as np
import pandas as pd
import requests
from PIL import Image

def main():
    st.title("Proyecto de Data Science")
    image = Image.open("img/hackaboss.png")
    st.image(image = image, use_column_width = True)
       
    st.markdown("""
            
                En este apasionante proyecto, nos proponemos aplicar los conocimientos adquiridos durante el bootcamp de Hack a Boss y llevarlos un paso más allá. No nos conformamos con simplemente dominar las bases, sino que también nos movemos por la curiosidad y el deseo de explorar nuevas formas de presentar y compartir el conocimiento en el amplio campo de Python.
                
                \n\nNuestra meta es construir una aplicación interactiva que abarque múltiples áreas temáticas relacionadas con lo aprendido en Python. Para lograr una mejor organización y facilidad de navegación, hemos decidido dividir el contenido en diferentes páginas o pestañas independientes. 

                \n\nCada página será un espacio dedicado a un tema específico, donde exploraremos conceptos clave, algoritmos avanzados y aplicaciones prácticas. A través de ejemplos claros y explicaciones concisas, nos esforzaremos por transmitir la esencia de cada concepto, brindando una experiencia de aprendizaje enriquecedora.

                \n\nAdemás de abordar los aspectos fundamentales, nos aventuraremos más allá de lo enseñado en el bootcamp. Nos sumergiremos en la investigación y la búsqueda de nuevas formas de aplicar los conocimientos adquiridos. Exploraremos bibliotecas, técnicas y recursos adicionales para enriquecer aún más nuestra comprensión y habilidades en el fascinante mundo de Python.

                \n\nEste proyecto representa una oportunidad para destacarnos y consolidar nuestro dominio en el ámbito de la programación y la ciencia de datos. Nos retamos a nosotros mismos para superar los límites de lo conocido y seguir expandiendo nuestros horizontes en este apasionante viaje de descubrimiento.

                \n\nA través de esta aplicación interactiva, esperamos compartir nuestro entusiasmo por Python y ofrecer a otros aprendices una fuente valiosa de conocimiento y recursos para su propio crecimiento profesional. ¡Únete a nosotros en esta emocionante aventura hacia el dominio de Python y la ciencia de datos!
            
                   """)
    
    

if __name__ == "__main__":
    main()
    