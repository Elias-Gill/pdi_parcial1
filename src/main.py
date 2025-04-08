"""
Created on 2025-04-05 12:30:36

@authors:
    - Elias Sebastian Gill Quintana
    - Maria Jose Mendoza Recalde
    - Abigail Mercedes Nuñes Mendez
"""

import os
import cv2
import time
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

estadisticas = "estadisticas"
os.makedirs(estadisticas, exist_ok=True)


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
            image_folder, f"{titles[i].lower().replace(' ', '_')}_histograma.pgf"
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
        # Inicializar estructura para métricas
        metricas = {
            "CLAHE": {
                "ambe": [],
                "psnr": [],
                "entropy": [],
                "contrast": [],
                "uniformity": [],
                "time": [],
            },
            "HE": {
                "ambe": [],
                "psnr": [],
                "entropy": [],
                "contrast": [],
                "uniformity": [],
                "time": [],
            },
            "DQHEPL": {
                "ambe": [],
                "psnr": [],
                "entropy": [],
                "contrast": [],
                "uniformity": [],
                "time": [],
            },
            "BHEPL-D": {
                "ambe": [],
                "psnr": [],
                "entropy": [],
                "contrast": [],
                "uniformity": [],
                "time": [],
            },
        }

        # Verificar si hay archivos para procesar
        if not files:
            print("¡No se encontraron archivos en el directorio!")
        else:
            print(f"\nProcesando {len(files)} imágenes...")

            for filename in files:
                file_path = os.path.join(directory, filename)

                try:
                    img = medidas.read_image_as_grayscale(file_path)

                    # Calcular métricas de la imagen original
                    orig_entropy = medidas.calculate_entropy(img)
                    orig_contrast = medidas.calculate_contrast(img)
                    orig_uniformity = medidas.calculate_uniformity(img)

                    # Medir tiempos de procesamiento
                    tiempos = {}
                    start = time.perf_counter()
                    clahe = metodos.apply_clahe(img)
                    tiempos["CLAHE"] = time.perf_counter() - start

                    start = time.perf_counter()
                    he = metodos.apply_histogram_equalization(img)
                    tiempos["HE"] = time.perf_counter() - start

                    start = time.perf_counter()
                    dqhepl = metodos.apply_dqhepl(img)
                    tiempos["DQHEPL"] = time.perf_counter() - start

                    start = time.perf_counter()
                    bhepl_d = metodos.apply_bhepl_d(img)
                    tiempos["BHEPL-D"] = time.perf_counter() - start

                    # Guardar estadísticas individuales
                    stats_filename = os.path.splitext(filename)[0] + "_stats.txt"
                    stats_path = os.path.join(estadisticas, stats_filename)

                    with open(stats_path, "w") as stats_file:
                        stats_file.write(f"Estadísticas para: {filename}\n")
                        stats_file.write("=" * 50 + "\n\n")
                        
                        # Escribir métricas de la imagen original
                        stats_file.write("Imagen Original:\n")
                        stats_file.write(f"Entropía: {orig_entropy:.4f}\n")
                        stats_file.write(f"Contraste: {orig_contrast:.4f}\n")
                        stats_file.write(f"Uniformidad: {orig_uniformity:.4f}\n")
                        stats_file.write("-" * 40 + "\n\n")

                        for name, processed in zip(
                            ["CLAHE", "HE", "DQHEPL", "BHEPL-D"],
                            [clahe, he, dqhepl, bhepl_d],
                        ):
                            # Calcular métricas
                            ambe = medidas.calculate_ambe(img, processed)
                            psnr = medidas.calculate_psnr(img, processed)
                            entropy = medidas.calculate_entropy(processed)
                            contrast = medidas.calculate_contrast(processed)
                            uniformity = medidas.calculate_uniformity(processed)
                            tiempo = tiempos[name]

                            # Almacenar métricas (solo para estadísticas globales)
                            metricas[name]["ambe"].append(ambe)
                            metricas[name]["psnr"].append(psnr)
                            metricas[name]["entropy"].append(entropy)
                            metricas[name]["contrast"].append(contrast)
                            metricas[name]["uniformity"].append(uniformity)
                            metricas[name]["time"].append(tiempo)

                            # Escribir en archivo
                            stats_file.write(f"Método: {name}\n")
                            stats_file.write(f"AMBE: {ambe:.4f}\n")
                            stats_file.write(f"PSNR: {psnr:.4f} dB\n")
                            stats_file.write(f"Entropía: {entropy:.4f}\n")
                            stats_file.write(f"Contraste: {contrast:.4f}\n")
                            stats_file.write(f"Uniformidad: {uniformity:.4f}\n")
                            stats_file.write(f"Tiempo: {tiempo*1000:.2f} ms\n")
                            stats_file.write("-" * 40 + "\n\n")

                except Exception as e:
                    print(f"Error procesando {filename}: {str(e)}")
                    continue

            # Mostrar resumen estadístico
            print("\n" + "=" * 50)
            print("RESUMEN ESTADÍSTICO DE TODAS LAS IMÁGENES")
            print("=" * 50 + "\n")

            # Encabezados de la tabla
            print(
                f"{'Método':<10} {'AMBE (↓)':<10} {'PSNR (↑)':<10} {'Entropía':<10} {'Contraste':<10} {'Uniformidad':<12} {'Tiempo (ms)':<10}"
            )
            print("-" * 80)

            for metodo in metricas:
                if not metricas[metodo]["ambe"]:
                    print(f"{metodo}: No hay datos disponibles")
                    continue

                # Calcular estadísticas
                stats = {
                    "ambe_mean": np.mean(metricas[metodo]["ambe"]),
                    "ambe_med": np.median(metricas[metodo]["ambe"]),
                    "psnr_mean": np.mean(metricas[metodo]["psnr"]),
                    "psnr_med": np.median(metricas[metodo]["psnr"]),
                    "entropy_mean": np.mean(metricas[metodo]["entropy"]),
                    "entropy_med": np.median(metricas[metodo]["entropy"]),
                    "contrast_mean": np.mean(metricas[metodo]["contrast"]),
                    "contrast_med": np.median(metricas[metodo]["contrast"]),
                    "uniformity_mean": np.mean(metricas[metodo]["uniformity"]),
                    "uniformity_med": np.median(metricas[metodo]["uniformity"]),
                    "time_mean": np.mean(metricas[metodo]["time"])
                    * 1000,  # Convertir a ms
                }

            # RESULTADOS FINALES MEJORADOS
            print("\n\n=== RESUMEN ESTADÍSTICO ===")
            print("Método       | AMBE (↓)        | PSNR (↑)       | Entropía       | Contraste     | Uniformidad   | Tiempo (ms)")
            print("             | Media   Mediana | Media  Mediana | Media Mediana  | Media Mediana | Media Mediana | Media")
            print("-" * 120)

            for metodo in ["CLAHE", "HE", "DQHEPL", "BHEPL-D"]:
                datos = metricas[metodo]

                # Solo si hay datos procesados
                if datos["ambe"]:
                    print(
                        f"{metodo:<12}| "
                        f"{np.mean(datos['ambe']):6.2f}  {np.median(datos['ambe']):6.2f} | "
                        f"{np.mean(datos['psnr']):6.2f}  {np.median(datos['psnr']):6.2f} | "
                        f"{np.mean(datos['entropy']):5.2f}  {np.median(datos['entropy']):5.2f} | "
                        f"{np.mean(datos['contrast']):6.2f}  {np.median(datos['contrast']):6.2f} | "
                        f"{np.mean(datos['uniformity']):5.4f}  {np.median(datos['uniformity']):5.4f} | "
                        f"{np.mean(datos['time'])*1000:7.2f}"
                    )

            # Explicación de métricas
            print("\nLEYENDA:")
            print("- AMBE: Absolute Mean Brightness Error (menor es mejor)")
            print("- PSNR: Peak Signal-to-Noise Ratio en dB (mayor es mejor)")
            print("- Uniformidad: 1 = máxima uniformidad")
            print("- Tiempos en milisegundos (menor es mejor)")


if __name__ == "__main__":
    main()
