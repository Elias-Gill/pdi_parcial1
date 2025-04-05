# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 13:39:13 2024

@author: marce
"""

import cv2
import numpy as np

# Cargar la imagen en escala de grises
image_gray = cv2.imread('tsukuba_L.png', cv2.IMREAD_GRAYSCALE)

# Verificar si la imagen se ha cargado correctamente
if image_gray is None:
    print("Error: la imagen no se pudo cargar. Verifica la ruta del archivo.")
else:
    # Ecualizar el histograma de la imagen de manera estándar
    image_equalized = cv2.equalizeHist(image_gray)

    # Crear el objeto CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    # Aplicar CLAHE a la imagen en escala de grises
    image_clahe = clahe.apply(image_gray)

    # Mostrar la imagen original, la imagen con histograma ecualizado y la imagen con CLAHE
    cv2.imshow('Imagen Original', image_gray)
    cv2.imshow('Histograma Ecualizado', image_equalized)
    cv2.imshow('CLAHE', image_clahe)

    # Esperar a que el usuario presione una tecla y cerrar todas las ventanas
    cv2.waitKey(0)
    cv2.destroyAllWindows()