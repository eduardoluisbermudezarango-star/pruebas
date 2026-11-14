"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.
Una excepción es un objeto que representa un error. Aquí se crean las propias
del sistema: todas heredan de ErrorSoftwareFJ, lo que permite capturarlas
todas juntas (except ErrorSoftwareFJ) o cada una por separado.
"""


# Clase base de los errores del sistema; hereda de Exception, la clase de errores de Python
class ErrorSoftwareFJ(Exception):
    """Excepción base: de ella heredan todos los errores propios del sistema."""

    # Constructor: recibe el texto del error y un código; si no se da código, usa "ERR-000"
    def __init__(self, mensaje, codigo="ERR-000"):
        """Guarda el mensaje y el código del error."""
        super().__init__(mensaje)   # Llama al constructor de Exception y le entrega el mensaje
        self.mensaje = mensaje      # Guarda el texto del error dentro del objeto
        self.codigo = codigo        # Guarda el código que identifica el tipo de error

    # Método especial que Python usa cuando el error se convierte en texto (print o str)
    def __str__(self):
        """Devuelve el error con el formato [CÓDIGO] mensaje."""
        return f"[{self.codigo}] {self.mensaje}"   # Ejemplo: [ERR-001] El correo no es válido


# Error para datos con formato o valor no permitido; hereda de ErrorSoftwareFJ
class DatoInvalidoError(ErrorSoftwareFJ):
    """Un dato tiene un formato o un valor no permitido (ej.: correo sin @)."""

    # Constructor: solo recibe el mensaje porque el código es fijo
    def __init__(self, mensaje):
        """Crea el error con el código ERR-001."""
        super().__init__(mensaje, "ERR-001")   # Envía mensaje y código a la clase base


# Error para datos obligatorios que no llegaron
class ParametroFaltanteError(ErrorSoftwareFJ):
    """Falta un dato obligatorio (ej.: nombre vacío o None)."""

    # Constructor: solo recibe el mensaje
    def __init__(self, mensaje):
        """Crea el error con el código ERR-002."""
        super().__init__(mensaje, "ERR-002")   # Envía mensaje y código a la clase base


# Error para acciones que el estado actual no permite
class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se intenta algo que el estado actual no permite (ej.: cancelar dos veces)."""

    # Constructor: solo recibe el mensaje
    def __init__(self, mensaje):
        """Crea el error con el código ERR-003."""
        super().__init__(mensaje, "ERR-003")   # Envía mensaje y código a la clase base


# Error para servicios desactivados
class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio solicitado está desactivado o no existe."""

    # Constructor: solo recibe el mensaje
    def __init__(self, mensaje):
        """Crea el error con el código ERR-004."""
        super().__init__(mensaje, "ERR-004")   # Envía mensaje y código a la clase base


# Error para reservas que no se pueden crear o procesar
class ReservaInvalidaError(ErrorSoftwareFJ):
    """La reserva no se puede crear o procesar."""

    # Constructor: solo recibe el mensaje
    def __init__(self, mensaje):
        """Crea el error con el código ERR-005."""
        super().__init__(mensaje, "ERR-005")   # Envía mensaje y código a la clase base


# Error para cálculos de costos con valores sin sentido
class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Un cálculo de costos produce o recibe valores sin sentido."""

    # Constructor: solo recibe el mensaje
    def __init__(self, mensaje):
        """Crea el error con el código ERR-006."""
        super().__init__(mensaje, "ERR-006")   # Envía mensaje y código a la clase base
