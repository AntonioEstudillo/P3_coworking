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

import math


class Espacio(Tarifable):
    """Abstracción central: espacio de trabajo reservable."""

    PREFIJO: ClassVar[str] = ""

    def __init__(self, nombre: str, precio_base: float, clave: str | None = None) -> None:
        """Inicializa nombre, precio base y clave (se genera si es ``None``).
        Asigna el nombre y el precio base mediante sus
        propiedades para aplicar las validaciones.
        Genera una clave si no se proporciona una o
        registra la clave existente si es válida.

        Args:
            nombre (str): Nombre descriptivo del espacio.
            precio_base (float): Precio diario del espacio.
                Debe ser mayor que cero.
            clave (str | None): Identificador opcional.
                Si es None, se genera automáticamente.

        Raises:
            ValueError: Si el nombre, precio o clave son
                inválidos, o si la clave no corresponde
                al prefijo del subtipo.
            """
        # TODO E04: implementar `Espacio.__init__`
        super().__init__()
        self.nombre = nombre
        self.precio_base = precio_base

        if clave is None:
            self.__clave = Clave.siguiente(self.PREFIJO)
        else:
            if not Clave.es_valida(clave) or not clave.startswith(f"{self.PREFIJO}-"):
                raise ValueError("Clave invalida para el tipo de espacio")
            Clave.registrar(clave)
            self.__clave = clave



    @property
    def clave(self) -> str:
        """Identidad inmutable (solo lectura).

        Obtiene el identificador único del espacio.

        Permite consultar el atributo privado __clave
        mediante una propiedad de solo lectura,
        evitando su modificación mediante asignación
        directa a la propiedad.

        Returns:
            str: Identificador único del espacio.

        """
        # TODO E04: implementar `Espacio.clave`
        return self.__clave

    @property
    def nombre(self) -> str:
        """Nombre descriptivo, no vacío.
        Permite consultar el atributo protegido _nombre,
        cuyo valor es validado y almacenado mediante
        el setter correspondiente.

        Returns:
            str: Nombre descriptivo del espacio.
        """
        # TODO E04: implementar `Espacio.nombre`
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """
        Establece el nombre descriptivo del espacio.

        Elimina los espacios al inicio y al final del nombre
        y verifica que el resultado no esté vacío antes
        de almacenarlo en el atributo protegido _nombre.

        Args:
            valor (str): Nombre que se asignará al espacio.

        Raises:
            ValueError: Si el nombre está vacío o contiene
                únicamente espacios en blanco.
        """
        # TODO E04: implementar `Espacio.nombre`
        nombre_limpio = valor.strip()
        if not nombre_limpio:
            raise ValueError("El nombre no puede ser Vacio")

        self._nombre = nombre_limpio

    @property
    def precio_base(self) -> float:
        """Precio base por día, estrictamente positivo.

        Obtiene el precio base diario del espacio.

        Permite consultar el atributo protegido _precio_base,
        cuyo valor es validado y almacenado mediante
        el setter correspondiente.

        Returns:
            float: Precio base diario del espacio.
        """
        # TODO E04: implementar `Espacio.precio_base`
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor: float) -> None:
        """
        Establece el precio base diario del espacio.

        Valida que el valor recibido sea estrictamente
        positivo y finito antes de almacenarlo en el
        atributo protegido _precio_base.

        Args:
            valor (float): Precio diario que se asignará
                al espacio.

        Raises:
            ValueError: Si el precio es menor o igual
                que cero, infinito o NaN.
        """
        # TODO E04: implementar `Espacio.precio_base`
        if not math.isfinite(valor) or valor <= 0:
            raise ValueError("Precio debe ser positivo y finito")

        self._precio_base = float(valor)

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
        """Tarifa del subtipo por ``dias`` (fórmula: §6 del DOCX, por deducir).
        Calcula la tarifa de un espacio según sus características.

        Multiplica el precio base por el número de días y
        el factor correspondiente al subtipo. Posteriormente,
        aplica el recargo de sus capacidades y redondea
        el resultado a dos decimales.

        Args:
            dias (int): Número de días de la reservación,
                previamente validado por cotizar().

        Returns:
            float: Tarifa total del espacio sin IVA,
                redondeada a dos decimales.

        """
        # TODO E04: implementar `Espacio._calcular`
        subtotal = self.precio_base * dias
        total = subtotal * self.factor() * (1 + self.recargo())
        return self.redondear(total)

    def copiar(self) -> "Espacio":
        """Crea un objeto equivalente con clave NUEVA (identidad distinta).    Crea una copia del espacio con una identidad nueva.

        Conserva el subtipo, nombre, precio base y atributo
        distintivo del objeto original. Utiliza el método
        de fábrica crear() para construir una nueva instancia
        sin reutilizar su identificador.

        Returns:
            Espacio: Nueva instancia del mismo subtipo,
                con características equivalentes y una
                clave diferente.
        """
        # TODO E05: implementar `Espacio.copiar`
        return Espacio.crear(
            prefijo=self.tipo,
            nombre=self.nombre,
            precio_base=self.precio_base,
            valor=self.valor_atributo()
        )

    @staticmethod
    def crear(
        prefijo: str, nombre: str, precio_base: float, valor: int, clave: str | None = None
    ) -> "Espacio":
        """Fábrica polimórfica: reconstruye el subtipo correcto según el prefijo.

        Raises:
            ValueError: si el prefijo no corresponde a ningún subtipo.
        """
        # TODO E05: implementar `Espacio.crear`
        match prefijo:
            case "ESC":
                return Escritorio(nombre, precio_base, valor,clave)
            case "SAL":
                return SalaJuntas(nombre, precio_base, valor, clave)
            case "CAB":
                return Cabina(nombre, precio_base, valor, clave)
            case _:
                return ValueError(f"Tipo de espacio desconocido: {prefijo}")

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
    """Capacidad: incluye proyector y pizarra.

    Representa una capacidad que incorpora equipamiento adicional.

    Aplica un recargo del 8 % sobre la tarifa de los
    espacios que cuentan con esta capacidad.

    """

    RECARGO: ClassVar[float] = 0.08 # TODO E05: valor por deducir de los ejemplos (§6)

    def recargo(self) -> float:
        """
           Calcula el recargo correspondiente a la capacidad Equipado.

           Suma el porcentaje de recargo de Equipado al valor
           obtenido mediante super(), permitiendo combinar
           los recargos de diferentes capacidades siguiendo
           el orden de resolución de métodos (MRO).

           Returns:
               float: Recargo acumulado de las capacidades,
                   expresado como un valor decimal.
           """
        # TODO E05: implementar `Equipado.recargo`
        return Equipado.RECARGO + super().recargo()

    def etiquetas(self) -> list[str]:
        # TODO E05: implementar `Equipado.etiquetas`
        """
        Obtiene las etiquetas de las capacidades del objeto.

        Agrega la etiqueta "equipado" a las etiquetas
        recuperadas mediante super(), permitiendo
        combinar características de distintas clases
        según el orden de resolución de métodos (MRO).

        Returns:
            list[str]: Lista de etiquetas de las
                capacidades, comenzando por "equipado".
        """

        return ["equipado"] + super().etiquetas()


class Privado(Capacidad):
    """Capacidad: acceso restringido.

    Representa una capacidad con acceso restringido.

    Aplica un recargo del 15 % sobre la tarifa de
    los espacios que incorporan esta capacidad.

    """

    RECARGO: ClassVar[float] = 0.15 # TODO E05: valor por deducir de los ejemplos (§6)

    def recargo(self) -> float:
        """
        Calcula el recargo correspondiente a la capacidad Privado.

        Suma el porcentaje de recargo de Privado al valor
        obtenido mediante super(), permitiendo acumular
        los recargos de distintas capacidades según el
        orden de resolución de métodos (MRO).

        Returns:
            float: Recargo total acumulado de las
                capacidades, expresado como decimal.
        """

        # TODO E05: implementar `Privado.recargo`
        return Privado.RECARGO + super().recargo()

    def etiquetas(self) -> list[str]:
        """
        Obtiene las etiquetas de las capacidades del objeto.

        Agrega la etiqueta "privado" a las etiquetas
        recuperadas mediante super(), permitiendo combinar
        las características de distintas capacidades
        según el orden de resolución de métodos (MRO).

        Returns:
            list[str]: Lista de etiquetas de las capacidades,
                comenzando por "privado" en esta implementación.
        """
        # TODO E05: implementar `Privado.etiquetas`
        return ["privado"] + super().etiquetas()


class Escritorio(Equipado, Espacio):
    """Escritorio compartido. Atributo ``monitores`` (monitores) entre 0 y 3.

        Representa un escritorio compartido de coworking.

        Permite configurar entre cero y tres monitores.
        Utiliza la constante ESCALA para determinar
        el factor de la tarifa según la cantidad de
        monitores disponibles.

        Attributes:
            PREFIJO (str): Identificador del subtipo.
            MINIMO (int): Cantidad mínima de monitores.
            MAXIMO (int): Cantidad máxima de monitores.
            ESCALA (int): Divisor utilizado para calcular
                el factor de tarifa. Su valor es 10.
    """
    # TODO E05: declarar las capacidades que hereda y su orden (§6 y prueba 05)

    PREFIJO: ClassVar[str] = "ESC"
    MINIMO: ClassVar[int] = 0
    MAXIMO: ClassVar[int] = 3
    ESCALA: ClassVar[int]  = 10 # TODO E05: valor por deducir de los ejemplos (§6)

    def __init__(self, nombre: str, precio_base: float, monitores: int, clave: str | None = None) -> None:
        """
           Inicializa un escritorio con sus características.

           Reutiliza el constructor de Espacio para establecer
           el nombre, precio base e identificador. Posteriormente,
           asigna la cantidad de monitores mediante su setter
           para aplicar las validaciones correspondientes.

           Args:
               nombre (str): Nombre descriptivo del escritorio.
               precio_base (float): Precio diario del escritorio.
                   Debe ser estrictamente positivo.
               monitores (int): Cantidad de monitores disponibles.
                   Debe estar entre 0 y 3.
               clave (str | None): Identificador opcional.
                   Si es None, se genera automáticamente.

           Raises:
               ValueError: Si el nombre, precio, clave o
                   cantidad de monitores son inválidos.
           """

        # TODO E05: implementar `Escritorio.__init__`

        super.__init__(nombre, precio_base,clave)

        self.monitores = monitores


    @property
    def monitores(self) -> int:
        """
        Obtiene la cantidad de monitores del escritorio.

        Recupera el atributo protegido _monitores,
        previamente validado y almacenado mediante
        el setter correspondiente.

        Returns:
            int: Cantidad de monitores del escritorio,
                comprendida entre 0 y 3.
        """
        # TODO E05: implementar `Escritorio.monitores`
        return self._monitores

    @monitores.setter
    def monitores(self, valor: int) -> None:
        # TODO E05: implementar `Escritorio.monitores`
        """
        Establece la cantidad de monitores del escritorio.

        Verifica que el valor recibido sea un número entero
        comprendido entre los límites MINIMO y MAXIMO.
        Una vez validado, lo almacena en el atributo
        protegido _monitores.

        Args:
            valor (int): Cantidad de monitores que tendrá
                el escritorio. Debe estar entre 0 y 3.

        Raises:
            ValueError: Si el valor no es un número entero
                válido o se encuentra fuera del rango
                permitido.
        """

        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ("Debe de ser un número entero")

        if not self.MINIMO <= valor <= self.MAXIMO:
            raise ValueError(f"Los monitores deben de estar entre " f"{self.MINIMO} y {self.MAXIMO}")

        self._monitores = valor

    def factor(self) -> float:
        """Factor propio del subtipo; depende de ``monitores`` y de ``ESCALA``.
        Calcula el factor multiplicativo de un escritorio.

        Determina el incremento de la tarifa según la
        cantidad de monitores disponibles, utilizando
        la constante de clase ESCALA.

        El factor inicia en 1.0 y aumenta 0.1 por
        cada monitor adicional.

        Returns:
            float: Factor multiplicativo correspondiente
                a la cantidad de monitores del escritorio

        """
        # TODO E05: implementar `Escritorio.factor`
        return 1 + self.monitores / self.ESCALA

    def valor_atributo(self) -> int:
        """
        Obtiene el atributo distintivo de un escritorio.

        Recupera la cantidad de monitores disponibles
        mediante la propiedad monitores, permitiendo
        utilizar este valor en operaciones de persistencia,
        reconstrucción y copia de objetos.

        Returns:
            int: Cantidad de monitores del escritorio,
                comprendida entre 0 y 3.
        """
        # TODO E05: implementar `Escritorio.valor_atributo`
        return self._monitores


class SalaJuntas(Privado, Espacio):
    """
    Representa una sala de juntas con acceso restringido.

    Permite administrar salas con capacidad para
    entre 4 y 30 personas. Utiliza ESCALA para
    determinar el incremento de la tarifa según
    la capacidad de la sala.

    Attributes:
        PREFIJO (str): Identificador del subtipo.
        MINIMO (int): Capacidad mínima de personas.
        MAXIMO (int): Capacidad máxima de personas.
        ESCALA (int): Divisor del factor de tarifa,
            cuyo valor es 20.
    """
    # TODO E05: declarar las capacidades que hereda y su orden (§6 y prueba 05)

    PREFIJO: ClassVar[str] = "SAL"
    MINIMO: ClassVar[int] = 4
    MAXIMO: ClassVar[int] = 30
    ESCALA: ClassVar[int] = 20 # TODO E05: valor por deducir de los ejemplos (§6)

    def __init__(self, nombre: str, precio_base: float, capacidad: int, clave: str | None = None) -> None:
        """
        Inicializa una sala de juntas con sus características.

        Reutiliza el constructor de Espacio para establecer
        el nombre, precio base y clave del objeto.
        Posteriormente, asigna la capacidad de personas
        mediante su setter para aplicar las validaciones.

        Args:
            nombre (str): Nombre descriptivo de la sala.
            precio_base (float): Precio diario de la sala.
                Debe ser estrictamente positivo.
            capacidad (int): Número de personas que admite
                la sala. Debe estar entre 4 y 30.
            clave (str | None): Identificador opcional.
                Si es None, se genera automáticamente.

        Raises:
            ValueError: Si el nombre, precio, clave o
                capacidad de personas son inválidos.
        """
        # TODO E05: implementar `SalaJuntas.__init__`
        super.__init__(nombre, precio_base, clave)
        self.capacidad = capacidad

    @property
    def capacidad(self) -> int:
        """"
        Obtiene la capacidad de personas de la sala de juntas.

        Recupera el atributo protegido _capacidad,
        cuyo valor es validado y almacenado previamente
        mediante el setter correspondiente.

        Returns:
            int: Número máximo de personas que admite
                la sala, comprendido entre 4 y 30.
        """
        # TODO E05: implementar `SalaJuntas.capacidad`
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor: int) -> None:
        """
        Establece la capacidad de personas de una sala de juntas.

        Verifica que el valor recibido sea un número entero
        comprendido entre los límites MINIMO y MAXIMO.
        Una vez validado, almacena el valor en el atributo
        protegido _capacidad.

        Args:
            valor (int): Número de personas que admite
                la sala. Debe estar entre 4 y 30.

        Raises:
            ValueError: Si el valor no es un número entero
            válido o se encuentra fuera del rango
            permitido.
        """
        # TODO E05: implementar `SalaJuntas.capacidad`
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("Debe ser numero entero")
        if not self.MINIMO <= valor <= self.MAXIMO:
            raise ValueError(f"La capacidad debe de ser entre " f"{self.MINIMO} y {self.MAXIMO}")

        self._capacidad = valor

    def factor(self) -> float:
        """Factor propio del subtipo; depende de ``aislamiento_db`` y de ``ESCALA``.

        Calcula el factor multiplicativo de una sala de juntas.

        Determina el incremento de la tarifa según la
        capacidad de personas de la sala, utilizando
        la constante ESCALA.

        El factor parte de 1.0 y aumenta 0.05 por cada
        persona adicional de capacidad.

        Returns:
            float: Factor multiplicativo correspondiente
                a la capacidad de personas de la sala.

        """
        # TODO E05: implementar `SalaJuntas.factor`
        return 1 + self.capacidad / self.ESCALA

    def valor_atributo(self) -> int:
        """
        Obtiene el atributo distintivo de una sala de juntas.

        Recupera la capacidad de personas mediante su
        propiedad pública, permitiendo utilizar este
        valor en operaciones de persistencia, copia
        y reconstrucción de objetos.

        Returns:
            int: Capacidad de personas de la sala,
                comprendida entre 4 y 30.
        """
        # TODO E05: implementar `SalaJuntas.valor_atributo`
        return self.capacidad


class Cabina(Equipado, Privado, Espacio):
    """
    Representa una cabina telefónica del coworking.

    Hereda las capacidades Equipado y Privado.
    Su tarifa depende del aislamiento acústico,
    expresado en decibeles, y utiliza una escala
    de 100 para calcular el factor multiplicativo.

    Attributes:
        PREFIJO (str): Prefijo de identificación CAB.
        MINIMO (int): Aislamiento mínimo de 20 dB.
        MAXIMO (int): Aislamiento máximo de 60 dB.
        ESCALA (int): Constante de valor 100 utilizada
            para calcular el factor de la tarifa.
    """

    # TODO E05: declarar las capacidades que hereda y su orden (§6 y prueba 05)

    PREFIJO: ClassVar[str] = "CAB"
    MINIMO: ClassVar[int] = 20
    MAXIMO: ClassVar[int] = 60
    ESCALA: ClassVar[int] = 100 # TODO E05: valor por deducir de los ejemplos (§6)

    def __init__(
        self, nombre: str, precio_base: float, aislamiento_db: int, clave: str | None = None
    ) -> None:
        """
        Inicializa una cabina telefónica del coworking.

        Reutiliza el constructor de Espacio para establecer
        el nombre, precio base y clave de identificación.
        Posteriormente, asigna el aislamiento acústico
        mediante su propiedad para aplicar las validaciones.

        Args:
            nombre (str): Nombre descriptivo de la cabina.
            precio_base (float): Precio diario de la cabina.
                Debe ser estrictamente positivo.
            aislamiento_db (int): Nivel de aislamiento
                acústico en decibeles, entre 20 y 60.
            clave (str | None): Identificador opcional.
                Si es None, se genera automáticamente.

        Raises:
            ValueError: Si el nombre, precio base, clave
                o aislamiento acústico son inválidos.
        """
        # TODO E05: implementar `Cabina.__init__`

        super().__init__(nombre, precio_base,clave)
        self.aislamiento_db = aislamiento_db


    @property
    def aislamiento_db(self) -> int:
        """
        Obtiene el aislamiento acústico de la cabina.

        Recupera el valor almacenado en el atributo
        protegido _aislamiento_db, expresado en decibeles.
        Este valor es validado previamente mediante
        el setter correspondiente.

        Returns:
            int: Nivel de aislamiento acústico de la
                cabina, comprendido entre 20 y 60 dB.
        """

        # TODO E05: implementar `Cabina.aislamiento_db`
        return self._aislamiento_db


    @aislamiento_db.setter
    def aislamiento_db(self, valor: int) -> None:
        """
        Establece el aislamiento acústico de la cabina.

        Verifica que el valor recibido sea un número entero
        comprendido entre los límites MINIMO y MAXIMO.
        Una vez validado, almacena el aislamiento en el
        atributo protegido _aislamiento_db.

        Args:
            valor (int): Nivel de aislamiento acústico
                expresado en decibeles, entre 20 y 60.

        Raises:
            ValueError: Si el valor no es un número entero
                o se encuentra fuera del rango permitido.
        """
        # TODO E05: implementar `Cabina.aislamiento_db`

        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("Debe de ser un número entero")

        if not self.MINIMO <= valor <= self.MAXIMO:
            raise ValueError(f"El aislamiento acústico debe estar entre "
            f"{self.MINIMO} y {self.MAXIMO} dB")

        self._aislamiento_db = valor


    def factor(self) -> float:
        """
        Calcula el factor multiplicativo de una cabina.

        Determina el incremento de la tarifa según el
        aislamiento acústico de la cabina, utilizando
        la constante de clase ESCALA.

        El factor parte de 1.0 y aumenta 0.01 por
        cada decibel adicional de aislamiento.

        Returns:
            float: Factor multiplicativo correspondiente
                al aislamiento acústico de la cabina.
        """

        # TODO E05: implementar `Cabina.factor`

        return self.aislamiento_db / self.ESCALA


    def valor_atributo(self) -> int:
        """
        Obtiene el atributo distintivo de una cabina.

        Recupera el nivel de aislamiento acústico mediante
        la propiedad aislamiento_db, permitiendo utilizar
        este valor en operaciones de persistencia,
        reconstrucción y copia de objetos.

        Returns:
            int: Nivel de aislamiento acústico de la cabina,
                expresado en decibeles y comprendido
                entre 20 y 60.
        """

        # TODO E05: implementar `Cabina.valor_atributo`

        return self._aislamiento_db


    def recargo(self) -> float:
        """Colisión: ambas capacidades definen recargo(); resuélvela de forma explícita (regla: §6).
        Calcula el recargo combinado de una cabina.

        Resuelve explícitamente la colisión del método
        recargo heredado de Equipado y Privado.

        Combina los recargos de ambas capacidades
        mediante una suma, obteniendo un recargo
        total del 23 por ciento.

        Returns:
            float: Recargo combinado de las capacidades
                Equipado y Privado, equivalente a 0.23.
        """
        # TODO E05: implementar `Cabina.recargo`
        return Equipado.RECARGO + Privado.RECARGO