"""
sistema.py
Clase SistemaGestion: guarda clientes, servicios y reservas en LISTAS
(no hay base de datos) y captura los errores para que el programa siga activo.
"""

from cliente import Cliente             # Clase para crear clientes
from reserva import Reserva             # Clase para crear reservas
from excepciones import ErrorSoftwareFJ, OperacionNoPermitidaError   # Errores que se capturan o se lanzan aquí
from registro import registrar_evento, registrar_error               # Funciones que escriben en el log


# Clase que coordina todo el sistema
class SistemaGestion:
    """Administra las listas internas del sistema."""

    # Constructor: crea las tres listas vacías
    def __init__(self):
        """Prepara las listas donde se guardan los objetos."""
        self._clientes = []     # Lista interna de objetos Cliente
        self._servicios = []    # Lista interna de objetos Servicio
        self._reservas = []     # Lista interna de objetos Reserva

    # Los parámetros valen None por defecto para poder detectar datos faltantes
    def registrar_cliente(self, nombre=None, documento=None, correo=None, telefono=None):
        """Crea un cliente. Usa try / except / else."""
        try:                                                            # Bloque que puede fallar
            cliente = Cliente(nombre, documento, correo, telefono)      # Crea el cliente; lanza excepción si un dato es inválido
            for existente in self._clientes:                            # Recorre los clientes ya guardados
                if existente.documento == cliente.documento:            # Si otro cliente ya tiene ese documento
                    raise OperacionNoPermitidaError(
                        f"Ya existe un cliente con documento {cliente.documento}.")   # Lanza error por duplicado
        except ErrorSoftwareFJ as error:                                # Captura cualquier error propio del sistema
            registrar_error(error, "Registro de cliente")               # Guarda el error en el log
            print(f"  ✗ Cliente rechazado: {error}")                    # Avisa en pantalla sin detener el programa
            return None                                                 # Devuelve None porque no se creó el cliente
        else:                                                           # Se ejecuta solo si no hubo errores
            self._clientes.append(cliente)                              # Agrega el cliente a la lista
            registrar_evento(f"Cliente registrado: {cliente.describir()}")   # Guarda el evento en el log
            print(f"  ✓ {cliente}")                                     # Muestra el cliente en pantalla
            return cliente                                              # Devuelve el cliente creado

    # clase_servicio es la clase a crear; *argumentos recoge los demás datos, sean cuantos sean
    def crear_servicio(self, clase_servicio, *argumentos):
        """Crea un servicio de cualquier tipo. Usa try / except / else."""
        try:                                                # Bloque que puede fallar
            servicio = clase_servicio(*argumentos)          # Polimorfismo: crea el servicio de la clase recibida
        except ErrorSoftwareFJ as error:                    # Captura los errores propios del sistema
            registrar_error(error, "Creación de servicio")  # Guarda el error en el log
            print(f"  ✗ Servicio rechazado: {error}")       # Avisa en pantalla sin detener el programa
            return None                                     # Devuelve None porque no se creó el servicio
        except TypeError as error:                          # Captura el error de Python por argumentos de más o de menos
            registrar_error(error, "Creación de servicio (argumentos)")               # Guarda el error en el log
            print(f"  ✗ Servicio rechazado: argumentos incorrectos ({error})")        # Avisa en pantalla
            return None                                     # Devuelve None porque no se creó el servicio
        else:                                               # Se ejecuta solo si no hubo errores
            self._servicios.append(servicio)                # Agrega el servicio a la lista
            registrar_evento(f"Servicio creado: {servicio.describir()}")   # Guarda el evento en el log
            print(f"  ✓ {servicio}")                        # Muestra el servicio en pantalla
            return servicio                                 # Devuelve el servicio creado

    # Recibe los objetos cliente y servicio, y la duración
    def crear_reserva(self, cliente, servicio, duracion):
        """Crea y confirma una reserva. Usa try / except / else / finally."""
        try:                                                # Bloque que puede fallar
            reserva = Reserva(cliente, servicio, duracion)  # Crea la reserva; lanza excepción si algo es inválido
            reserva.confirmar()                             # La pasa de PENDIENTE a CONFIRMADA
        except ErrorSoftwareFJ as error:                    # Captura los errores propios del sistema
            registrar_error(error, "Creación de reserva")   # Guarda el error en el log
            print(f"  ✗ Reserva rechazada: {error}")        # Avisa en pantalla sin detener el programa
            return None                                     # Devuelve None porque no se creó la reserva
        else:                                               # Se ejecuta solo si no hubo errores
            self._reservas.append(reserva)                  # Agrega la reserva a la lista
            print(f"  ✓ {reserva}")                         # Muestra la reserva en pantalla
            return reserva                                  # Devuelve la reserva creada
        finally:                                            # Se ejecuta siempre, con o sin error
            registrar_evento("Intento de reserva finalizado.")   # Deja rastro del intento en el log

    # impuesto y descuento son opcionales
    def procesar_reserva(self, reserva, impuesto=None, descuento=None):
        """Procesa una reserva y muestra la causa original si falla."""
        try:                                                # Bloque que puede fallar
            if reserva is None:                             # Si la reserva nunca se creó
                raise OperacionNoPermitidaError("No hay reserva para procesar.")      # Lanza error de operación no permitida
            costo = reserva.procesar(impuesto, descuento)   # Cobra la reserva; puede lanzar una excepción encadenada
        except ErrorSoftwareFJ as error:                    # Captura los errores propios del sistema
            registrar_error(error, "Procesamiento de reserva")   # Guarda el error en el log
            print(f"  ✗ {error}")                           # Avisa en pantalla sin detener el programa
            if error.__cause__ is not None:                 # Si el error trae otro error encadenado
                print(f"    Causa: {error.__cause__}")      # Muestra también el error original
            return None                                     # Devuelve None porque no se procesó
        else:                                               # Se ejecuta solo si no hubo errores
            print(f"  ✓ Reserva #{reserva.id} procesada. Total: ${costo:,.2f}")       # Muestra el total cobrado
            return costo                                    # Devuelve el costo

    # Recibe la reserva que se quiere anular
    def cancelar_reserva(self, reserva):
        """Cancela una reserva. Usa try / except."""
        try:                                                # Bloque que puede fallar
            if reserva is None:                             # Si la reserva nunca se creó
                raise OperacionNoPermitidaError("No hay reserva para cancelar.")      # Lanza error de operación no permitida
            reserva.cancelar()                              # Cancela; lanza excepción si ya estaba cancelada o procesada
            print(f"  ✓ Reserva #{reserva.id} cancelada.")  # Confirma la cancelación en pantalla
        except ErrorSoftwareFJ as error:                    # Captura los errores propios del sistema
            registrar_error(error, "Cancelación de reserva")     # Guarda el error en el log
            print(f"  ✗ {error}")                           # Avisa en pantalla sin detener el programa

    # Muestra todo lo que quedó guardado
    def mostrar_resumen(self):
        """Imprime el contenido de las tres listas."""
        print(f"\nClientes registrados: {len(self._clientes)}")   # len() cuenta los elementos de la lista
        for cliente in self._clientes:                # Recorre la lista de clientes
            print(f"  - {cliente}")                   # Imprime cada cliente
        print(f"Servicios creados: {len(self._servicios)}")       # Cantidad de servicios
        for servicio in self._servicios:              # Recorre la lista de servicios
            print(f"  - {servicio}")                  # Polimorfismo: cada servicio se describe a su manera
        print(f"Reservas guardadas: {len(self._reservas)}")       # Cantidad de reservas
        for reserva in self._reservas:                # Recorre la lista de reservas
            print(f"  - {reserva}")                   # Imprime cada reserva
