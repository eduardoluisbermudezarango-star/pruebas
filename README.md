# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Fase 4 - Componente práctico - Programación 213023_68 - UNAD

Sistema orientado a objetos en Python, sin base de datos, con manejo avanzado de excepciones y registro de eventos y errores en un archivo de logs.

## Cómo ejecutar

Requiere Python 3.8 o superior. No necesita instalar librerías.

```
python main.py
```

Al terminar se crea el archivo `logs/software_fj.log` con todos los eventos y errores.

## Estructura

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (base `ErrorSoftwareFJ` y 6 derivadas) |
| `registro.py` | Escritura del archivo de logs |
| `entidad.py` | Clase abstracta `Entidad` |
| `cliente.py` | Clase `Cliente` con encapsulación y validaciones |
| `servicios.py` | Clase abstracta `Servicio` y `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reserva.py` | Clase `Reserva`: confirmar, cancelar y procesar |
| `sistema.py` | Clase `SistemaGestion`: listas internas y captura de errores |
| `main.py` | Simulación de 16 operaciones válidas e inválidas |

## Requisitos del Anexo 3 y dónde se cumplen

| Requisito | Ubicación |
|---|---|
| Clase abstracta general | `Entidad` en `entidad.py` |
| Cliente con validaciones y encapsulación | `cliente.py` (atributos privados y propiedades) |
| Servicio abstracto y tres servicios | `servicios.py` |
| Polimorfismo y métodos sobrescritos | `costo_base`, `describir`, `validar_parametros` |
| Métodos sobrecargados | `Servicio.calcular_costo(duracion, impuesto, descuento)` |
| Reserva con confirmación, cancelación y procesamiento | `reserva.py` |
| Excepciones personalizadas | `excepciones.py` |
| try/except | `SistemaGestion.cancelar_reserva` |
| try/except/else | `SistemaGestion.registrar_cliente` y `crear_servicio` |
| try/except/finally | `registro._escribir` |
| try/except/else/finally | `Reserva.procesar` y `SistemaGestion.crear_reserva` |
| Encadenamiento (`raise ... from ...`) | `Cliente.documento`, `AsesoriaEspecializada.__init__`, `Reserva.procesar` |
| Archivo de logs | `logs/software_fj.log` |
| Mínimo 10 operaciones simuladas | 16 operaciones en `main.py` |

## Integrantes

- Nombre 1: Eduardo Bermudez
-
