"""
entidad.py
Clase abstracta que representa cualquier entidad general del sistema
(clientes, servicios y reservas heredan de ella).
"""

from abc import ABC, abstractmethod   # ABC permite crear clases abstractas; abstractmethod marca métodos obligatorios


# Clase abstracta: al heredar de ABC no se pueden crear objetos Entidad directamente
class Entidad(ABC):
    """Clase abstracta base. No se puede instanciar directamente."""

    _contador = 0   # Atributo de clase: consecutivo compartido por todas las entidades

    # Constructor: se ejecuta cada vez que se crea un cliente, un servicio o una reserva
    def __init__(self):
        """Asigna un identificador único a la entidad."""
        Entidad._contador += 1              # Suma 1 al consecutivo general
        self._id = Entidad._contador        # Guarda ese número como identificador del objeto

    # @property convierte el método en un atributo de solo lectura: se usa objeto.id
    @property
    def id(self):
        """Identificador de solo lectura (encapsulación: no tiene setter)."""
        return self._id                     # Devuelve el identificador sin permitir cambiarlo

    # Método abstracto: no tiene código aquí; cada clase hija está obligada a escribirlo
    @abstractmethod
    def describir(self):
        """Cada clase hija debe devolver un texto que la describa."""

    # Método abstracto: cada clase hija define cómo revisa sus datos
    @abstractmethod
    def validar(self):
        """Cada clase hija debe comprobar que sus datos son correctos."""

    # Método especial que Python usa al hacer print(objeto)
    def __str__(self):
        """Devuelve la descripción del objeto."""
        return self.describir()             # Polimorfismo: ejecuta el describir() de la clase hija que corresponda
