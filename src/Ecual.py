# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import numpy as np

# Cargar la imagen en escala de grises
image_gray = cv2.imread('1.jpg', cv2.IMREAD_GRAYSCALE)

# Verificar si la imagen se ha cargado correctamente
if image_gray is None:
    print("Error: la imagen no se pudo cargar. Verifica la ruta del archivo.")
else:
    # Ecualizar el histograma de la imagen
    image_equalized = cv2.equalizeHist(image_gray)

    # Mostrar la imagen original y la imagen ecualizada
    cv2.imshow('Imagen Original', image_gray)
    cv2.imshow('Imagen Ecualizada', image_equalized)

    # Esperar a que el usuario presione una tecla y cerrar todas las ventanas
    cv2.waitKey(0)
    cv2.destroyAllWindows()