import streamlit as st
import cv2
import numpy as np
import os

def main():
    # ----------- READ DNN MODEL -----------
    # Model architecture
    prototxt = "FinalPr/pages/detection/model/MobileNetSSD_deploy.prototxt.txt"
    # Weights
    model = "FinalPr/pages/detection/model/MobileNetSSD_deploy.caffemodel"
    # Class labels
    classes = {
        0: "fondo", 1: "avión", 2: "bicicleta",
        3: "pájaro", 4: "barco",
        5: "botella", 6: "autobús",
        7: "coche", 8: "gato",
        9: "silla", 10: "vaca",
        11: "mesa de comedor", 12: "perro",
        13: "caballo", 14: "motocicleta",
        15: "persona", 16: "planta en maceta",
        17: "oveja", 18: "sofá",
        19: "tren", 20: "monitor de televisión"
    }

    # Load the model
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    # ----------- STREAMLIT APP -----------
    st.title("Detector de objetos a través de imágenes")

    # Mostrar las clases de objetos con las que el algoritmo está entrenado en columnas
    st.write("""
    Este proyecto es una aplicación web dinámica e interactiva de ciencia de datos que utiliza algoritmos de aprendizaje automático profundo para identificar y clasificar imágenes 
    introducidas por los usuarios.
    
    Su objetivo principal es proporcionar a los usuarios la capacidad de analizar y clasificar imágenes con precisión y eficiencia, 
    ya sea para propósitos académicos, de investigación, o para cualquier uso práctico.
    
    Nuestro enfoque consistió en adaptar y personalizar un algoritmo de red neuronal convolucional preentrenado. 
    Este algoritmo es conocido por su eficiencia en el procesamiento y reconocimiento de imágenes debido a su habilidad para detectar y aprender patrones 
    en los datos de entrada. En lugar de entrenar un modelo desde cero, que puede requerir una gran cantidad de tiempo y recursos, optamos por utilizar técnicas de transferencia de aprendizaje.
    Esto implica tomar un modelo preentrenado y adaptarlo a nuestras necesidades específicas, lo que nos permite beneficiarnos del aprendizaje previo del modelo y ahorrar en recursos de entrenamiento.

    Esta app no sólo está diseñada para ser una herramienta de clasificación de imágenes potente y precisa, 
    sino que también pretende ser una plataforma educativa para aquellos interesados en aprender más sobre la ciencia de datos y el aprendizaje automático.
    """)
    
    st.write("El algoritmo está entrenado con las siguientes imágenes:")
    col1, col2, col3 = st.columns(3)
    col1.header("")
    col2.header("")
    col3.header("")
    st.header("")
    with col1:
        for class_id, class_name in list(classes.items())[:7]:
            st.write(f"{class_id}: {class_name}")

    with col2:
        for class_id, class_name in list(classes.items())[7:14]:
            st.write(f"{class_id}: {class_name}")

    with col3:
        for class_id, class_name in list(classes.items())[14:]:
            st.write(f"{class_id}: {class_name}")

    # Upload image

    uploaded_file = st.file_uploader("Seleccione una imagen", type=["jpg", "jpeg", "png"])


    if uploaded_file is not None:
        # Read and preprocess the image
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        height, width, _ = image.shape
        image_resized = cv2.resize(image, (300, 300))

        # Create a blob
        blob = cv2.dnn.blobFromImage(image_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5))

        # DETECTIONS AND PREDICTIONS
        net.setInput(blob)
        detections = net.forward()

        for detection in detections[0][0]:
            if detection[2] > 0.45:
                label = classes[detection[1]]
                box = detection[3:7] * [width, height, width, height]
                x_start, y_start, x_end, y_end = int(box[0]), int(box[1]), int(box[2]), int(box[3])
    
                cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 12)
                cv2.putText(image, "Conf: {:.2f}".format(detection[2] * 100), (x_start, y_start - 5), 1, 1.2, (255, 0, 0), 2)
                cv2.putText(image, label, (x_start, y_start - 25), 1, 1.5, (255, 0, 0), 2)
    
                level = "Intermediate"  # Obtener el nivel desde algún cálculo o fuente de datos
                accuracy = detection[2] * 100  # Obtener la precisión del objeto detectado
    
                # Display level and accuracy
                st.write(f"Etiqueta: {label}, Precisión: {accuracy:.2f}")

        # Display the image with detections
        st.image(image, channels="BGR")
        
if __name__ == "__main__":
    main()
