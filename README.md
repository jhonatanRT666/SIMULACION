✨ Bienvenue a simulacion. 

PASOS DE INSTALACION 
- INSTALAR PYTHON EN EL ORDENADOR (REQUISITO FUNDAMENTAL)
- INSTALAR VISUAL STUDIO CODE (REQUISITO OPCIONAL)
- INSTALAR LAS LIBRERIAS MOSTRADAS EN EL ARHIVO ".py". (REQUISITO FUNDAMENTAL)
    codigo de instalacion (pip install ####), donde #### es la libreria que necesita
- LISTO PARA CORRER

Este proyecto implementa distintos **métodos de generación de números pseudoaleatorios** y los somete a **pruebas estadísticas de uniformidad, media y varianza**.  
La aplicación cuenta con una **interfaz gráfica construida en Tkinter y CustomTkinter**, y permite visualizar los resultados en forma de tablas e histogramas.

- Pruebas estadísticas incluidas:
  - ✅ **Prueba de la Media (Z-test)**
  - ✅ **Prueba de la Varianza (Chi²-test)**
  - ✅ **Prueba de Uniformidad (Chi² con histograma + KDE)**

## 🛠️ Tecnologías utilizadas

- [Python 3.10+](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Matplotlib](https://matplotlib.org/)
- [SciPy](https://scipy.org/)
- [NumPy](https://numpy.org/)

📑 Pruebas implementadas
🔹 Prueba de Media
Evalúa si la media de los números generados se acerca a la media teórica de 0.5.
Se utiliza un test Z con un nivel de significancia configurable.

🔹 Prueba de Varianza
Contrasta si la varianza muestral coincide con la varianza teórica de una distribución U(0,1), que es 1/12.
Se usa distribución Chi².

🔹 Prueba de Uniformidad
Divide los números en m intervalos y compara frecuencias observadas vs esperadas.
Incluye histograma visual + KDE para inspección gráfica.

A continuacion se presenta una imagen del programa mostrando el metodo multiplicador por constante.

![image-alt](https://github.com/jhonatanRT666/SIMULACION/blob/0641427c89ed6e94b72bbdf5a89f1dc0bad64632/inicio.PNG)

Ahora se muestra un histograma de la prueba de uniformidad

![image-alt](https://github.com/jhonatanRT666/SIMULACION/blob/0641427c89ed6e94b72bbdf5a89f1dc0bad64632/image.png)


