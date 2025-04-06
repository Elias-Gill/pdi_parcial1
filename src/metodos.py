import cv2
import numpy as np

# ```
# Tecnicas de mejora de imagen


def apply_histogram_equalization(image):
    """Aplica ecualización de histograma para mejorar el contraste de la imagen."""
    return cv2.equalizeHist(image)


def apply_clahe(image):
    """Aplica CLAHE con el límite de clip y tamaño de la cuadrícula de mosaicos indicados."""
    clip_limit = 2.0
    tile_grid_size = (8, 8)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    return clahe.apply(image)


def apply_dqhepl(imagen):
    """
    El método busca mejorar el contraste de imágenes preservando el brillo medio y evitando sobre-ecualización. Combina ideas de:
        1. División en cuadrantes dinámicos: Divide el histograma en 4 subhistogramas usando cuartiles estadísticos.
        2. Límites de meseta: Controla la amplificación del contraste recortando píxeles extremos.
        3. Preservación del brillo: Mantiene el punto medio del histograma original.
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    niveles = 256

    # Calcular el histograma y CDF de la imagen
    histograma = cv2.calcHist([imagen], [0], None, [niveles], [0, niveles])
    histograma = histograma.flatten()
    histograma = histograma.astype(np.float64)

    total_pixeles = imagen.shape[0] * imagen.shape[1]
    cdf = histograma.cumsum()

    # Calcular los valores de intensidad minimos y maximos
    intensidad_min = np.min(imagen)
    intensidad_max = np.max(imagen)

    # Calcular los cuartiles para division del histograma
    objetivo_25 = 0.25 * total_pixeles
    objetivo_50 = 0.5 * total_pixeles
    objetivo_75 = 0.75 * total_pixeles

    q1 = np.argmax(cdf >= objetivo_25)
    q2 = np.argmax(cdf >= objetivo_50)
    q3 = np.argmax(cdf >= objetivo_75)

    # Calcular los rangos de los subhistogramas
    rangos_subhist = []
    inicios = [intensidad_min, q1 + 1, q2 + 1, q3 + 1]
    finales = [q1, q2, q3, intensidad_max]

    for inicio, fin in zip(inicios, finales):
        if inicio > fin:
            temp = inicio
            inicio = fin
            fin = temp
        rangos_subhist.append((inicio, fin))

    subhists_recortados = []
    masas_recortadas = []

    # Recorte del histograma por meseta
    for inicio, fin in rangos_subhist:
        inicio = max(0, int(inicio))
        fin = min(niveles - 1, int(fin))

        subhist = histograma[inicio : fin + 1].copy()
        suma = subhist.sum()
        niveles_rango = max(1, fin - inicio)
        limite_meseta = suma / niveles_rango
        subhist_recortado = np.minimum(subhist, limite_meseta)

        subhists_recortados.append(subhist_recortado)
        masas_recortadas.append(subhist_recortado.sum())

    # Calcular los nuevos limites de intensidad
    n0 = 0
    n4 = niveles - 1

    if q2 != intensidad_min:
        n1 = q2 * (q1 - intensidad_min) / (q2 - intensidad_min)
    else:
        n1 = 0

    n1 = int(np.round(np.clip(n1, 0, 255)))
    n2 = int(np.clip(q2, 0, 255))

    if intensidad_max != q2:
        n3 = ((niveles - 1 - q2) * (q3 - q2) / (intensidad_max - q2)) + q2
    else:
        n3 = q2

    n3 = int(np.round(np.clip(n3, 0, 255)))

    nuevos_rangos = [(n0, n1), (n1, n2), (n2, n3), (n3, n4)]

    # Construir la tabla LUT
    tabla_lut = np.zeros(niveles, dtype=np.uint8)

    for i in range(4):
        inicio, fin = rangos_subhist[i]
        n_inicio, n_fin = nuevos_rangos[i]
        subhist = subhists_recortados[i]
        masa = masas_recortadas[i]

        if masa == 0:
            for j in range(int(inicio), int(fin) + 1):
                tabla_lut[j] = n_inicio
            continue

        acumulado = subhist.cumsum()
        for idx in range(int(inicio), int(fin) + 1):
            pos = idx - int(inicio)
            if pos < 0 or pos >= len(acumulado):
                continue
            y = n_inicio + (n_fin - n_inicio) * (acumulado[pos] / max(masa, 1e-10))
            tabla_lut[idx] = int(np.round(np.clip(y, 0, 255)))

    # Aplicar mapeo
    imagen_mejorada = cv2.LUT(imagen, tabla_lut)

    return imagen_mejorada


def apply_bhepl_d(imagen):
    """
    Método de ecualización bi-histograma con límite de meseta basado en la mediana. Diseñado para:
        1. Mejorar contraste preservando brillo medio
        2. Evitar sobre-realce y saturación
        3. Mantener información de la imagen original
    """
    # Calcular el histograma
    histograma = cv2.calcHist([imagen], [0], None, [256], [0, 256])
    histograma = histograma.ravel()
    histograma = histograma.astype(np.float64)

    total_pixeles = imagen.size

    # Calcular el punto medio del histograma (el valor de brillo medio)
    brillo_medio = np.sum(np.arange(256) * (histograma / total_pixeles))
    brillo_medio = int(round(np.clip(brillo_medio, 0, 255)))

    # Dividir el histograma en superior e inferior
    if brillo_medio >= 0:
        hist_inf = histograma[: brillo_medio + 1]
    else:
        hist_inf = np.array([])

    if brillo_medio < 255:
        hist_sup = histograma[brillo_medio + 1 :]
    else:
        hist_sup = np.array([])

    # Calcular los limites de meseta utilizando la media
    if len(hist_inf) > 0:
        meseta_inf = np.median(hist_inf)
    else:
        meseta_inf = 0

    if len(hist_sup) > 0:
        meseta_sup = np.median(hist_sup)
    else:
        meseta_sup = 0

    # Recortar los subhistogramas
    if len(hist_inf) > 0:
        hist_inf_rec = np.minimum(hist_inf, meseta_inf)
    else:
        hist_inf_rec = np.array([])

    if len(hist_sup) > 0:
        hist_sup_rec = np.minimum(hist_sup, meseta_sup)
    else:
        hist_sup_rec = np.array([])

    if len(hist_inf_rec) > 0:
        masa_inf = np.sum(hist_inf_rec)
    else:
        masa_inf = 0

    if len(hist_sup_rec) > 0:
        masa_sup = np.sum(hist_sup_rec)
    else:
        masa_sup = 0

    # Aplicar CDF y mapeo inferior
    mapeo_inf = np.zeros_like(hist_inf, dtype=np.float64)
    if masa_inf > 1e-10:
        cdf_inf = np.cumsum(hist_inf_rec)
        mapeo_inf = (brillo_medio * (cdf_inf / masa_inf)).astype(np.float64)

    # Aplicar CDF y mapeo superior
    if brillo_medio < 255:
        mapeo_sup = np.zeros_like(hist_sup, dtype=np.float64)
    else:
        mapeo_sup = np.array([])

    if masa_sup > 1e-10 and brillo_medio < 255:
        cdf_sup = np.cumsum(hist_sup_rec)
        mapeo_sup = (
            (brillo_medio + 1) + (254 - brillo_medio) * (cdf_sup / masa_sup)
        ).astype(np.float64)

    # Unificar los mapeos
    tabla_mapeo = np.zeros(256, dtype=np.uint8)

    if len(mapeo_inf) > 0:
        valores = np.round(np.clip(mapeo_inf, 0, 255)).astype(np.uint8)
        tabla_mapeo[: len(mapeo_inf)] = valores

    if len(mapeo_sup) > 0 and brillo_medio < 255:
        valores = np.round(np.clip(mapeo_sup, 0, 255)).astype(np.uint8)
        tabla_mapeo[brillo_medio + 1 : brillo_medio + 1 + len(mapeo_sup)] = valores

    # Aplicar mapeo
    imagen_mejorada = cv2.LUT(imagen, tabla_mapeo)

    return imagen_mejorada
