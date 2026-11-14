"""
servicios.py
Clase abstracta Servicio y tres servicios especializados:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
"""

from abc import abstractmethod          # Decorador para marcar los métodos que las clases hijas deben escribir
from entidad import Entidad             # Clase abstracta base del sistema
from excepciones import (DatoInvalidoError, ParametroFaltanteError,
                         CalculoInconsistenteError)   # Errores que pueden lanzar los servicios


# Servicio hereda de Entidad y sigue siendo abstracta porque tiene métodos abstractos
class Servicio(Entidad):
    """Clase abstracta: define lo que todo servicio debe saber hacer."""

    # Constructor común a todos los servicios
    def __init__(self, nombre, tarifa_base):
        """Valida y guarda el nombre y la tarifa."""
        super().__init__()                                  # Ejecuta el constructor de Entidad, que genera el id
        if nombre is None or str(nombre).strip() == "":     # Si el nombre no llegó o está vacío
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")   # Lanza error de dato faltante
        if not isinstance(tarifa_base, (int, float)) or isinstance(tarifa_base, bool):   # Si la tarifa no es un número
            raise DatoInvalidoError("La tarifa base debe ser un número.")            # Lanza error de dato inválido
        if tarifa_base <= 0:                                # Si la tarifa es cero o negativa
            raise DatoInvalidoError("La tarifa base debe ser mayor que cero.")       # Lanza error de dato inválido
        self._nombre = str(nombre).strip()                  # Guarda el nombre (un guion bajo: atributo protegido)
        self._tarifa_base = float(tarifa_base)              # Guarda la tarifa como número decimal
        self._disponible = True                             # Todo servicio se crea disponible

    # Propiedad de solo lectura para consultar el nombre
    @property
    def nombre(self):
        """Devuelve el nombre del servicio."""
        return self._nombre                                 # Entrega el nombre sin permitir modificarlo

    # Propiedad de solo lectura para consultar la tarifa
    @property
    def tarifa_base(self):
        """Devuelve la tarifa base."""
        return self._tarifa_base                            # Entrega la tarifa sin permitir modificarla

    # Propiedad de solo lectura para saber si se puede reservar
    @property
    def disponible(self):
        """Devuelve True si el servicio está disponible."""
        return self._disponible                             # Entrega el estado de disponibilidad

    # Método para activar o desactivar el servicio
    def cambiar_disponibilidad(self, estado):
        """Activa o desactiva el servicio."""
        self._disponible = bool(estado)                     # Convierte el valor recibido en verdadero o falso y lo guarda

    # Implementación del método abstracto validar() de Entidad
    def validar(self):
        """Un servicio es válido si tiene tarifa positiva."""
        return self._tarifa_base > 0                        # Devuelve True si la tarifa es mayor que cero

    # Método abstracto: cada servicio lo escribe con su propia fórmula
    @abstractmethod
    def costo_base(self, duracion):
        """Cada servicio calcula su costo sin impuestos de forma distinta."""

    # Método abstracto: cada servicio lo escribe con sus propios límites
    @abstractmethod
    def validar_parametros(self, duracion):
        """Cada servicio tiene sus propios límites de duración."""

    # Método sobrecargado: impuesto y descuento son opcionales (valen None si no se envían)
    def calcular_costo(self, duracion, impuesto=None, descuento=None):
        """
        MÉTODO SOBRECARGADO. Python no permite repetir el nombre de un método
        con distintas firmas, así que la sobrecarga se logra con parámetros
        opcionales. Admite tres variantes:
            calcular_costo(duracion)                        -> costo base
            calcular_costo(duracion, impuesto)              -> con impuesto
            calcular_costo(duracion, impuesto, descuento)   -> con impuesto y descuento
        impuesto y descuento se expresan en porcentaje (19 significa 19 %).
        """
        self.validar_parametros(duracion)               # Revisa la duración con las reglas del servicio concreto
        total = self.costo_base(duracion)               # Polimorfismo: usa la fórmula de la clase hija
        if descuento is not None:                       # Solo entra si se envió un descuento
            if not 0 <= descuento <= 100:               # El descuento debe estar entre 0 y 100
                raise CalculoInconsistenteError(
                    f"Descuento de {descuento}% fuera del rango 0-100.")   # Lanza error de cálculo
            total -= total * descuento / 100            # Resta al total el porcentaje de descuento
        if impuesto is not None:                        # Solo entra si se envió un impuesto
            if impuesto < 0:                            # El impuesto no puede ser negativo
                raise CalculoInconsistenteError(
                    f"Impuesto de {impuesto}% no puede ser negativo.")     # Lanza error de cálculo
            total += total * impuesto / 100             # Suma al total el porcentaje de impuesto
        if total < 0:                                   # Revisión final: el resultado no puede ser negativo
            raise CalculoInconsistenteError("El costo calculado resultó negativo.")   # Lanza error de cálculo
        return round(total, 2)                          # Devuelve el total redondeado a dos decimales

    # Método de apoyo que usan las tres clases hijas
    def _validar_duracion_numerica(self, duracion):
        """Validación común a todos los servicios."""
        if duracion is None:                            # Si no se envió la duración
            raise ParametroFaltanteError("La duración es obligatoria.")              # Lanza error de dato faltante
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool):     # Si la duración no es un número
            raise DatoInvalidoError(f"La duración '{duracion}' debe ser numérica.")  # Lanza error de dato inválido
        if duracion <= 0:                               # Si la duración es cero o negativa
            raise DatoInvalidoError("La duración debe ser mayor que cero.")          # Lanza error de dato inválido


# Primer servicio especializado: hereda de Servicio
class ReservaSala(Servicio):
    """Reserva de salas: se cobra por hora y hay recargo en salas grandes."""

    # Constructor: además de nombre y tarifa recibe la capacidad de la sala
    def __init__(self, nombre, tarifa_hora, capacidad):
        """Crea la sala y valida su capacidad."""
        super().__init__(nombre, tarifa_hora)               # El constructor de Servicio valida nombre y tarifa
        if not isinstance(capacidad, int) or capacidad <= 0:   # La capacidad debe ser un entero mayor que cero
            raise DatoInvalidoError("La capacidad debe ser un entero positivo.")     # Lanza error de dato inválido
        self._capacidad = capacidad                         # Guarda el número de personas

    # Método sobrescrito: reglas de duración de las salas
    def validar_parametros(self, duracion):
        """Una sala se reserva entre más de 0 y 12 horas."""
        self._validar_duracion_numerica(duracion)           # Primero la validación común
        if duracion > 12:                                   # Regla propia: máximo 12 horas
            raise DatoInvalidoError("Una sala se reserva máximo por 12 horas.")      # Lanza error si se pasa

    # Método sobrescrito: fórmula de costo de las salas
    def costo_base(self, duracion):
        """Tarifa por hora, con recargo del 15 % si la sala es de más de 20 personas."""
        costo = self._tarifa_base * duracion                # Multiplica la tarifa por las horas
        if self._capacidad > 20:                            # Si la sala es grande
            costo *= 1.15                                   # Aumenta el costo en 15 %
        return costo                                        # Devuelve el costo sin impuestos

    # Método sobrescrito: descripción de la sala
    def describir(self):
        """Devuelve un texto con los datos de la sala."""
        return (f"Servicio #{self.id}: Sala '{self._nombre}' | "
                f"{self._capacidad} personas | ${self._tarifa_base:,.0f}/hora")   # Tarifa con separador de miles


# Segundo servicio especializado: hereda de Servicio
class AlquilerEquipo(Servicio):
    """Alquiler de equipos: se cobra por día y por cantidad de equipos."""

    # Constructor: además de nombre y tarifa recibe cuántos equipos se alquilan
    def __init__(self, nombre, tarifa_dia, cantidad):
        """Crea el alquiler y valida la cantidad."""
        super().__init__(nombre, tarifa_dia)                # El constructor de Servicio valida nombre y tarifa
        if not isinstance(cantidad, int) or cantidad <= 0:  # La cantidad debe ser un entero mayor que cero
            raise DatoInvalidoError("La cantidad de equipos debe ser un entero positivo.")   # Lanza error de dato inválido
        self._cantidad = cantidad                           # Guarda la cantidad de equipos

    # Método sobrescrito: reglas de duración del alquiler
    def validar_parametros(self, duracion):
        """El alquiler es por días completos y máximo 30."""
        self._validar_duracion_numerica(duracion)           # Primero la validación común
        if duracion != int(duracion):                       # Si tiene decimales (ej.: 2.5 días)
            raise DatoInvalidoError("El alquiler se hace por días completos.")       # Lanza error de dato inválido
        if duracion > 30:                                   # Regla propia: máximo 30 días
            raise DatoInvalidoError("El alquiler máximo es de 30 días.")             # Lanza error si se pasa

    # Método sobrescrito: fórmula de costo del alquiler
    def costo_base(self, duracion):
        """Tarifa por día y por equipo, con rebaja del 10 % desde 7 días."""
        costo = self._tarifa_base * duracion * self._cantidad   # Tarifa por días por número de equipos
        if duracion >= 7:                                       # Si el alquiler es de una semana o más
            costo *= 0.90                                       # Rebaja el costo en 10 %
        return costo                                            # Devuelve el costo sin impuestos

    # Método sobrescrito: descripción del alquiler
    def describir(self):
        """Devuelve un texto con los datos del alquiler."""
        return (f"Servicio #{self.id}: Alquiler '{self._nombre}' | "
                f"{self._cantidad} equipo(s) | ${self._tarifa_base:,.0f}/día")   # Tarifa con separador de miles


# Tercer servicio especializado: hereda de Servicio
class AsesoriaEspecializada(Servicio):
    """Asesorías: se cobran por hora según el nivel del asesor."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}   # Diccionario: nivel -> número que multiplica la tarifa

    # Constructor: además de nombre y tarifa recibe el nivel del asesor
    def __init__(self, nombre, tarifa_hora, nivel):
        """Crea la asesoría y valida el nivel."""
        super().__init__(nombre, tarifa_hora)                   # El constructor de Servicio valida nombre y tarifa
        try:                                                    # Bloque que puede fallar
            self._factor = self.NIVELES[str(nivel).lower()]     # Busca el nivel en el diccionario y guarda su multiplicador
        except KeyError as error:                               # Se ejecuta si el nivel no está en el diccionario
            # Encadenamiento: se lanza el error propio y "from error" conserva el KeyError original como causa
            raise DatoInvalidoError(
                f"Nivel '{nivel}' no existe. Use: junior, senior o experto."
            ) from error
        self._nivel = str(nivel).lower()                        # Guarda el nivel en minúsculas

    # Método sobrescrito: reglas de duración de las asesorías
    def validar_parametros(self, duracion):
        """Una asesoría dura entre más de 0 y 8 horas."""
        self._validar_duracion_numerica(duracion)           # Primero la validación común
        if duracion > 8:                                    # Regla propia: máximo 8 horas
            raise DatoInvalidoError("Una asesoría dura máximo 8 horas.")             # Lanza error si se pasa

    # Método sobrescrito: fórmula de costo de las asesorías
    def costo_base(self, duracion):
        """Tarifa por hora multiplicada por el factor del nivel."""
        return self._tarifa_base * duracion * self._factor  # Tarifa por horas por multiplicador del nivel

    # Método sobrescrito: descripción de la asesoría
    def describir(self):
        """Devuelve un texto con los datos de la asesoría."""
        return (f"Servicio #{self.id}: Asesoría '{self._nombre}' | "
                f"nivel {self._nivel} | ${self._tarifa_base:,.0f}/hora")   # Tarifa con separador de miles
