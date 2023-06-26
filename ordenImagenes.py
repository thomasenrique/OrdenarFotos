import os
import shutil
import datetime
from PIL import Image, UnidentifiedImageError

# Carpeta de origen y destino
carpeta_origen = 'C:\\Users\\Andori\\Desktop\\TODAS_LAS_FOTOS\\TODO_JUNTO'
carpeta_destino = 'C:\\Users\\Andori\\Desktop\\TODAS_LAS_FOTOS\\FOTOS_POR_ANIO_v0.3'

""" carpeta_otros = os.path.join(carpeta_destino, 'otros') """
carpeta_sinIdentificar = os.path.join(carpeta_destino, 'Imagen_no_identificada')
carpeta_sinFecha = os.path.join(carpeta_destino, 'Imagen_sin_fecha_encontrada')

# Crear la carpeta si no existen
""" os.makedirs(carpeta_otros, exist_ok=True) """
os.makedirs(carpeta_sinIdentificar, exist_ok=True)
os.makedirs(carpeta_sinFecha, exist_ok=True)

# Obtener la lista de archivos en la carpeta de origen
archivos = os.listdir(carpeta_origen)

contador_sinIdentificar = 0
contador_sinFecha = 0
contador_archivoAsignado = 0
contador_archivosTotales = len(archivos)
contador_archivos_movido = 0


# Iterar sobre los archivos
for index, archivo in enumerate(archivos):
    print(f"Trabajando con el archivo {index+1} de {contador_archivosTotales}")
    ruta_archivo = os.path.join(carpeta_origen, archivo)

    # Verificar si es un archivo de imagen
    if os.path.isfile(ruta_archivo) and archivo.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4')):
        try:
            # Leer la metadata de creación de la imagen
            imagen = Image.open(ruta_archivo)
            metadata = imagen._getexif()
            fecha_creacion_str = metadata.get(36867)
            
            if fecha_creacion_str:
                fecha_creacion_components = fecha_creacion_str.split()
                if len(fecha_creacion_components) >= 1:
                    fecha_creacion = datetime.datetime.strptime(fecha_creacion_components[0], "%Y:%m:%d")
                    año = str(fecha_creacion.year)
                    mes = str(fecha_creacion.month)

                    # Crear las subcarpetas según el año y mes, si no existen
                    carpeta_año = os.path.join(carpeta_destino, año)
                    carpeta_mes = os.path.join(carpeta_año, mes)
                    os.makedirs(carpeta_mes, exist_ok=True)

                    # Copiar el archivo a la subcarpeta correspondiente
                    shutil.copy(ruta_archivo, carpeta_mes)
                    contador_archivoAsignado += 1
                    contador_archivos_movido += 1
                else:
                    # Copiar el archivo a la carpeta "otros"
                    shutil.copy(ruta_archivo, carpeta_sinFecha)
                    contador_sinFecha += 1
                    contador_archivos_movido += 1
            else:
                # Copiar el archivo a la carpeta "otros"
                shutil.copy(ruta_archivo, carpeta_sinFecha)
                contador_sinFecha += 1
                contador_archivos_movido += 1
        
        except UnidentifiedImageError:
            # No se pudo identificar la imagen
            """ print(f"No se pudo identificar la imagen: {archivo}") """
            shutil.copy(ruta_archivo, carpeta_sinIdentificar)
            contador_sinIdentificar += 1
            contador_archivos_movido += 1
            continue
        
        except (AttributeError, KeyError, IndexError):
            # No se pudo obtener la fecha de creación de la imagen
            """ print(f"No se pudo obtener la fecha de creación de {archivo}.") """
            # Copiar el archivo a la carpeta "otros"
            shutil.copy(ruta_archivo, carpeta_sinFecha)
            contador_sinFecha += 1
            contador_archivos_movido += 1
            continue

# Mensaje de finalización
print("Proceso de organización de archivos completado.")
print(f"Archivos asignados correctamente: {contador_archivoAsignado * 100 / contador_archivosTotales:.2f}% - {contador_archivoAsignado} de {contador_archivosTotales}")

print(f"Archivos movidos: {contador_archivos_movido} de {contador_archivosTotales}")
print(F"Archivos sin identificar: {contador_sinIdentificar} de {contador_archivosTotales}")
print(F"Archivos sin fecha: {contador_sinFecha} de {contador_archivosTotales}")