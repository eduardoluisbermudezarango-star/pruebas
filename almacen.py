#importamos librerias
# Importamos tkinter para crear la ventana
import tkinter as tk

# Importamos ttk para crear los menús desplegables
from tkinter import ttk



# Area donde podemos configurar colores y ancho de la pantalla



ANCHO_VENTANA = 700
ALTO_VENTANA = 600

COLOR_NARANJA ="#F28C28"
COLOR_AZUL = "#1976D2"
COLOR_VERDE = "#2E8B57"
COLOR_BLANCO = "#FFFFFF"
COLOR_GRIS = "#555555"
COLOR_ROJO = "#D32F2F"

TIPO_LETRA = "Arial"

TAMAÑO_TITULO = 20
TAMAÑO_NORMAL = 12
TAMAÑO_RESULTADO = 14



# Herramientas disponibles para alquilar 

# Creamos la clase que representa una herramienta
class HerramientaAlquiler:

    # Esta función crea una nueva herramienta
    def __init__(self, id_herramienta, nombre, tarifa_hora):

        # Guardamos el ID de la herramienta
        self._id_herramienta = id_herramienta

        # Guardamos el nombre de la herramienta
        self._nombre = nombre

        # Al comenzar no existe una hora de salida
        self._hora_salida = None

        # Guardamos el precio por hora
        self._tarifa_hora = tarifa_hora


         # Registramos la hora de salida
     

    # Esta función guarda la hora de salida
    def registrar_salida(self, hora):

        # Guardamos la hora
        self._hora_salida = hora

        # Indicamos que todo salió bien
        return True


     
    # Registramos la hora de retorno

    # Esta función revisa la hora de retorno
    def registrar_retorno(self, hora):

        # Revisamos si existe una hora de salida
        if self._hora_salida is None:

            # Si no existe, no podemos registrar retorno
            return False


        # Separamos la hora y los minutos de la salida
        hora_salida, minuto_salida = map(
            int,
            self._hora_salida.split(":")
        )


        # Separamos la hora y los minutos del retorno
        hora_retorno, minuto_retorno = map(
            int,
            hora.split(":")
        )


        # Convertimos la salida completa a minutos
        salida = hora_salida * 60 + minuto_salida


        # Convertimos el retorno completo a minutos
        retorno = hora_retorno * 60 + minuto_retorno


        # Revisamos que el retorno no sea antes de la salida
        if retorno < salida:

            # La hora no es correcta
            return False


        # La hora es correcta
        return True


     
    # Calculamos el tiempo que estuvo alquilada la herramienta
    

    # Calculamos cuánto tiempo estuvo alquilada
    def calcular_tiempo(self, hora_retorno):

        # Separamos la hora de salida
        hora_salida, minuto_salida = map(
            int,
            self._hora_salida.split(":")
        )


        # Separamos la hora de retorno
        hora_retorno, minuto_retorno = map(
            int,
            hora_retorno.split(":")
        )


        # Convertimos la salida a minutos
        salida = hora_salida * 60 + minuto_salida


        # Convertimos el retorno a minutos
        retorno = hora_retorno * 60 + minuto_retorno


        # Calculamos los minutos utilizados
        minutos_totales = retorno - salida


        # Calculamos las horas completas
        horas = minutos_totales // 60


        # Calculamos los minutos que sobran
        minutos = minutos_totales % 60


        # Devolvemos las horas y los minutos
        return horas, minutos


    #calculamos el costo del alquiler

    # Calculamos el valor que debe pagar el cliente
    def calcular_costo(self, hora_retorno):

        # Separamos la hora de salida
        hora_salida, minuto_salida = map(
            int,
            self._hora_salida.split(":")
        )


        # Separamos la hora de retorno
        hora_retorno, minuto_retorno = map(
            int,
            hora_retorno.split(":")
        )


        # Convertimos la salida a minutos
        salida = hora_salida * 60 + minuto_salida


        # Convertimos el retorno a minutos
        retorno = hora_retorno * 60 + minuto_retorno


        # Calculamos los minutos utilizados
        minutos = retorno - salida


        # Convertimos los minutos a horas
        horas = minutos / 60


        # Calculamos el precio
        costo = horas * self._tarifa_hora


        # Devolvemos el precio
        return costo


    #identificamos la herramienta

    # Esta función devuelve el ID
    def obtener_id(self):

        return self._id_herramienta


   #nombe de la herramienta

    # Esta función devuelve el nombre
    def obtener_nombre(self):

        return self._nombre


#creamos litsa de herramientas

# Creamos una lista vacía
herramientas = []


# Creamos el Taladro
herramientas.append(
    HerramientaAlquiler(
        1,
        "Drill",
        5000
    )
)


# Creamos la Sierra eléctrica
herramientas.append(
    HerramientaAlquiler(
        2,
        "electric saw",
        8000
    )
)


# Creamos la Pulidora
herramientas.append(
    HerramientaAlquiler(
        3,
        "Polisher",
        10000
    )
)


# Creamos la Lijadora
herramientas.append(
    HerramientaAlquiler(
        4,
        "sander",
        7000
    )
)


#Buscar herramientas

# Esta función busca una herramienta por su ID
def buscar_herramienta(id_herramienta):

    # Recorremos la lista de herramientas
    for herramienta in herramientas:

        # Revisamos si el ID coincide
        if herramienta.obtener_id() == id_herramienta:

            # Devolvemos la herramienta
            return herramienta


    # Si no encontramos la herramienta
    return None


##limpiar resultados

# Esta función borra los resultados anteriores
def limpiar_resultados(event=None):

    # Borramos el mensaje de estado
    estado.config(
        text="New tool selected.",
        fg=COLOR_GRIS
    )


    # Borramos la información anterior
    informacion.config(
        text="Here will appear the rental information."
    )


    # Borramos el tiempo anterior
    tiempo_resultado.config(
        text="--",
        fg=COLOR_GRIS
    )


    # Borramos el valor anterior
    costo_resultado.config(
        text="$ --",
        fg=COLOR_GRIS
    )


#registrar salida

# Esta función se ejecuta al presionar
# el botón "Registrar salida"
def registrar_salida():

    # Obtenemos la herramienta seleccionada
    seleccion = combo_herramientas.get()

    # Obtenemos la hora seleccionada
    hora = combo_hora.get()


    # Revisamos si seleccionó una herramienta
    if seleccion == "":

        # Mostramos un mensaje de error
        estado.config(
            text="Select a tool.",
            fg=COLOR_ROJO
        )

        return


    # Revisamos si seleccionó una hora
    if hora == "":

        # Mostramos un mensaje de error
        estado.config(
            text="Select a time.",
            fg=COLOR_ROJO
        )

        return


    # Sacamos el ID de la herramienta
    id_herramienta = int(
        seleccion.split(" - ")[0]
    )


    # Buscamos la herramienta
    herramienta = buscar_herramienta(
        id_herramienta
    )


    # Revisamos si la herramienta ya está alquilada
    if herramienta._hora_salida is not None:

        estado.config(
            text="This tool is already rented.",
            fg=COLOR_ROJO
        )

        return


    # Registramos la salida
    herramienta.registrar_salida(hora)


    # Mostramos mensaje de confirmación
    estado.config(
        text="✓Successfully registered output ",
        fg=COLOR_VERDE
    )


    # Mostramos la información
    informacion.config(
        text=(
            "Tool: "
            + herramienta.obtener_nombre()
            + "\nHour of departure: "
            + hora
        )
    )


    # Dejamos los resultados vacíos
    tiempo_resultado.config(
        text="--",
        fg=COLOR_GRIS
    )


    costo_resultado.config(
        text="$ --",
        fg=COLOR_GRIS
    )


#registrar retorno

# Esta función se ejecuta al presionar
# el botón "Registrar retorno"
def registrar_retorno():

    # Obtenemos la herramienta seleccionada
    seleccion = combo_herramientas.get()

    # Obtenemos la hora seleccionada
    hora = combo_hora.get()


    # Revisamos si seleccionó una herramienta
    if seleccion == "":

        estado.config(
            text="Select a tool.",
            fg=COLOR_ROJO
        )

        return


    # Revisamos si seleccionó una hora
    if hora == "":

        estado.config(
            text="Select a time.",
            fg=COLOR_ROJO
        )

        return


    # Sacamos el ID
    id_herramienta = int(
        seleccion.split(" - ")[0]
    )


    # Buscamos la herramienta
    herramienta = buscar_herramienta(
        id_herramienta
    )


    # Revisamos si existe una salida
    if herramienta._hora_salida is None:

        estado.config(
            text="First you must register the departure.",
            fg=COLOR_ROJO
        )

        return


    # Revisamos si el retorno es correcto
    if herramienta.registrar_retorno(hora):

        # Calculamos el tiempo
        horas, minutos = herramienta.calcular_tiempo(
            hora
        )


        # Calculamos el costo
        costo = herramienta.calcular_costo(
            hora
        )


        # Mostramos el tiempo utilizado
        tiempo_resultado.config(
            text=(
                str(horas)
                + " horas y "
                + str(minutos)
                + " minutos"
            ),
            fg=COLOR_VERDE
        )


        # Mostramos el valor a pagar
        costo_resultado.config(
            text="$" + f"{costo:,.0f}",
            fg=COLOR_VERDE
        )


        # Mostramos toda la información
        informacion.config(
            text=(
                "Tool: "
                + herramienta.obtener_nombre()
                + "\nHour of departure: "
                + herramienta._hora_salida
                + "\nHour of return: "
                + hora
            )
        )


        # Mostramos mensaje correcto
        estado.config(
            text="✓Rental completed successfully ",
            fg=COLOR_VERDE
        )


        # Quitamos la hora de salida
        # para indicar que ya terminó el alquiler
        herramienta._hora_salida = None


    else:

        # Mostramos el error
        estado.config(
            text=(
                "The return time cannot"
                "to be prior to departure."
            ),
            fg=COLOR_ROJO
        )




# Creamos la ventana principal
ventana = tk.Tk()


# Ponemos el nombre de la ventana
ventana.title(
    "Tool Rental Shop"
)



# Aquí puedes cambiar el tamaño de la ventana
ventana.geometry(
    str(ANCHO_VENTANA)
    + "x"
    + str(ALTO_VENTANA)
)


# Hacemos que la ventana sea redimensionable

ventana.resizable(
    True,
    True
)


# Ponemos el fondo blanco
ventana.configure(
    bg=COLOR_BLANCO
)




# Creamos el encabezado naranja
encabezado = tk.Frame(
    ventana,
    bg=COLOR_NARANJA,
    height=90
)


# Colocamos el encabezado
encabezado.pack(
    fill="x"
)


# Creamos el título
titulo = tk.Label(
    encabezado,
    text="TOOLS RENTAL",
    bg=COLOR_NARANJA,
    fg=COLOR_BLANCO,
    font=(
        TIPO_LETRA,
        TAMAÑO_TITULO,
        "bold"
    )
)


# Colocamos el título
titulo.pack(
    pady=25
)




# Creamos un espacio para los controles
contenido = tk.Frame(
    ventana,
    bg=COLOR_BLANCO
)


# Colocamos el contenido
contenido.pack(
    pady=20
)


#tools

# Creamos el texto "Herramienta"
label_herramienta = tk.Label(
    contenido,
    text="Tools:",
    bg=COLOR_BLANCO,
    fg=COLOR_GRIS,
    font=(
        TIPO_LETRA,
        TAMAÑO_NORMAL,
        "bold"
    )
)


# Colocamos el texto
label_herramienta.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)


# Creamos el menú desplegable
combo_herramientas = ttk.Combobox(
    contenido,
    width=30,
    state="readonly"
)


# Colocamos el menú
combo_herramientas.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Creamos una lista para mostrar las herramientas
lista_herramientas = []


# Recorremos las herramientas
for herramienta in herramientas:

    # Creamos un texto como:
    # 1 - Taladro
    texto = (
        str(herramienta.obtener_id())
        + " - "
        + herramienta.obtener_nombre()
    )


    # Agregamos el texto a la lista
    lista_herramientas.append(
        texto
    )


# Colocamos las herramientas
# dentro del menú desplegable
combo_herramientas["values"] = (
    lista_herramientas
)




# Cuando el usuario selecciona otra herramienta,
# se ejecuta automáticamente limpiar_resultados()
combo_herramientas.bind(
    "<<ComboboxSelected>>",
    limpiar_resultados
)


#hora

# Creamos el texto "Hora"
label_hora = tk.Label(
    contenido,
    text="Hour:",
    bg=COLOR_BLANCO,
    fg=COLOR_GRIS,
    font=(
        TIPO_LETRA,
        TAMAÑO_NORMAL,
        "bold"
    )
)


# Colocamos el texto
label_hora.grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)


# Creamos el menú de horas
combo_hora = ttk.Combobox(
    contenido,
    width=15,
    state="readonly"
)


# Colocamos el menú
combo_hora.grid(
    row=1,
    column=1,
    sticky="w",
    padx=10,
    pady=10
)


# Creamos una lista para guardar las horas
horas = []


# Recorremos las 24 horas
for hora in range(24):

    # Recorremos los minutos de 15 en 15
    for minuto in range(0, 60, 15):

        # Creamos una hora como 08:30
        hora_completa = (
            f"{hora:02d}:{minuto:02d}"
        )


        # Guardamos la hora
        horas.append(
            hora_completa
        )


# Colocamos las horas en el desplegable
combo_hora["values"] = horas




# Creamos un espacio para los botones
botones = tk.Frame(
    contenido,
    bg=COLOR_BLANCO
)


# Colocamos el espacio
botones.grid(
    row=2,
    column=0,
    columnspan=2,
    pady=20
)




# Creamos el botón de salida
boton_salida = tk.Button(
    botones,
    text="CHECK OUT",
    bg=COLOR_AZUL,
    fg=COLOR_BLANCO,
    font=(
        TIPO_LETRA,
        11,
        "bold"
    ),
    width=20,
    height=2,
    command=registrar_salida
)


# Colocamos el botón
boton_salida.grid(
    row=0,
    column=0,
    padx=10
)


#boton de retorno

# Creamos el botón de retorno
boton_retorno = tk.Button(
    botones,
    text="RECORD RETURN",
    bg=COLOR_VERDE,
    fg=COLOR_BLANCO,
    font=(
        TIPO_LETRA,
        11,
        "bold"
    ),
    width=20,
    height=2,
    command=registrar_retorno
)


# Colocamos el botón al lado
boton_retorno.grid(
    row=0,
    column=1,
    padx=10
)


#estado de la aplicación

# Creamos un texto para mostrar el estado
estado = tk.Label(
    ventana,
    text="Select a tool and a time.",
    bg=COLOR_BLANCO,
    fg=COLOR_GRIS,
    font=(
        TIPO_LETRA,
        11,
        "bold"
    )
)


# Colocamos el estado
estado.pack(
    pady=5
)


#información del alquiler

# Creamos un texto para mostrar información
informacion = tk.Label(
    ventana,
    text="The rental information will appear here.",
    bg=COLOR_BLANCO,
    fg=COLOR_GRIS,
    font=(
        TIPO_LETRA,
        11
    ),
    justify="center"
)


# Colocamos la información
informacion.pack(
    pady=10
)


#cajetines de resultados

# Creamos un espacio para los cajetines
resultados = tk.Frame(
    ventana,
    bg=COLOR_BLANCO
)


# Colocamos los cajetines
resultados.pack(
    pady=10
)


#tiempo de alquiler

# Creamos el cajetín
caja_tiempo = tk.Frame(
    resultados,
    bg="#F5F5F5",
    bd=2,
    relief="solid",
    width=270,
    height=100
)


# Lo colocamos a la izquierda
caja_tiempo.grid(
    row=0,
    column=0,
    padx=10
)


# Título del cajetín
titulo_tiempo = tk.Label(
    caja_tiempo,
    text="TIME OF USE",
    bg="#F5F5F5",
    fg=COLOR_AZUL,
    font=(
        TIPO_LETRA,
        11,
        "bold"
    )
)


# Colocamos el título
titulo_tiempo.pack(
    pady=10
)


# Resultado del tiempo
tiempo_resultado = tk.Label(
    caja_tiempo,
    text="--",
    bg="#F5F5F5",
    fg=COLOR_GRIS,
    font=(
        TIPO_LETRA,
        TAMAÑO_RESULTADO,
        "bold"
    )
)


# Colocamos el resultado
tiempo_resultado.pack()


#valor a pagar
# Creamos el cajetín
caja_costo = tk.Frame(
    resultados,
    bg="#F5F5F5",
    bd=2,
    relief="solid",
    width=270,
    height=100
)


# Lo colocamos al lado
caja_costo.grid(
    row=0,
    column=1,
    padx=10
)


# Título del cajetín
titulo_costo = tk.Label(
    caja_costo,
    text="AMOUNT TO PAY",
    bg="#F5F5F5",
    fg=COLOR_NARANJA,
    font=(
        TIPO_LETRA,
        11,
        "bold"
    )
)


# Colocamos el título
titulo_costo.pack(
    pady=10
)


# Resultado del costo
costo_resultado = tk.Label(
    caja_costo,
    text="$ --",
    bg="#F5F5F5",
    fg=COLOR_GRIS,
    font=(
        TIPO_LETRA,
        TAMAÑO_RESULTADO,
        "bold"
    )
)


# Colocamos el resultado
costo_resultado.pack()



# Creamos un texto pequeño para mostrar el horario disponible
pie = tk.Label(
    ventana,
    text="Available schedule: 00:00 until 23:45",
    bg=COLOR_BLANCO,
    fg="#777777",
    font=(
        TIPO_LETRA,
        9
    )
)


# Colocamos el texto
pie.pack(
    pady=10
)


#inicio de la ventana

# Mantenemos la ventana abierta
ventana.mainloop()
