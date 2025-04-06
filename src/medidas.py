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


def calculate_contrast(image):
    """Calcula el contraste como la desviación estándar de las intensidades de los píxeles."""
    return np.std(image)
