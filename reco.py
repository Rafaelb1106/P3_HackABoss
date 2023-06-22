import streamlit as st
import face_recognition
import cv2
import os

def cargar_imagenes_referencia(directorio):
    lista_imagenes = os.listdir(directorio)
    lista_encodings = []
    lista_nombre = []

    for imagen in lista_imagenes:
        # Comprobar que el archivo sea una imagen
        if imagen.endswith(".jpg") or imagen.endswith(".jpeg") or imagen.endswith(".png"):
            imagen_path = os.path.join(directorio, imagen)
            imagen_referencia = face_recognition.load_image_file(imagen_path)
            encoding_referencia = face_recognition.face_encodings(imagen_referencia)[0]
            lista_encodings.append(encoding_referencia)
            lista_nombre.append(imagen)
        
    return lista_encodings , lista_nombre

def main():
    st.title("Roconocer mediante una foto")
    st.write("Se reconoce mediante las fotos que esta ubica en la carpeta de fotos. se puede múltiples fotos a la vez pero se hace lento y se necesito un equipo de computo mas potente ")
    st.write("Vamos a utilizar una librería que se llama face recognition")
    ban = True
    ban1 = 0    
    
    lista_imagenes_referencia, lista_nombres = cargar_imagenes_referencia("fotos")
          
    captura = cv2.VideoCapture(0)
    col1, col2 = st.columns(2)
    ventana = st.image([])
    with col1:
        if st.button(label="Iniciar", key="B1"):
            ban1 = 1        
    with col2:
        if st.button(label="Parar", key="B2"):
            ban1 = 0       
    while ban:
        
        ret, frame = captura.read()
        
        # Detectar los rostros en el frame si se le dio al boton iniciar
        if ban1 == 1 :
            rgb_frame = frame[:, :, ::-1]
            rostros = face_recognition.face_locations(rgb_frame)
            enc_rostros = face_recognition.face_encodings(rgb_frame, rostros)
        
            for encoding in enc_rostros:
                # Comparar el rostro detectado con el rostro de referencia                
                coincidencias = face_recognition.compare_faces(lista_imagenes_referencia, encoding)
                for indice, coincidencia in enumerate(coincidencias):
                    if coincidencia:
                        (top, right, bottom, left) = rostros[coincidencias.index(True)]
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)                                            
                        try:
                            cv2.putText(frame, lista_nombres[indice], (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        except:
                            pass
                    
        # Mostrar el frame en la ventana
        ventana.image(frame, channels="BGR")
        
        # Romper el bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            ban = False
    
    # Liberar los recursos
    captura.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
