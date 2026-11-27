"""E12. Tarea periódica con detención cooperativa.

Referencias: thread07.py (subclase de ``threading.Thread`` con ``run``),
thread04.py (``threading.Event``), thread01.py (``join``).
"""

import threading
from abc import ABC, abstractmethod


class TareaPeriodica(threading.Thread, ABC):
    """Hilo que ejecuta ``ejecutar()`` cada ``periodo`` segundos hasta ``detener()``."""

    def __init__(self, periodo: float, nombre: str = "tarea") -> None:
        """
        Inicializa una tarea periódica ejecutada en un hilo.

        Configura el hilo mediante el constructor de
        threading.Thread, almacena el intervalo entre
        ejecuciones y crea un evento que permitirá
        solicitar la detención de forma cooperativa.

        Args:
            periodo (float): Intervalo en segundos entre
                las ejecuciones de la tarea.
            nombre (str): Nombre identificador del hilo.
                Por defecto es "tarea".
        """
        # TODO E12: implementar `TareaPeriodica.__init__`
        super().__init__(name= nombre, daemon=True)
        self.periodo = periodo
        self._evento_deteccion = threading.Event()

    def run(self) -> None:
        """
        Ejecuta periódicamente el trabajo del hilo.

        Mantiene un ciclo de ejecución mientras no se
        active el evento de detención.

        En cada iteración invoca el método ejecutar()
        y espera el intervalo establecido mediante
        threading.Event.wait().

        La espera puede interrumpirse cuando otro hilo
        activa el evento de detención.

        Returns:
            None: Este método no devuelve ningún valor.
        """
        """Ciclo: mientras el evento no esté activo, ejecutar y esperar."""
        # TODO E12: implementar `TareaPeriodica.run`
        while not self._evento_deteccion.is_set():
            self.ejecutar()
            self._evento_deteccion.wait(self.periodo)

    def detener(self, espera: float = 2.0) -> None:
        """
        Solicita la detención cooperativa del hilo.

        Activa el evento de detención para indicar
        al ciclo de ejecución que debe finalizar.

        Si el hilo está activo, espera su terminación
        mediante join(), utilizando el tiempo máximo
        de espera proporcionado.

        Args:
            espera (float): Tiempo máximo, en segundos,
                que se esperará a que finalice el hilo.
                Por defecto es 2.0 segundos.
        """
        """Detención cooperativa: activa el evento y espera con ``join``."""
        # TODO E12: implementar `TareaPeriodica.detener`
        self._evento_deteccion.set()

        if self.is_alive():
            self.join(timeout=espera)

    @abstractmethod
    def ejecutar(self) -> None:
        """Trabajo de cada ciclo."""
