"""E15–E16 y E12. Fachada única del dominio Espacio de coworking.

Referencias: p23_contexto3.py (``__enter__``/``__exit__``), jerarquia13.py
(clase anidada ``Monitor``), thread07.py (hilo como clase), construccion09.py.
"""

import threading
from collections.abc import Callable
from datetime import date
from pathlib import Path
from types import TracebackType
from typing import ClassVar

from ..concurrencia.tarea import TareaPeriodica
from ..eventos.oyentes import Oyente
from ..modelo.actor import Socio
from ..modelo.catalogo import DirectorioEspacios
from ..modelo.elemento import Espacio
from ..modelo.transaccion import Reservacion
from ..persistencia import respaldo
from ..persistencia.conexion import abrir
from ..persistencia.repositorios import (
    RepositorioEspacio,
    RepositorioReservacion,
    RepositorioSocio,
)


class ServicioCoworking:
    """Fachada: casos de uso, eventos, monitor y reportes."""

    PLAZO: ClassVar[int] = 1
    """Días máximos que una reservacion puede permanecer EN_CURSO."""

    class Monitor(TareaPeriodica):
        """Hilo vigilante: clase anidada con referencia explícita a su servicio."""

        def __init__(self, servicio: "ServicioCoworking", periodo: float) -> None:
            # TODO E12: implementar `ServicioCoworking.Monitor.__init__`
            raise NotImplementedError

        def ejecutar(self) -> None:
            # TODO E12: implementar `ServicioCoworking.Monitor.ejecutar`
            raise NotImplementedError

    def __init__(
        self,
        ruta_bd: str = ":memory:",
        reloj: Callable[[], date] = date.today,
    ) -> None:
        """``reloj`` inyectable para pruebas deterministas."""
        self._ruta_bd = ruta_bd
        self._reloj = reloj
        self._oyentes: list[Oyente] = []
        self._candado = threading.Lock()
        self._monitor: ServicioCoworking.Monitor | None = None
        self.catalogo = DirectorioEspacios()

    # ---------------------------------------------------------------- ciclo de vida
    def __enter__(self) -> "ServicioCoworking":
        # TODO E15: implementar `ServicioCoworking.__enter__`
        raise NotImplementedError

    def __exit__(
        self,
        tipo: type[BaseException] | None,
        valor: BaseException | None,
        traza: TracebackType | None,
    ) -> None:
        # TODO E15: implementar `ServicioCoworking.__exit__`
        raise NotImplementedError

    # ---------------------------------------------------------------- eventos
    def suscribir(self, oyente: Oyente) -> None:
        # TODO E15: implementar `ServicioCoworking.suscribir`
        raise NotImplementedError

    def _emitir(self, evento: str, detalle: str) -> None:
        # TODO E15: implementar `ServicioCoworking._emitir`
        raise NotImplementedError

    # ---------------------------------------------------------------- casos de uso
    def registrar_espacio(self, espacio: Espacio) -> None:
        # TODO E15: implementar `ServicioCoworking.registrar_espacio`
        raise NotImplementedError

    def registrar_socio(self, socio: Socio) -> None:
        # TODO E15: implementar `ServicioCoworking.registrar_socio`
        raise NotImplementedError

    def socios(self) -> list[Socio]:
        # TODO E15: implementar `ServicioCoworking.socios`
        raise NotImplementedError

    def abrir(self, clave_socio: str) -> Reservacion:
        """Abre una reservacion con la fecha del reloj inyectado."""
        # TODO E15: implementar `ServicioCoworking.abrir`
        raise NotImplementedError

    def agregar_linea(self, clave_reservacion: str, clave_espacio: str, dias: int) -> Reservacion:
        # TODO E15: implementar `ServicioCoworking.agregar_linea`
        raise NotImplementedError

    def cambiar_estado(self, clave_reservacion: str, nuevo: str) -> Reservacion:
        # TODO E15: implementar `ServicioCoworking.cambiar_estado`
        raise NotImplementedError

    def reservaciones(self, estado: str | None = None) -> list[Reservacion]:
        """Todas o sólo las del estado indicado."""
        # TODO E15: implementar `ServicioCoworking.reservaciones`
        raise NotImplementedError

    def _requerir(self, clave: str) -> Reservacion:
        # TODO E15: implementar `ServicioCoworking._requerir`
        raise NotImplementedError

    # ---------------------------------------------------------------- monitor
    def revisar(self) -> tuple[int, int]:
        """Reglas del monitor; devuelve (canceladas, alertas emitidas).

        1. ABIERTA sin líneas con antigüedad >= 1 día → CANCELADA.
        2. EN_CURSO con antigüedad > PLAZO y sin alerta previa → alerta ÚNICA
           (el indicador ``alertada`` se persiste).
        """
        # TODO E12: implementar `ServicioCoworking.revisar`
        raise NotImplementedError

    def iniciar_monitor(self, periodo: float = 60.0) -> None:
        # TODO E12: implementar `ServicioCoworking.iniciar_monitor`
        raise NotImplementedError

    def detener_monitor(self) -> None:
        # TODO E12: implementar `ServicioCoworking.detener_monitor`
        raise NotImplementedError

    @property
    def monitor(self) -> "ServicioCoworking.Monitor | None":
        return self._monitor

    # ---------------------------------------------------------------- respaldo
    def respaldar(self, ruta: str | Path) -> int:
        # TODO E14: implementar `ServicioCoworking.respaldar`
        raise NotImplementedError

    # ---------------------------------------------------------------- reportes
    def conteo_por_estado(self) -> dict[str, int]:
        """Número de reservaciones por estado (los 4 estados siempre presentes)."""
        # TODO E16: implementar `ServicioCoworking.conteo_por_estado`
        raise NotImplementedError

    def ingresos_por_tipo(self) -> dict[str, float]:
        """Suma de importes de reservaciones CERRADAS agrupada por tipo de espacio."""
        # TODO E16: implementar `ServicioCoworking.ingresos_por_tipo`
        raise NotImplementedError

    def top_espacios(self, n: int = 3) -> list[tuple[str, int]]:
        """Los ``n`` espacios más usados (clave, días acumulados), descendente."""
        # TODO E16: implementar `ServicioCoworking.top_espacios`
        raise NotImplementedError

    def ticket_promedio(self) -> float:
        """Promedio del total de las reservaciones CERRADAS (0.0 si no hay)."""
        # TODO E16: implementar `ServicioCoworking.ticket_promedio`
        raise NotImplementedError
