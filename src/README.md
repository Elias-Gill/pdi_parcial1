El dataset utilizado es el de: 
https://projects.asl.ethz.ch/datasets/doku.php?id=ir%3Airicra2014

Pero solo es utilizado un subset de 309 imagenes de este dataset. Mas especificamente: 
`Sempatch-5` las imagenes de `8bit`.

## 1. **AMBE (Error de Brillo Medio Absoluto)**

AMBE mide la diferencia en el brillo medio entre la imagen original y la procesada.
Cuanto más bajo sea el valor, mejor, ya que indica que el brillo de la imagen procesada es
similar al de la original.
- **Valor bajo**:
  Mejora la imagen sin alterar mucho el brillo.
- **Valor alto**:
  Indica que hubo una alteración significativa en el brillo medio.

## 2. **PSNR (Relación Señal-Ruido Máxima)**

PSNR mide la calidad de la imagen procesada en relación con la original.
Cuanto mayor sea el valor, mejor será la calidad percibida, ya que significa que la imagen
procesada es más similar a la original en términos de ruido y distorsión.
- **Valor alto**:
  Mejor preservación de la calidad de la imagen.
- **Valor bajo**:
  Mayor distorsión y ruido en la imagen.

## 3. **Entropía**

La entropía mide la cantidad de información o complejidad en la imagen.
Valores más altos indican imágenes con más detalles y variación.
- **Valor alto**:
  Más detalles en la imagen.
- **Valor bajo**:
  Imagen más uniforme y con menos detalles.

## 4. **Contraste**

El contraste mide la variabilidad en la intensidad de los píxeles.
Un valor más alto significa que hay más diferencia entre las zonas claras y oscuras de la
imagen.
- **Valor alto**:
  Mayor diferencia entre las áreas claras y oscuras, mejor visibilidad de los detalles.
- **Valor bajo**:
  Imagen más uniforme y menos diferenciación entre áreas claras y oscuras.
