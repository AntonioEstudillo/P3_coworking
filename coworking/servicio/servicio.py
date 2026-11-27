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
            """
            Inicializa el monitor periódico del servicio.

            Configura el hilo mediante el constructor de
            TareaPeriodica, almacena una referencia al
            servicio supervisado e inicializa el contador
            de ejecuciones.

            Args:
                servicio (ServicioCoworking): Instancia del
                    servicio cuyas reservaciones supervisará
                    el monitor.
                periodo (float): Intervalo en segundos entre
                    las ejecuciones periódicas del monitor.
            """
            # TODO E12: implementar `ServicioCoworking.Monitor.__init__`
            super().__init__(periodo=periodo, nombre= "Monitor")

            self._servicio = servicio
            self.ejecuciones = 0

        def ejecutar(self) -> None:
            """
            Ejecuta una revisión periódica del servicio.

            Invoca el método revisar() de la instancia de
            ServicioCoworking asociada al monitor y aumenta
            el contador de ejecuciones realizadas.

            Este método es invocado por el ciclo definido
            en TareaPeriodica.run().

            Returns:
                None: No devuelve ningún valor.
            """
            # TODO E12: implementar `ServicioCoworking.Monitor.ejecutar`
            self._servicio.revisar()
            self.ejecuciones += 1

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
        """
        Revisa las reservaciones y aplica las reglas del monitor.

        Cancela las reservaciones abiertas que no tienen
        líneas y poseen al menos un día de antigüedad.

        También detecta reservaciones en curso que superan
        el plazo permitido y emite una alerta única,
        persistiendo el indicador alertada.

        Protege las operaciones sobre las reservaciones
        mediante un candado y emite los eventos después
        de liberar la sección crítica.

        Returns:
            tuple[int, int]: Cantidad de reservaciones
                canceladas y cantidad de alertas emitidas.
        """
        """Reglas del monitor; devuelve (canceladas, alertas emitidas).

        1. ABIERTA sin líneas con antigüedad >= 1 día → CANCELADA.
        2. EN_CURSO con antigüedad > PLAZO y sin alerta previa → alerta ÚNICA
           (el indicador ``alertada`` se persiste).
        """
        # TODO E12: implementar `ServicioCoworking.revisar`
        hoy = self._reloj()

        canceladas = 0
        alertas = 0
        eventos: list[tuple[[str, str]]] = []

        with self._candado:
            repositorio = RepositorioReservacion(
                self._con,
                RepositorioEspacio(self._con),
                RepositorioSocio(self._con)
            )

            for reservacion in repositorio.todos():
                dias = reservacion.antiguedad(hoy)

                if (
                    reservacion.estado == Reservacion.ABIERTA
                    and not reservacion.lineas
                    and dias >= 1
                ):
                    reservacion.cambiar_estado(Reservacion.CANCELADA)

                    repositorio.guardar(reservacion)

                    canceladas += 1

                    eventos.append(("CANCELACION", reservacion.clave))

                elif(
                    reservacion.estado == Reservacion.EN_CURSO
                    and dias > self.PLAZO
                    and not reservacion.alertada
                ):
                    reservacion.alertada = True

                    repositorio.guardar(reservacion)

                    alertas += 1
                    eventos.append(("ALERTA", reservacion.clave))

        for tipo, detalle in eventos:
            self._emitir(tipo, detalle)

        return canceladas, alertas


    def iniciar_monitor(self, periodo: float = 60.0) -> None:
        """
        Crea e inicia el monitor periódico del servicio.

        Comprueba si ya existe un monitor activo para
        evitar iniciar múltiples hilos simultáneamente.

        Si no existe un monitor activo, crea una nueva
        instancia de la clase anidada Monitor, la asocia
        al servicio e inicia su ejecución mediante start().

        La operación se protege mediante el candado
        del servicio.

        Args:
            periodo (float): Intervalo en segundos entre
                las ejecuciones del monitor.
                Por defecto es 60.0.

        Returns:
            None: No devuelve ningún valor.
        """
        # TODO E12: implementar `ServicioCoworking.iniciar_monitor`
        with self._candado:
            if self._monitor is not None and self._monitor.is_alive():
                return

            self._monitor = self.Monitor(self, periodo)
            self._monitor.start()

    def detener_monitor(self) -> None:
        """
        Solicita la detención del monitor periódico.

        Obtiene una referencia al monitor asociado al
        servicio mientras protege el acceso mediante
        el candado.

        Posteriormente, solicita su detención
        cooperativa fuera de la sección crítica,
        evitando mantener el candado adquirido
        mientras se espera la finalización del hilo.

        Si no existe un monitor, no realiza ninguna
        operación.

        Returns:
            None: No devuelve ningún valor.
        """
        # TODO E12: implementar `ServicioCoworking.detener_monitor`

        with self._candado:
            monitor = self._monitor

        if monitor is not None:
            monitor.detener()


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
