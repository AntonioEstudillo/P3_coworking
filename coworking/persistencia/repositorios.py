"""E13. Repositorios SQLite con SQL explícito y mapeo de filas.

Referencias: jerarquia06.py (contrato abstracto), elemento.py
(reconstrucción polimórfica con ``Espacio.crear``).
"""

import sqlite3
from abc import ABC, abstractmethod
from datetime import date

from ..modelo.actor import Nivel, Socio
from ..modelo.elemento import Espacio
from ..modelo.transaccion import Reservacion
from .conexion import transaccion


class Repositorio[T](ABC):
    """Contrato genérico de repositorio (la anotación ``[T]`` es sólo de tipos)."""

    def __init__(self, con: sqlite3.Connection) -> None:
        self._con = con

    @abstractmethod
    def guardar(self, objeto: T) -> None:
        """Inserta o actualiza (upsert)."""

    @abstractmethod
    def obtener(self, clave: str) -> T | None:
        """Busca por clave."""

    @abstractmethod
    def todos(self) -> list[T]:
        """Recupera todos."""

    @abstractmethod
    def _mapear(self, fila: sqlite3.Row) -> T:
        """Convierte una fila en objeto."""


class RepositorioEspacio(Repositorio[Espacio]):
    """Persistencia de espacios (los tres subtipos en una tabla)."""

    _UPSERT = (
        "INSERT INTO espacios (clave, tipo, nombre, precio_base, atributo) "
        "VALUES (?, ?, ?, ?, ?) "
        "ON CONFLICT(clave) DO UPDATE SET nombre = excluded.nombre, "
        "precio_base = excluded.precio_base, atributo = excluded.atributo"
    )

    @staticmethod
    def _parametros(e: Espacio) -> tuple[str, str, str, float, int]:
        return (e.clave, e.tipo, e.nombre, e.precio_base, e.valor_atributo())

    def guardar(self, objeto: Espacio) -> None:
        # TODO E13: implementar `RepositorioEspacio.guardar`
        raise NotImplementedError

    def guardar_varios(self, objetos: list[Espacio]) -> None:
        """Inserción masiva con ``executemany``."""
        # TODO E13: implementar `RepositorioEspacio.guardar_varios`
        raise NotImplementedError

    def obtener(self, clave: str) -> Espacio | None:
        # TODO E13: implementar `RepositorioEspacio.obtener`
        raise NotImplementedError

    def todos(self) -> list[Espacio]:
        # TODO E13: implementar `RepositorioEspacio.todos`
        raise NotImplementedError

    def _mapear(self, fila: sqlite3.Row) -> Espacio:
        """Reconstrucción polimórfica por la columna ``tipo``."""
        # TODO E13: implementar `RepositorioEspacio._mapear`
        raise NotImplementedError


class RepositorioSocio(Repositorio[Socio]):
    """Persistencia de socios."""

    def guardar(self, objeto: Socio) -> None:
        # TODO E13: implementar `RepositorioSocio.guardar`
        raise NotImplementedError

    def obtener(self, clave: str) -> Socio | None:
        # TODO E13: implementar `RepositorioSocio.obtener`
        raise NotImplementedError

    def todos(self) -> list[Socio]:
        # TODO E13: implementar `RepositorioSocio.todos`
        raise NotImplementedError

    def _mapear(self, fila: sqlite3.Row) -> Socio:
        # TODO E13: implementar `RepositorioSocio._mapear`
        raise NotImplementedError


class RepositorioReservacion(Repositorio[Reservacion]):
    """Persistencia de reservaciones y sus líneas (composición)."""

    def __init__(
        self,
        con: sqlite3.Connection,
        repo_espacios: RepositorioEspacio,
        repo_socios: RepositorioSocio,
    ) -> None:
        super().__init__(con)
        self._repo_espacios = repo_espacios
        self._repo_socios = repo_socios

    def guardar(self, objeto: Reservacion) -> None:
        """Upsert de la transacción y reemplazo de sus líneas en UNA transacción."""
        # TODO E13: implementar `RepositorioReservacion.guardar`
        raise NotImplementedError

    def obtener(self, clave: str) -> Reservacion | None:
        # TODO E13: implementar `RepositorioReservacion.obtener`
        raise NotImplementedError

    def todos(self) -> list[Reservacion]:
        # TODO E13: implementar `RepositorioReservacion.todos`
        raise NotImplementedError

    def _mapear(self, fila: sqlite3.Row) -> Reservacion:
        """Reconstruye la transacción, su socio y sus líneas."""
        # TODO E13: implementar `RepositorioReservacion._mapear`
        raise NotImplementedError
