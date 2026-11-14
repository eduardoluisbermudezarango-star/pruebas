"""
main.py
Programa principal de Software FJ.
Simula 16 operaciones (válidas e inválidas) para demostrar que el sistema
sigue funcionando aunque se presenten errores.
Ejecutar con:  python main.py
"""

from sistema import SistemaGestion      # Clase que guarda las listas y captura los errores
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada   # Los tres tipos de servicio
from registro import registrar_evento, registrar_error, ARCHIVO_LOG        # Funciones del log y ruta del archivo


# Función de apoyo para que la salida en pantalla se lea ordenada
def titulo(numero, texto):
    """Imprime el encabezado de cada operación."""
    print(f"\nOperación {numero}: {texto}")     # \n deja una línea en blanco antes del título


# Función que contiene toda la simulación
def simular():
    """Ejecuta las 16 operaciones de prueba."""
    sistema = SistemaGestion()                      # Crea el sistema con sus tres listas vacías
    registrar_evento("===== Inicio de la simulación =====")   # Marca en el log el inicio

    # ----- CLIENTES -----
    titulo(1, "registrar cliente válido")           # Encabezado de la operación 1
    # Registra un cliente correcto y lo guarda en la variable ana para usarlo en las reservas
    ana = sistema.registrar_cliente("Ana Torres", "1032456789", "ana.torres@correo.com", "3104567890")

    titulo(2, "registrar segundo cliente válido")   # Encabezado de la operación 2
    # Registra otro cliente correcto y lo guarda en la variable luis
    luis = sistema.registrar_cliente("Luis Pérez", "79456123", "luis@empresa.co", "3209876543")

    titulo(3, "cliente con correo inválido")        # Encabezado de la operación 3
    # El correo no tiene @: debe rechazarse con DatoInvalidoError
    sistema.registrar_cliente("Carlos Ruiz", "52147896", "carlos.correo.com", "3001234567")

    titulo(4, "cliente sin nombre (parámetro faltante)")   # Encabezado de la operación 4
    # El nombre es None: debe rechazarse con ParametroFaltanteError
    sistema.registrar_cliente(None, "1122334455", "x@correo.com", "3001112233")

    titulo(5, "cliente con documento no numérico (excepción encadenada)")   # Encabezado de la operación 5
    # El documento tiene letras: se rechaza y el log muestra el ValueError original como causa
    sistema.registrar_cliente("Marta Gil", "ABC123", "marta@correo.com", "3015556677")

    titulo(6, "cliente con documento repetido")     # Encabezado de la operación 6
    # El documento ya pertenece a Ana: debe rechazarse con OperacionNoPermitidaError
    sistema.registrar_cliente("Ana Torres", "1032456789", "ana2@correo.com", "3104567891")

    # ----- SERVICIOS -----
    titulo(7, "crear los tres servicios válidos")   # Encabezado de la operación 7
    sala = sistema.crear_servicio(ReservaSala, "Sala de juntas", 80000, 25)   # Sala: nombre, tarifa por hora, capacidad
    equipo = sistema.crear_servicio(AlquilerEquipo, "Portátil", 45000, 3)     # Alquiler: nombre, tarifa por día, cantidad
    # Asesoría: nombre, tarifa por hora, nivel del asesor
    asesoria = sistema.crear_servicio(AsesoriaEspecializada, "Arquitectura de software", 120000, "experto")

    titulo(8, "servicio con tarifa negativa")       # Encabezado de la operación 8
    sistema.crear_servicio(ReservaSala, "Sala pequeña", -5000, 6)   # Tarifa negativa: debe rechazarse

    titulo(9, "asesoría con nivel inexistente (excepción encadenada)")   # Encabezado de la operación 9
    # El nivel "master" no existe: se rechaza y el log muestra el KeyError original como causa
    sistema.crear_servicio(AsesoriaEspecializada, "Bases de datos", 90000, "master")

    # ----- RESERVAS -----
    titulo(10, "reserva exitosa de sala, procesada con IVA del 19 %")   # Encabezado de la operación 10
    reserva1 = sistema.crear_reserva(ana, sala, 3)  # Ana reserva la sala por 3 horas
    sistema.procesar_reserva(reserva1, 19)          # Se cobra con impuesto del 19 % (método sobrecargado, 2 datos)

    titulo(11, "reserva exitosa de equipos con IVA 19 % y descuento 10 %")   # Encabezado de la operación 11
    reserva2 = sistema.crear_reserva(luis, equipo, 7)   # Luis alquila los equipos por 7 días
    sistema.procesar_reserva(reserva2, 19, 10)      # Se cobra con impuesto 19 % y descuento 10 % (3 datos)

    titulo(12, "reserva con duración inválida (asesoría de 20 horas)")   # Encabezado de la operación 12
    sistema.crear_reserva(ana, asesoria, 20)        # 20 horas supera el máximo de 8: debe rechazarse

    titulo(13, "reserva sobre un servicio no disponible")   # Encabezado de la operación 13
    sala.cambiar_disponibilidad(False)              # Se desactiva la sala
    sistema.crear_reserva(luis, sala, 2)            # Debe rechazarse con ServicioNoDisponibleError
    sala.cambiar_disponibilidad(True)               # Se vuelve a activar la sala

    titulo(14, "reserva con cliente inexistente")   # Encabezado de la operación 14
    sistema.crear_reserva(None, asesoria, 2)        # El cliente es None: debe rechazarse

    titulo(15, "cálculo inconsistente: descuento del 150 %")   # Encabezado de la operación 15
    reserva3 = sistema.crear_reserva(ana, asesoria, 2)   # La reserva es válida y se crea
    sistema.procesar_reserva(reserva3, 19, 150)     # El descuento de 150 % es imposible: falla con excepción encadenada

    titulo(16, "cancelar la reserva y luego intentar cancelarla otra vez")   # Encabezado de la operación 16
    sistema.cancelar_reserva(reserva3)              # Primera cancelación: funciona
    sistema.cancelar_reserva(reserva3)              # Segunda cancelación: se rechaza porque ya estaba cancelada

    sistema.mostrar_resumen()                       # Muestra lo que quedó en las tres listas
    registrar_evento("===== Fin de la simulación =====")   # Marca en el log el final


# Punto de arranque: este bloque solo corre si se ejecuta este archivo directamente
if __name__ == "__main__":
    print("SOFTWARE FJ - Gestión de clientes, servicios y reservas")   # Título del programa
    try:                                            # Bloque que puede fallar
        simular()                                   # Ejecuta toda la simulación
    except Exception as error:                      # Última barrera: captura cualquier error no previsto
        registrar_error(error, "Error no controlado")           # Lo guarda en el log
        print(f"\nError inesperado controlado: {error}")        # Avisa en pantalla sin que el programa se rompa
    finally:                                        # Se ejecuta siempre, haya error o no
        print(f"\nEl sistema terminó sin interrupciones. Revise el log en: {ARCHIVO_LOG}")   # Mensaje final
