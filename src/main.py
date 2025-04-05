# -*- coding: utf-8 -*-
"""
Created on 2025-04-05 12:30:36

@authors: 
    - Elias Sebastian Gill Quintana
    - Maria Jose Mendoza Recalde
    - Abigail Mercedes Nuñes Mendez
"""


import cv2

# Utilizando el comando imread de opencv, leeremos la imagen 1.jpeg y la guardaremos en la variable img
def show_img(img: str):
    img = cv2.imread(img)
    if img is None:
        print("Error: No se pudo cargar la imagen")
    else:
        cv2.imshow("ventana1", img)
        cv2.waitKey()
        cv2.destroyAllWindows()

img = cv2.imread("1.jpeg")
img2 = cv2.imread("1.jpeg",0)

cv2.imshow("ventana", img) ## Mostramos la imagen en la ventana "ventana", es redimensionable pero no cambia su escala


while True:
    
    key = cv2.waitKey()
    
    if key == ord("4"):
        cv2.imshow("ventana", img)
    elif key == ord("6"):
        cv2.imshow("ventana", img2)
    else:
        break
    
cv2.destroyAllWindows()
