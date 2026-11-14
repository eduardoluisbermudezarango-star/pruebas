"""
cliente.py
Clase Cliente: datos personales encapsulados y validaciones estrictas.
"""

import re                               # Módulo de expresiones regulares, para validar el formato del correo
from entidad import Entidad             # Clase abstracta de la que hereda Cliente
from excepciones import DatoInvalidoError, ParametroFaltanteError   # Errores que puede lanzar esta clase


# Cliente hereda de Entidad, así que recibe el id y debe escribir describir() y validar()
class Cliente(Entidad):
    """Cliente de Software FJ."""

    # Constructor: recibe los cuatro datos personales
    def __init__(self, nombre, documento, correo, telefono):
        """Crea el cliente; si algún dato es incorrecto se lanza una excepción y el cliente no se crea."""
        super().__init__()              # Ejecuta el constructor de Entidad, que genera el id
        self.nombre = nombre            # Pasa por el setter de nombre, que lo valida
        self.documento = documento      # Pasa por el setter de documento, que lo valida
        self.correo = correo            # Pasa por el setter de correo, que lo valida
        self.telefono = telefono        # Pasa por el setter de teléfono, que lo valida

    # ---------- nombre ----------
    # Getter: permite leer el nombre con cliente.nombre
    @property
    def nombre(self):
        """Devuelve el nombre."""
        return self.__nombre            # El doble guion bajo hace el atributo privado (encapsulación)

    # Setter: se ejecuta cada vez que se asigna cliente.nombre = algo
    @nombre.setter
    def nombre(self, valor):
        """Valida el nombre antes de guardarlo."""
        if valor is None or str(valor).strip() == "":               # Si no llegó nada o llegó solo espacios
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")   # Lanza error de dato faltante
        valor = str(valor).strip()                                  # Lo convierte en texto y quita espacios de los extremos
        if len(valor) < 3:                                          # Si tiene menos de 3 caracteres
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")  # Lanza error de dato inválido
        if not all(c.isalpha() or c.isspace() for c in valor):      # Revisa carácter por carácter: solo letras o espacios
            raise DatoInvalidoError(f"El nombre '{valor}' solo puede contener letras.")   # Lanza error si hay números o símbolos
        self.__nombre = valor.title()                               # Guarda el nombre con mayúscula inicial en cada palabra

    # ---------- documento ----------
    # Getter: permite leer el documento con cliente.documento
    @property
    def documento(self):
        """Devuelve el documento."""
        return self.__documento         # Atributo privado

    # Setter: valida el documento al asignarlo
    @documento.setter
    def documento(self, valor):
        """Valida el documento antes de guardarlo."""
        if valor is None or str(valor).strip() == "":               # Si no llegó nada
            raise ParametroFaltanteError("El documento del cliente es obligatorio.")   # Lanza error de dato faltante
        try:                                                        # Bloque que puede fallar
            numero = int(str(valor).strip())                        # Intenta convertir el texto en número entero
        except ValueError as error:                                 # Se ejecuta si el texto tenía letras o símbolos
            # Encadenamiento: se lanza el error propio y "from error" conserva el ValueError original como causa
            raise DatoInvalidoError(
                f"El documento '{valor}' debe ser numérico."
            ) from error
        if numero <= 0 or not 6 <= len(str(numero)) <= 10:          # Debe ser positivo y tener entre 6 y 10 dígitos
            raise DatoInvalidoError("El documento debe tener entre 6 y 10 dígitos.")   # Lanza error si no cumple
        self.__documento = str(numero)                              # Guarda el documento como texto

    # ---------- correo ----------
    # Getter: permite leer el correo con cliente.correo
    @property
    def correo(self):
        """Devuelve el correo."""
        return self.__correo            # Atributo privado

    # Setter: valida el correo al asignarlo
    @correo.setter
    def correo(self, valor):
        """Valida el correo antes de guardarlo."""
        if valor is None or str(valor).strip() == "":               # Si no llegó nada
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")   # Lanza error de dato faltante
        valor = str(valor).strip().lower()                          # Quita espacios y lo pasa a minúsculas
        patron = r"^[\w\.-]+@[\w\.-]+\.[a-z]{2,}$"                  # Molde del correo: usuario @ dominio . extensión
        if not re.match(patron, valor):                             # Compara el correo contra el molde
            raise DatoInvalidoError(f"El correo '{valor}' no tiene un formato válido.")   # Lanza error si no coincide
        self.__correo = valor                                       # Guarda el correo

    # ---------- teléfono ----------
    # Getter: permite leer el teléfono con cliente.telefono
    @property
    def telefono(self):
        """Devuelve el teléfono."""
        return self.__telefono          # Atributo privado

    # Setter: valida el teléfono al asignarlo
    @telefono.setter
    def telefono(self, valor):
        """Valida el teléfono antes de guardarlo."""
        if valor is None or str(valor).strip() == "":               # Si no llegó nada
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")   # Lanza error de dato faltante
        valor = str(valor).strip()                                  # Lo convierte en texto y quita espacios
        if not valor.isdigit() or len(valor) != 10:                 # Debe tener solo dígitos y exactamente 10
            raise DatoInvalidoError(f"El teléfono '{valor}' debe tener 10 dígitos.")   # Lanza error si no cumple
        self.__telefono = valor                                     # Guarda el teléfono

    # ---------- métodos sobrescritos de Entidad ----------
    # Implementación del método abstracto validar()
    def validar(self):
        """Si el objeto existe, sus datos ya pasaron por los setters."""
        return True                     # Devuelve verdadero porque un cliente creado siempre es válido

    # Implementación del método abstracto describir()
    def describir(self):
        """Devuelve un texto con los datos del cliente, ocultando parte del documento."""
        oculto = "*" * (len(self.__documento) - 3) + self.__documento[-3:]   # Asteriscos y solo los 3 últimos dígitos
        return f"Cliente #{self.id}: {self.__nombre} | Doc: {oculto} | {self.__correo}"   # Texto final del cliente
