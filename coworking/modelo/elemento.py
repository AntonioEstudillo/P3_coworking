"""E04–E05. Clase base abstracta, capacidades (mixins) y subtipos.

Referencias: jerarquia05.py (especialización), jerarquia06.py (ABC),
jerarquia11.py y jerarquia12.py (herencia múltiple y colisión de métodos),
encapsulacion03.py (propiedad calculada), persona03.py (name mangling),
p10_match.py (``match``).
"""

from abc import abstractmethod
from typing import ClassVar

from .clave import Clave
from .contrato import Tarifable


class Espacio(Tarifable):
    """Abstracción central: espacio de trabajo reservable."""

    PREFIJO: ClassVar[str] = ""

    def __init__(self, nombre: str, precio_base: float, clave: str | None = None) -> None:
        """Inicializa nombre, precio base y clave (se genera si es ``None``)."""
        # TODO E04: implementar `Espacio.__init__`
        raise NotImplementedError

    @property
    def clave(self) -> str:
        """Identidad inmutable (solo lectura)."""
        # TODO E04: implementar `Espacio.clave`
        raise NotImplementedError

    @property
    def nombre(self) -> str:
        """Nombre descriptivo, no vacío."""
        # TODO E04: implementar `Espacio.nombre`
        raise NotImplementedError

    @nombre.setter
    def nombre(self, valor: str) -> None:
        # TODO E04: implementar `Espacio.nombre`
        raise NotImplementedError

    @property
    def precio_base(self) -> float:
        """Precio base por día, estrictamente positivo."""
        # TODO E04: implementar `Espacio.precio_base`
        raise NotImplementedError

    @precio_base.setter
    def precio_base(self, valor: float) -> None:
        # TODO E04: implementar `Espacio.precio_base`
        raise NotImplementedError

    @property
    def tipo(self) -> str:
        """Prefijo del subtipo (propiedad calculada)."""
        return self.PREFIJO

    def recargo(self) -> float:
        """Recargo por capacidades; la base no tiene ninguno."""
        return 0.0

    @abstractmethod
    def factor(self) -> float:
        """Factor multiplicativo propio del subtipo."""

    @abstractmethod
    def valor_atributo(self) -> int:
        """Valor del atributo distintivo del subtipo (para persistencia)."""

    def _calcular(self, dias: int) -> float:
        """Tarifa del subtipo por ``dias`` (fórmula: §6 del DOCX, por deducir)."""
        # TODO E04: implementar `Espacio._calcular`
        raise NotImplementedError

    def copiar(self) -> "Espacio":
        """Crea un objeto equivalente con clave NUEVA (identidad distinta)."""
        # TODO E05: implementar `Espacio.copiar`
        raise NotImplementedError

    @staticmethod
    def crear(
        prefijo: str, nombre: str, precio_base: float, valor: int, clave: str | None = None
    ) -> "Espacio":
        """Fábrica polimórfica: reconstruye el subtipo correcto según el prefijo.

        Raises:
            ValueError: si el prefijo no corresponde a ningún subtipo.
        """
        # TODO E05: implementar `Espacio.crear`
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.clave} {self.nombre} (${self.precio_base:.2f}/día)"


class Capacidad:
    """Raíz de las capacidades: termina la cadena cooperativa de ``super()``."""

    def recargo(self) -> float:
        """Recargo neutro."""
        return 0.0

    def etiquetas(self) -> list[str]:
        """Etiquetas acumuladas por la cadena de ``super()``."""
        return []


class Equipado(Capacidad):
    """Capacidad: incluye proyector y pizarra."""

    RECARGO: ClassVar[float]  # TODO E05: valor por deducir de los ejemplos (§6)

    def recargo(self) -> float:
        # TODO E05: implementar `Equipado.recargo`
        raise NotImplementedError

    def etiquetas(self) -> list[str]:
        # TODO E05: implementar `Equipado.etiquetas`
        raise NotImplementedError


class Privado(Capacidad):
    """Capacidad: acceso restringido."""

    RECARGO: ClassVar[float]  # TODO E05: valor por deducir de los ejemplos (§6)

    def recargo(self) -> float:
        # TODO E05: implementar `Privado.recargo`
        raise NotImplementedError

    def etiquetas(self) -> list[str]:
        # TODO E05: implementar `Privado.etiquetas`
        raise NotImplementedError


class Escritorio(Espacio):
    """Escritorio compartido. Atributo ``monitores`` (monitores) entre 0 y 3."""

    # TODO E05: declarar las capacidades que hereda y su orden (§6 y prueba 05)

    PREFIJO: ClassVar[str] = "ESC"
    MINIMO: ClassVar[int] = 0
    MAXIMO: ClassVar[int] = 3
    ESCALA: ClassVar[int]  # TODO E05: valor por deducir de los ejemplos (§6)

    def __init__(self, nombre: str, precio_base: float, monitores: int, clave: str | None = None) -> None:
        # TODO E05: implementar `Escritorio.__init__`
        raise NotImplementedError

    @property
    def monitores(self) -> int:
        """monitores."""
        # TODO E05: implementar `Escritorio.monitores`
        raise NotImplementedError

    @monitores.setter
    def monitores(self, valor: int) -> None:
        # TODO E05: implementar `Escritorio.monitores`
        raise NotImplementedError

    def factor(self) -> float:
        """Factor propio del subtipo; depende de ``monitores`` y de ``ESCALA``."""
        # TODO E05: implementar `Escritorio.factor`
        raise NotImplementedError

    def valor_atributo(self) -> int:
        # TODO E05: implementar `Escritorio.valor_atributo`
        raise NotImplementedError


class SalaJuntas(Espacio):
    """Sala de juntas. Atributo ``capacidad`` (personas) entre 4 y 30."""

    # TODO E05: declarar las capacidades que hereda y su orden (§6 y prueba 05)

    PREFIJO: ClassVar[str] = "SAL"
    MINIMO: ClassVar[int] = 4
    MAXIMO: ClassVar[int] = 30
    ESCALA: ClassVar[int]  # TODO E05: valor por deducir de los ejemplos (§6)

    def __init__(self, nombre: str, precio_base: float, capacidad: int, clave: str | None = None) -> None:
        # TODO E05: implementar `SalaJuntas.__init__`
        raise NotImplementedError

    @property
    def capacidad(self) -> int:
        """personas."""
        # TODO E05: implementar `SalaJuntas.capacidad`
        raise NotImplementedError

    @capacidad.setter
    def capacidad(self, valor: int) -> None:
        # TODO E05: implementar `SalaJuntas.capacidad`
        raise NotImplementedError

    def factor(self) -> float:
        """Factor propio del subtipo; depende de ``capacidad`` y de ``ESCALA``."""
        # TODO E05: implementar `SalaJuntas.factor`
        raise NotImplementedError

    def valor_atributo(self) -> int:
        # TODO E05: implementar `SalaJuntas.valor_atributo`
        raise NotImplementedError


class Cabina(Espacio):
    """Cabina telefónica. Atributo ``aislamiento_db`` (decibeles) entre 20 y 60."""

    # TODO E05: declarar las capacidades que hereda y su orden (§6 y prueba 05)

    PREFIJO: ClassVar[str] = "CAB"
    MINIMO: ClassVar[int] = 20
    MAXIMO: ClassVar[int] = 60
    ESCALA: ClassVar[int]  # TODO E05: valor por deducir de los ejemplos (§6)

    def __init__(
        self, nombre: str, precio_base: float, aislamiento_db: int, clave: str | None = None
    ) -> None:
        # TODO E05: implementar `Cabina.__init__`
        raise NotImplementedError

    @property
    def aislamiento_db(self) -> int:
        """decibeles."""
        # TODO E05: implementar `Cabina.aislamiento_db`
        raise NotImplementedError

    @aislamiento_db.setter
    def aislamiento_db(self, valor: int) -> None:
        # TODO E05: implementar `Cabina.aislamiento_db`
        raise NotImplementedError

    def factor(self) -> float:
        """Factor propio del subtipo; depende de ``aislamiento_db`` y de ``ESCALA``."""
        # TODO E05: implementar `Cabina.factor`
        raise NotImplementedError

    def valor_atributo(self) -> int:
        # TODO E05: implementar `Cabina.valor_atributo`
        raise NotImplementedError

    def recargo(self) -> float:
        """Colisión: ambas capacidades definen recargo(); resuélvela de forma explícita (regla: §6)."""
        # TODO E05: implementar `Cabina.recargo`
        raise NotImplementedError
