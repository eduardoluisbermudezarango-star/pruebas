"""
registro.py
Manejo del archivo de logs. Es el ÚNICO uso de archivos del sistema
(no hay base de datos): aquí se guardan los eventos y los errores.
"""

import os                       # Módulo del sistema operativo: sirve para crear carpetas y armar rutas
from datetime import datetime   # Clase que entrega la fecha y la hora actuales

CARPETA_LOGS = "logs"                                        # Nombre de la carpeta donde se guarda el log
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "software_fj.log")  # Une carpeta y nombre: logs/software_fj.log


# Función interna (el guion bajo indica que solo se usa dentro de este archivo)
def _escribir(nivel, mensaje):
    """Escribe una línea en el log. Usa try/except/finally."""
    archivo = None                                              # Se crea la variable vacía para poder revisarla en finally
    try:                                                        # Bloque con las instrucciones que pueden fallar
        os.makedirs(CARPETA_LOGS, exist_ok=True)                # Crea la carpeta logs; si ya existe, no hace nada
        archivo = open(ARCHIVO_LOG, "a", encoding="utf-8")      # Abre el archivo en modo "a" (agregar al final) con tildes
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # Toma la fecha y hora y las convierte en texto
        archivo.write(f"{fecha} | {nivel:<6} | {mensaje}\n")    # Escribe la línea: fecha | nivel (6 espacios) | mensaje
    except OSError as error:                                    # Se ejecuta si falla el disco o no hay permisos
        # Se avisa en consola, pero el programa NO se detiene
        print(f"  (No se pudo escribir en el log: {error})")
    finally:                                                    # Se ejecuta siempre, haya error o no
        if archivo is not None:                                 # Solo si el archivo alcanzó a abrirse
            archivo.close()                                     # Cierra el archivo para guardar los cambios


# Función pública para registrar algo que salió bien
def registrar_evento(mensaje):
    """Registra una operación exitosa o un evento relevante."""
    _escribir("EVENTO", mensaje)    # Escribe la línea con el nivel EVENTO


# Función pública para registrar un error; contexto dice en qué operación ocurrió
def registrar_error(error, contexto=""):
    """Registra un error con su tipo, su mensaje y, si existe, el error que lo causó."""
    texto = f"{contexto} -> {type(error).__name__}: {error}"    # Arma el texto: operación -> NombreDelError: mensaje
    if error.__cause__ is not None:                             # __cause__ tiene valor cuando se usó "raise ... from ..."
        causa = error.__cause__                                 # Toma la excepción original que quedó encadenada
        texto += f" | Causa original: {type(causa).__name__}: {causa}"   # Agrega la causa al texto
    _escribir("ERROR", texto)                                   # Escribe la línea con el nivel ERROR
