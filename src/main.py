"""
Created on 2025-04-05 12:30:36

@authors:
    - Elias Sebastian Gill Quintana
    - Maria Jose Mendoza Recalde
    - Abigail Mercedes Nuñes Mendez
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import metodos
import medidas
import argparse


# directorio del dataset
directory = "dataset/"

# directorio output de imagenes procesadas
output_dir = "procesadas/"
os.makedirs(output_dir, exist_ok=True)

# directorio output de histogramas
histogram_dir = "histogramas"
os.makedirs(histogram_dir, exist_ok=True)


def plot_histograms_and_save(images, titles, base_filename):
    """
    Función para graficar los histogramas de las imágenes y guardarlos en carpetas por imagen.
    """
    # Crear una carpeta para cada imagen donde se guardarán los histogramas
    image_folder = os.path.join(histogram_dir, base_filename)
    os.makedirs(image_folder, exist_ok=True)

    for i, img in enumerate(images):
        plt.figure(figsize=(10, 5))
        plt.hist(img.ravel(), bins=256, range=(0, 256), color="gray", alpha=0.7)
        plt.title(f"Histograma de {titles[i]}")
        plt.xlabel("Intensidad")
        plt.ylabel("Frecuencia")

        # Guardar el gráfico como imagen en la carpeta específica
        histogram_path = os.path.join(
            image_folder, f"{titles[i].lower().replace(' ', '_')}_histograma.png"
        )
        plt.savefig(histogram_path)
        plt.close()


def save_images(path, filename, images, titles):
    """Guarda versiones procesadas de una imagen."""
    for img, title in zip(images, titles):
        save_path = os.path.join(path, f"{os.path.splitext(filename)[0]}_{title}.png")
        cv2.imwrite(save_path, img)


def apply_all_methods(img):
    """Aplica los 4 métodos requeridos a una imagen."""
    clahe = metodos.apply_clahe(img)
    he = metodos.apply_histogram_equalization(img)
    dqhepl = metodos.apply_dqhepl(img)
    bhepl_d = metodos.apply_bhepl_d(img)
    return clahe, he, dqhepl, bhepl_d


def main():
    """
    Función principal del script. Permite ejecutar tres modos de operación:

    1. Sin flags: Aplica cuatro métodos de mejora de contraste (CLAHE, HE, DQHEPL, BHEPL-D)
       a todas las imágenes del dataset y calcula métricas de calidad (AMBE, PSNR, entropía, contraste).
       Luego muestra un resumen con los promedios por método.

    2. Con flag '--histogramas': Muestra los histogramas de la imagen original y sus versiones mejoradas
       usando los cuatro métodos, para las primeras 5 imágenes del dataset.

    3. Con flag '--imagenes': Guarda las primeras 5 imágenes procesadas por los cuatro métodos
       en una carpeta 'salida/' con nombres descriptivos.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--histogramas",
        action="store_true",
        help="Mostrar histogramas de las primeras 5 imágenes",
    )
    parser.add_argument(
        "--imagenes",
        action="store_true",
        help="Guardar versiones procesadas de las primeras 5 imágenes",
    )
    args = parser.parse_args()

    files = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]
    files.sort()
    first_5 = files[:5]

    # --histogramas
    if args.histogramas:
        for filename in first_5:
            file_path = os.path.join(directory, filename)
            img = medidas.read_image_as_grayscale(file_path)
            clahe, he, dqhepl, bhepl_d = apply_all_methods(img)

            # Crear los nombres de archivo para las imágenes de histograma
            plot_histograms_and_save(
                [img, clahe, he, dqhepl, bhepl_d],
                ["Original", "CLAHE", "HE", "DQHEPL", "BHEPL-D"],
                filename.split(".")[
                    0
                ],  # Usar el nombre base del archivo para la carpeta
            )

    # --imagenes
    elif args.imagenes:
        for filename in first_5:
            file_path = os.path.join(directory, filename)
            img = medidas.read_image_as_grayscale(file_path)
            clahe, he, dqhepl, bhepl_d = apply_all_methods(img)

            # Crear una carpeta para cada imagen procesada
            image_dir = os.path.join(
                output_dir, filename.split(".")[0]
            )  # Usar el nombre de la imagen sin la extensión
            os.makedirs(image_dir, exist_ok=True)  # Crear la carpeta si no existe

            # Guardar la imagen original
            original_image_path = os.path.join(
                image_dir, f"{filename.split('.')[0]}_original.png"
            )
            cv2.imwrite(original_image_path, img)

            # Guardar las imágenes procesadas en la carpeta correspondiente
            save_images(
                image_dir,  # Ruta de la carpeta de la imagen
                filename,
                [clahe, he, dqhepl, bhepl_d],
                ["clahe", "he", "dqhepl", "bhepl_d"],
            )

    # sin flag
    else:
        metricas = {
            "CLAHE": {
                "ambe": [],
                "psnr": [],
                "entropy": [],
                "contrast": [],
                "uniformity": [],
            },
            "HE": {
                "ambe": [],
                "psnr": [],
                "entropy": [],
                "contrast": [],
                "uniformity": [],
            },
            "DQHEPL": {
                "ambe": [],
                "psnr": [],
                "entropy": [],
                "contrast": [],
                "uniformity": [],
            },
            "BHEPL-D": {
                "ambe": [],
                "psnr": [],
                "entropy": [],
                "contrast": [],
                "uniformity": [],
            },
        }

        for filename in files:
            file_path = os.path.join(directory, filename)
            img = medidas.read_image_as_grayscale(file_path)
            clahe, he, dqhepl, bhepl_d = apply_all_methods(img)

            # Calcular las métricas de imagen para cada método
            for name, processed in zip(
                ["CLAHE", "HE", "DQHEPL", "BHEPL-D"],
                [clahe, he, dqhepl, bhepl_d],
            ):
                metricas[name]["ambe"].append(medidas.calculate_ambe(img, processed))
                metricas[name]["psnr"].append(medidas.calculate_psnr(img, processed))
                metricas[name]["entropy"].append(medidas.calculate_entropy(processed))
                metricas[name]["contrast"].append(medidas.calculate_contrast(processed))
                metricas[name]["uniformity"].append(
                    medidas.calculate_uniformity(processed)
                )  # Nueva métrica de uniformidad

        print("Resumen de métricas:\n")
        for metodo, datos in metricas.items():
            print(f"== {metodo} ==")
            print(
                f"AMBE promedio:     {np.mean(datos['ambe']):.2f}  Mediana: {np.median(datos['ambe']):.2f}"
            )
            print(
                f"PSNR promedio:     {np.mean(datos['psnr']):.2f}  Mediana: {np.median(datos['psnr']):.2f}"
            )
            print(
                f"Entropía promedio: {np.mean(datos['entropy']):.2f}  Mediana: {np.median(datos['entropy']):.2f}"
            )
            print(
                f"Contraste promedio:{np.mean(datos['contrast']):.2f}  Mediana: {np.median(datos['contrast']):.2f}"
            )
            print(
                f"Uniformidad promedio:{np.mean(datos['uniformity']):.4f}  Mediana: {np.median(datos['uniformity']):.4f}"
            )
            print()


if __name__ == "__main__":
    main()
