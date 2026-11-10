"""E14. Respaldo complementario con ``pickle``.

Referencias: persistencia02.py y persistencia03.py. Investigación del
estudiante: ``__getstate__``/``__setstate__`` (necesarios porque un
``threading.Lock`` no es serializable).
"""

import pickle
from pathlib import Path

from ..modelo.transaccion import Reservacion


def respaldar(ruta: str | Path, reservaciones: list[Reservacion]) -> int:
    """Serializa la lista completa; devuelve cuántas se guardaron."""
    # TODO E14: implementar `respaldar`
    raise NotImplementedError


def restaurar(ruta: str | Path) -> list[Reservacion]:
    """Lee un respaldo previo.

    Raises:
        TypeError: si el contenido no es una lista de Reservacion.
    """
    # TODO E14: implementar `restaurar`
    raise NotImplementedError
