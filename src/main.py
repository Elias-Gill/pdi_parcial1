# -*- coding: utf-8 -*-
"""
Created on 2025-04-05 12:30:36

@authors:
    - Elias Sebastian Gill Quintana
    - Maria Jose Mendoza Recalde
    - Abigail Mercedes Nuñes Mendez
"""


import cv2


def show_img(path: str):
    img = cv2.imread(path)
    if img is None:
        print("Error: No se pudo cargar la imagen")
    else:
        cv2.imshow(path, img)
        cv2.waitKey()
        cv2.destroyAllWindows()
