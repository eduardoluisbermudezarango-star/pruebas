"""
reserva.py
Clase Reserva: une un cliente, un servicio, una duración y un estado.
"""

from entidad import Entidad             # Clase abstracta base
from cliente import Cliente             # Para comprobar que el cliente recibido es un Cliente
from servicios import Servicio          # Para comprobar que el servicio recibido es un Servicio
from excepciones import (ErrorSoftwareFJ, ParametroFaltanteError,
                         OperacionNoPermitidaError, ServicioNoDisponibleError,
                         ReservaInvalidaError)   # Errores que puede lanzar o capturar la reserva
from registro import registrar_evento   # Función que escribe eventos en el log


# Reserva hereda de Entidad: recibe el id y debe escribir describir() y validar()
class Reserva(Entidad):
    """Reserva de un servicio hecha por un cliente."""

    # Constantes con los cuatro estados posibles de una reserva
    PENDIENTE = "PENDIENTE"         # Recién creada
    CONFIRMADA = "CONFIRMADA"       # Aceptada, lista para cobrar
    CANCELADA = "CANCELADA"         # Anulada
    PROCESADA = "PROCESADA"         # Cobrada y cerrada

    # Constructor: recibe el cliente, el servicio y la duración
    def __init__(self, cliente, servicio, duracion):
        """Crea la reserva; si algo es incorrecto se lanza una excepción y no se crea."""
        super().__init__()                  # Ejecuta el constructor de Entidad, que genera el id
        self._cliente = cliente             # Guarda el objeto Cliente
        self._servicio = servicio           # Guarda el objeto Servicio (cualquiera de los tres tipos)
        self._duracion = duracion           # Guarda la duración (horas o días, según el servicio)
        self._estado = Reserva.PENDIENTE    # Toda reserva empieza en estado PENDIENTE
        self._costo_total = 0.0             # El costo empieza en cero y se calcula al procesar
        self.validar()                      # Revisa todo; si algo está mal, lanza una excepción

    # Propiedad de solo lectura para consultar el estado
    @property
    def estado(self):
        """Devuelve el estado actual."""
        return self._estado                 # Entrega el estado sin permitir modificarlo desde fuera

    # Propiedad de solo lectura para consultar el costo
    @property
    def costo_total(self):
        """Devuelve el costo total."""
        return self._costo_total            # Entrega el costo sin permitir modificarlo desde fuera

    # Implementación del método abstracto validar() de Entidad
    def validar(self):
        """Comprueba que la reserva se pueda crear."""
        if self._cliente is None or self._servicio is None:         # Si falta el cliente o el servicio
            raise ParametroFaltanteError("La reserva requiere cliente y servicio.")   # Lanza error de dato faltante
        if not isinstance(self._cliente, Cliente):                  # Si lo recibido no es un objeto Cliente
            raise ReservaInvalidaError("El cliente indicado no es válido.")           # Lanza error de reserva inválida
        if not isinstance(self._servicio, Servicio):                # Si lo recibido no es un objeto Servicio
            raise ReservaInvalidaError("El servicio indicado no es válido.")          # Lanza error de reserva inválida
        if not self._servicio.disponible:                           # Si el servicio está desactivado
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' no está disponible.")         # Lanza error de servicio no disponible
        self._servicio.validar_parametros(self._duracion)           # El servicio revisa la duración con sus propias reglas
        return True                                                 # Si llegó hasta aquí, todo está correcto

    # Método para confirmar la reserva
    def confirmar(self):
        """Pasa la reserva de PENDIENTE a CONFIRMADA."""
        if self._estado != Reserva.PENDIENTE:           # Solo se puede confirmar una reserva pendiente
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}.")       # Lanza error de operación no permitida
        self._estado = Reserva.CONFIRMADA               # Cambia el estado a CONFIRMADA
        registrar_evento(f"Reserva #{self.id} confirmada.")   # Deja constancia en el log

    # Método para cancelar la reserva
    def cancelar(self):
        """Cancela la reserva si aún no fue procesada ni cancelada."""
        if self._estado in (Reserva.CANCELADA, Reserva.PROCESADA):   # Si ya estaba cancelada o ya se cobró
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado}.")        # Lanza error de operación no permitida
        self._estado = Reserva.CANCELADA                # Cambia el estado a CANCELADA
        registrar_evento(f"Reserva #{self.id} cancelada.")    # Deja constancia en el log

    # Método para cobrar la reserva; impuesto y descuento son opcionales
    def procesar(self, impuesto=None, descuento=None):
        """
        Calcula el costo final y cierra la reserva.
        Aquí se usa el bloque completo try / except / else / finally.
        """
        if self._estado != Reserva.CONFIRMADA:          # Solo se puede procesar una reserva confirmada
            raise OperacionNoPermitidaError(
                f"Solo se procesan reservas confirmadas (estado actual: {self._estado}).")   # Lanza error de operación no permitida
        try:                                            # Bloque que puede fallar
            # Llamada polimórfica: cada tipo de servicio calcula el costo con su propia fórmula
            costo = self._servicio.calcular_costo(self._duracion, impuesto, descuento)
        except ErrorSoftwareFJ as error:                # Se ejecuta si el cálculo lanzó un error del sistema
            # Encadenamiento: se lanza un error de reserva y "from error" conserva el error del cálculo como causa
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva #{self.id}."
            ) from error
        else:                                           # Se ejecuta solo si el try terminó SIN errores
            self._costo_total = costo                   # Guarda el costo calculado
            self._estado = Reserva.PROCESADA            # Cambia el estado a PROCESADA
            registrar_evento(f"Reserva #{self.id} procesada. Total: ${costo:,.2f}")   # Deja constancia en el log
            return costo                                # Devuelve el costo a quien llamó el método
        finally:                                        # Se ejecuta SIEMPRE, con o sin error
            registrar_evento(f"Fin del intento de procesamiento de la reserva #{self.id}.")   # Registra que el intento terminó

    # Implementación del método abstracto describir() de Entidad
    def describir(self):
        """Devuelve un texto con los datos de la reserva."""
        return (f"Reserva #{self.id}: {self._cliente.nombre} -> "
                f"{self._servicio.nombre} | duración {self._duracion} | "
                f"{self._estado} | ${self._costo_total:,.2f}")   # Costo con separador de miles y dos decimales
