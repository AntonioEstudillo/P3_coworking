"""E09–E10. Catálogo (agregación) y tipos anidados/locales.

Referencias: construccion05.py (``*args`` y ``**kwargs``), demo.py (el todo
referencia partes que existen por sí mismas), jerarquia13.py (clase anidada),
p10_match.py (``match``).
"""

from .elemento import Espacio


class DirectorioEspacios:
    """Agregación de espacios: los contiene, pero no los crea ni los destruye."""

    def __init__(self, *espacios: Espacio) -> None:
        # TODO E09: implementar `DirectorioEspacios.__init__`
        raise NotImplementedError

    def agregar(self, *espacios: Espacio) -> int:
        """Agrega uno o varios; rechaza claves repetidas. Devuelve cuántos agregó."""
        # TODO E09: implementar `DirectorioEspacios.agregar`
        raise NotImplementedError

    def obtener(self, clave: str) -> Espacio:
        """Raises: KeyError si no existe."""
        # TODO E09: implementar `DirectorioEspacios.obtener`
        raise NotImplementedError

    def quitar(self, clave: str) -> Espacio:
        # TODO E09: implementar `DirectorioEspacios.quitar`
        raise NotImplementedError

    def todos(self) -> tuple[Espacio, ...]:
        """Vista inmutable en orden de inserción."""
        # TODO E09: implementar `DirectorioEspacios.todos`
        raise NotImplementedError

    def __len__(self) -> int:
        # TODO E09: implementar `DirectorioEspacios.__len__`
        raise NotImplementedError

    def buscar(self, **criterios: object) -> list[Espacio]:
        """Filtra por ``tipo=``, ``texto=`` (en el nombre) y ``precio_max=``.

        Raises:
            ValueError: criterio desconocido.
        """
        # TODO E09: implementar `DirectorioEspacios.buscar`
        raise NotImplementedError

    def ordenados(self, por: str = "nombre", descendente: bool = False) -> list[Espacio]:
        """Ordena por ``"nombre"``, ``"precio"`` o ``"clave"`` usando ``key=lambda``."""
        # TODO E09: implementar `DirectorioEspacios.ordenados`
        raise NotImplementedError

    def resumen_por_tipo(self) -> dict[str, int]:
        """Cuenta espacios por tipo usando una CLASE LOCAL como acumulador."""

        class Acumulador:
            """Clase local: sólo existe dentro de este método."""

            def __init__(self) -> None:
                self.cuentas: dict[str, int] = {}

            def sumar(self, tipo: str) -> None:
                self.cuentas[tipo] = self.cuentas.get(tipo, 0) + 1

        # TODO E10: implementar `DirectorioEspacios.resumen_por_tipo`
        raise NotImplementedError
