"""E07–E08 y E14. Transacción con estados, composición de líneas y totales.

Referencias: demo.py y jerarquia13.py (clase anidada), construccion13.py
(la parte la crea el todo), thread07.py (sección crítica), persistencia03.py
(pickle de objetos).
"""

import threading
from datetime import date
from typing import ClassVar

from .actor import Socio
from .clave import Clave
from .contrato import Tarifable
from .elemento import Espacio


class Reservacion:
    """Transacción del dominio: reservación de espacios."""

    PREFIJO: ClassVar[str] = "RES"
    ABIERTA: ClassVar[str] = "ABIERTA"
    EN_CURSO: ClassVar[str] = "EN_CURSO"
    CERRADA: ClassVar[str] = "CERRADA"
    CANCELADA: ClassVar[str] = "CANCELADA"
    # TODO E07: traducir el diagrama de estados (§6) a una tabla de transiciones
    TRANSICIONES: ClassVar[dict[str, tuple[str, ...]]]

    class Linea:
        """Parte de la composición: sólo existe dentro de su transacción."""

        def __init__(self, contenedora: "Reservacion", espacio: Espacio, dias: int) -> None:
            # TODO E07: implementar `Reservacion.Linea.__init__`
            raise NotImplementedError

        @property
        def contenedora(self) -> "Reservacion":
            """Referencia explícita al todo."""
            # TODO E07: implementar `Reservacion.Linea.contenedora`
            raise NotImplementedError

        @property
        def espacio(self) -> Espacio:
            # TODO E07: implementar `Reservacion.Linea.espacio`
            raise NotImplementedError

        @property
        def dias(self) -> int:
            # TODO E07: implementar `Reservacion.Linea.dias`
            raise NotImplementedError

        def importe(self) -> float:
            """Importe de la línea = cotización polimórfica del espacio."""
            # TODO E08: implementar `Reservacion.Linea.importe`
            raise NotImplementedError

    def __init__(
        self,
        socio: Socio,
        fecha: date,
        clave: str | None = None,
        estado: str = "ABIERTA",
        alertada: bool = False,
    ) -> None:
        # TODO E07: implementar `Reservacion.__init__`
        raise NotImplementedError

    @property
    def clave(self) -> str:
        # TODO E07: implementar `Reservacion.clave`
        raise NotImplementedError

    @property
    def socio(self) -> Socio:
        # TODO E07: implementar `Reservacion.socio`
        raise NotImplementedError

    @property
    def fecha(self) -> date:
        # TODO E07: implementar `Reservacion.fecha`
        raise NotImplementedError

    @property
    def estado(self) -> str:
        # TODO E07: implementar `Reservacion.estado`
        raise NotImplementedError

    @property
    def lineas(self) -> tuple["Reservacion.Linea", ...]:
        """Vista inmutable de las líneas."""
        # TODO E07: implementar `Reservacion.lineas`
        raise NotImplementedError

    def agregar(self, espacio: Espacio, dias: int) -> "Reservacion.Linea":
        """Crea y posee una línea; sólo en estado ABIERTA. Sección crítica."""
        # TODO E07: implementar `Reservacion.agregar`
        raise NotImplementedError

    def _restaurar_linea(self, espacio: Espacio, dias: int) -> None:
        """Uso exclusivo de persistencia: agrega sin validar el estado."""
        # TODO E07: implementar `Reservacion._restaurar_linea`
        raise NotImplementedError

    def cambiar_estado(self, nuevo: str) -> None:
        """Aplica una transición válida de TRANSICIONES.

        Raises:
            ValueError: transición no permitida o EN_CURSO sin líneas.
        """
        # TODO E07: implementar `Reservacion.cambiar_estado`
        raise NotImplementedError

    def antiguedad(self, hoy: date) -> int:
        """Días transcurridos desde la apertura."""
        # TODO E07: implementar `Reservacion.antiguedad`
        raise NotImplementedError

    def subtotal(self) -> float:
        """Suma de importes de las líneas."""
        # TODO E08: implementar `Reservacion.subtotal`
        raise NotImplementedError

    def descuento(self) -> float:
        """Monto de descuento según el nivel del socio."""
        # TODO E08: implementar `Reservacion.descuento`
        raise NotImplementedError

    def total(self) -> float:
        """Total = subtotal - descuento."""
        # TODO E08: implementar `Reservacion.total`
        raise NotImplementedError

    def __getstate__(self) -> dict[str, object]:
        """Excluye el candado (no serializable), equivalente a ``transient``."""
        # TODO E14: implementar `Reservacion.__getstate__`
        raise NotImplementedError

    def __setstate__(self, estado: dict[str, object]) -> None:
        """Restaura atributos y crea un candado nuevo."""
        # TODO E14: implementar `Reservacion.__setstate__`
        raise NotImplementedError

    def __str__(self) -> str:
        # TODO E07: implementar `Reservacion.__str__`
        raise NotImplementedError
