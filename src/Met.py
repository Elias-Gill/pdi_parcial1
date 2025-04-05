# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 13:44:05 2024

@author: marce
"""

import cv2
import numpy as np
from skimage.measure import shannon_entropy

def calculate_ambe(image1, image2):
    """
    Calcula el Error Medio Absoluto del Brillo (AMBE) entre dos imágenes.
    """
    return abs(np.mean(image1) - np.mean(image2))

def calculate_psnr(image1, image2):
    """
    Calcula la Relación Señal a Ruido de Pico (PSNR) entre dos imágenes.
    """
    mse = np.mean((image1 - image2) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

def calculate_entropy(image):
    """
    Calcula la entropía de Shannon de una imagen.
    """
    return shannon_entropy(image)

def calculate_contrast(image):
    """
    Calcula el contraste de una imagen como su desviación estándar.
    """
    return np.std(image)


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
    
    print("Métricas para la imagen original")
    entropy_image1 = calculate_entropy(image_gray)
    contrast_image1 = calculate_contrast(image_gray)
    print(f"Entropía (Imagen 1): {entropy_image1}")
    print(f"Contraste (Imagen 1): {contrast_image1}")
    
    # Calcular y mostrar métricas
    ambe = calculate_ambe(image_gray, image_equalized)
    psnr = calculate_psnr(image_gray, image_equalized)
    entropy_image1 = calculate_entropy(image_equalized)
    contrast_image1 = calculate_contrast(image_equalized)
    

    print("Métricas para la Ecualización del Histogrma")
    print(f"AMBE: {ambe}")
    print(f"PSNR: {psnr}")
    print(f"Entropía (Imagen 1): {entropy_image1}")
    print(f"Contraste (Imagen 1): {contrast_image1}")
    
    
    # Calcular y mostrar métricas
    ambe = calculate_ambe(image_gray, image_clahe )
    psnr = calculate_psnr(image_gray, image_clahe )
    entropy_image1 = calculate_entropy(image_clahe)
    contrast_image1 = calculate_contrast(image_clahe)
    
    print("Métricas para el CLAHE")
    print(f"AMBE: {ambe}")
    print(f"PSNR: {psnr}")
    print(f"Entropía (Imagen 1): {entropy_image1}")
    print(f"Contraste (Imagen 1): {contrast_image1}")
    
    