import cv2
import numpy as np
from scipy.stats import entropy


def read_image_as_grayscale(path):
    """Lee una imagen en escala de grises de la ruta especificada."""
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)


def calculate_ambe(original, processed):
    """Calcula el error de brillo medio absoluto (AMBE)."""
    return abs(np.mean(original) - np.mean(processed))


def calculate_psnr(original, processed):
    """Calcula la relación señal-ruido máxima (PSNR)."""
    return cv2.PSNR(original, processed)


def calculate_entropy(image):
    """Calcula la entropía de la imagen (medida de información)."""
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist = hist.ravel() / hist.sum()  # Convertir a probabilidades 1D
    return entropy(hist, base=2)


def calculate_uniformity(image):
    """
    Calcula la uniformidad usando el Coeficiente de Variación (CV).
    Devuelve un valor entre 0 (máxima no uniformidad) y 1 (máxima uniformidad).
    """
    mean, std = cv2.meanStdDev(image)
    mean = mean[0][0] if mean[0][0] != 0 else 1e-10  # Evitar división por cero
    cv = std[0][0] / mean
    return 1 / (1 + cv)  # Normalizado a [0, 1]

def calculate_contrast(image):
    """Calcula el contraste como la desviación estándar de las intensidades de los píxeles."""
    return np.std(image)
