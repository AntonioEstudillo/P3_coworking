"""E03. Identidad de los objetos: claves ``PPP-0000``.

Referencias: construccion03.py (contador como atributo de clase),
construccion09.py (@classmethod / @staticmethod), thread07.py (sincronización).
"""

import threading
from typing import ClassVar
import re


class Clave:
    """Generador y validador de claves con prefijo de 3 letras y 4 dígitos."""

    _contadores: ClassVar[dict[str, int]] = {}
    _candado: ClassVar[threading.Lock] = threading.Lock()

    @staticmethod
    def es_valida(texto: str) -> bool:
        """``True`` si ``texto`` tiene la forma ``ABC-0001``.
        Verifica que una clave tenga el formato establecido.

        La clave debe contener exactamente tres letras
        mayúsculas, seguidas de un guion y cuatro dígitos.

        Args:
            texto (str): Clave que se desea validar.

        Returns:
            bool: True si la clave cumple el formato
                PPP-0000; False en caso contrario.

        """
        # TODO E03: implementar `Clave.es_valida`
        return re.fullmatch(r"[A-Z]{3}-[0-9]{4}",texto) is not None

    @classmethod
    def siguiente(cls, prefijo: str) -> str:
        """Devuelve la siguiente clave del prefijo; segura entre hilos.

        Valida que el prefijo contenga tres letras mayúsculas
        y utiliza un candado para evitar que varios hilos
        generen identificadores repetidos.

        Args:
            prefijo (str): Tres letras mayúsculas que
                identifican el tipo de objeto.

        Returns:
            str: Nueva clave con el formato PPP-0000.

        Raises:
            ValueError: si el prefijo no son 3 letras mayúsculas.
        """
        # TODO E03: implementar `Clave.siguiente`
        if re.fullmatch(r"[A-Z]{3}",prefijo) is None:
            raise ValueError("prefijo no son 3 letras")

        with cls._candado:
            numero = cls._contadores.get(prefijo, 0) + 1

            if numero > 9999:
                raise ValueError("Se agotaron las claves del prefijo")

            cls._contadores[prefijo] = numero

        return f"{prefijo}-{numero:04d}"


    @classmethod
    def registrar(cls, clave: str) -> None:
        """Informa una clave existente (p. ej. leída de SQLite) para no repetirla.

        Valida el formato del identificador y conserva el
        mayor número registrado para cada prefijo,
        evitando que se generen claves repetidas.

        Args:
            clave (str): Identificador existente con el
                formato PPP-0000.

        Raises:
            ValueError: Si la clave no cumple el formato.
        """
        # TODO E03: implementar `Clave.registrar`
        if not cls.es_valida(clave):
            raise ValueError("clave no cumple el formato")

        prefijo, numero_texto = clave.split("-")
        numero = int(numero_texto)

        with cls._candado:
            cls._contadores[prefijo] = max(cls._contadores.get(prefijo,0), numero)


    @classmethod
    def reiniciar(cls) -> None:
        """Reinicia todos los contadores (uso en pruebas)."""
        with cls._candado:
            cls._contadores.clear()
