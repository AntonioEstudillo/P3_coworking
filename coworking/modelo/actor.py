"""E06. Actor del dominio y jerarquía de niveles.

Referencias: construccion08.py (Singleton con ``__new__``), jerarquia07.py
(polimorfismo sobre una ABC), construccion09.py (constructor alternativo con
@classmethod), persona04.py (privado + propiedad de solo lectura).
"""

from abc import ABC, abstractmethod
from typing import ClassVar

from .clave import Clave


class Nivel(ABC):
    """Nivel del socio; cada subclase es un Singleton con su descuento."""

    NOMBRE: ClassVar[str] = ""
    _instancia: ClassVar["Nivel | None"] = None

    def __new__(cls) -> "Nivel":
        """Devuelve siempre la misma instancia por subclase (construccion08.py).

        Obtiene la instancia única del nivel solicitado.

        Implementa el patrón Singleton utilizando el
        atributo de clase _instancia. Si la subclase
        todavía no tiene una instancia, crea una nueva
        mediante el método __new__ de la clase base.

        Si ya existe, devuelve la instancia previamente
        creada, evitando generar objetos duplicados.

        Returns:
            Nivel: Instancia única correspondiente a
                la subclase que invocó el constructor.
        """
        # TODO E06: implementar `Nivel.__new__`
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)

        return cls._instancia

    @abstractmethod
    def descuento(self) -> float:
        """Fracción de descuento (0.0 a 1.0)."""

    @staticmethod
    def desde_nombre(nombre: str) -> "Nivel":
        """Fábrica: ``"BASICO"``, ``"PLATA"`` u ``"ORO"`` → instancia única.
            Obtiene un nivel de membresía a partir de su nombre.

        Normaliza el texto recibido eliminando espacios
        exteriores y convirtiéndolo a mayúsculas.
        Utiliza match para identificar el nivel solicitado
        y devuelve su instancia única mediante Singleton.

        Args:
            nombre (str): Nombre del nivel de membresía.
                Puede ser BASICO, PLATA u ORO, sin distinguir
                entre mayúsculas y minúsculas.

        Returns:
            Nivel: Instancia única de Basico, Plata u Oro,
                según el nombre proporcionado.

        Raises:
            ValueError: Si el nombre no corresponde a un
                nivel válido o no es una cadena de texto.
        """
        # TODO E06: implementar `Nivel.desde_nombre`
        if not isinstance(nombre, str):
            raise ValueError("Nombre no corresponde a una cadena de texto.")

        match nombre.strip().upper():
            case "BASICO":
                return Basico()
            case "PLATA":
                return Plata()
            case "ORO":
                return Oro()
            case _:
                raise ValueError(f"Nivel no encontrado {nombre}")

    def __str__(self) -> str:
        return self.NOMBRE


class Basico(Nivel):
    """Sin descuento."""

    NOMBRE = "BASICO"
    _instancia = None

    def descuento(self) -> float:
        """
        Obtiene el descuento correspondiente al nivel Básico.

        El nivel Básico no aplica descuentos sobre el
        subtotal de una reservación, por lo que devuelve
        una fracción de descuento igual a cero.

        Returns:
            float: Fracción de descuento del nivel Básico,
                equivalente a 0.0 (0 %).
        """
        # TODO E06: implementar `Basico.descuento`
        return 0.0


class Plata(Nivel):
    """Nivel intermedio."""

    NOMBRE = "PLATA"
    _instancia = None

    def descuento(self) -> float:
        """
        Obtiene el descuento correspondiente al nivel Plata.

        El nivel Plata aplica un descuento del cinco
        por ciento sobre el subtotal de una reservación.
        Devuelve la fracción decimal correspondiente
        para utilizarla en los cálculos monetarios.

        Returns:
            float: Fracción de descuento del nivel Plata,
                equivalente a 0.05 (5 %).
        """
        # TODO E06: implementar `Plata.descuento`
        return 0.05


class Oro(Nivel):
    """Nivel superior."""

    NOMBRE = "ORO"
    _instancia = None

    def descuento(self) -> float:
        """
        Obtiene el descuento correspondiente al nivel Oro.

        El nivel Oro aplica un descuento del diez por
        ciento sobre el subtotal de una reservación.
        Devuelve la fracción decimal correspondiente
        para utilizarla en los cálculos monetarios.

        Returns:
            float: Fracción de descuento del nivel Oro,
                equivalente a 0.10 (10 %).
        """
        # TODO E06: implementar `Oro.descuento`
        return 0.10


class Socio:
    """Actor del dominio: miembro del coworking."""

    PREFIJO: ClassVar[str] = "SOC"

    def __init__(
        self, nombre: str, correo: str, nivel: Nivel | None = None, clave: str | None = None
    ) -> None:
        """Nivel por omisión: ``Basico()``.}

        Inicializa un socio del sistema de coworking.

        Establece el nombre, correo electrónico y nivel
        de membresía mediante sus propiedades.
        Si no se proporciona un nivel, asigna Basico().

        Genera una clave nueva cuando no se proporciona
        una existente. Si se recibe una clave, valida
        su formato y prefijo antes de registrarla.

        Args:
            nombre (str): Nombre del socio. No puede estar
                vacío ni contener únicamente espacios.
            correo (str): Correo electrónico del socio.
                Debe contener exactamente una arroba.
            nivel (Nivel | None): Nivel de membresía.
                Por defecto utiliza Basico().
            clave (str | None): Identificador opcional
                con formato SOC-0001. Si es None, se
                genera automáticamente.

        Raises:
            ValueError: Si el nombre, correo, nivel o
                clave no cumplen las reglas del dominio.
        """
        # TODO E06: implementar `Socio.__init__`
        self.nombre = nombre
        self.correo = correo
        self.nivel = Basico() if nivel is None else nivel

        if clave is None:
            self.__clave = Clave.siguiente(self.PREFIJO)
        else:
            if(
            not isinstance(clave, str)
            or not Clave.es_valida(clave)
            or not clave.startswith(f"{self.PREFIJO}")
            ):
                raise ValueError("Clave no valida")

            Clave.registrar(clave)
            self.__clave = clave

    @classmethod
    def desde_texto(cls, texto: str) -> "Socio":
        """Constructor alternativo: ``"Nombre;correo;NIVEL"``.

        Crea un socio a partir de una cadena de texto.

        Divide el texto en nombre, correo y nivel de
        membresía utilizando el punto y coma como
        separador. Elimina los espacios exteriores
        de cada campo y obtiene la instancia del nivel
        correspondiente mediante Nivel.desde_nombre().

        Finalmente, construye y devuelve un socio
        utilizando los datos obtenidos.

        Args:
            texto (str): Cadena con el formato
                "Nombre;correo;NIVEL".

        Returns:
            Socio: Nueva instancia del socio con el
                nombre, correo y nivel especificados.

        Raises:
            ValueError: Si el texto no es una cadena,
                no contiene exactamente tres campos
                o alguno de sus datos es inválido.
        """
        # TODO E06: implementar `Socio.desde_texto`
        if not isinstance(texto, str):
            raise ValueError("Texto no es una cadena")

        partes = [parte.strip() for parte in texto.split(";")]

        if len(partes) != 3:
            raise ValueError("Formato incorrecto, debe ser 'Nombre;correo;Nivel'")

        nombre, correo, nombre_nivel = partes

        nivel = Nivel.desde_nombre(nombre_nivel)

        return cls(nombre, correo, nivel)



    @property
    def clave(self) -> str:
        """
        Obtiene la clave de identificación del socio.

        Recupera el identificador almacenado en el
        atributo privado __clave, que fue generado
        o registrado durante la inicialización del objeto.

        La propiedad permite consultar la clave sin
        proporcionar un setter público para modificarla.

        Returns:
            str: Clave de identificación del socio,
                con formato SOC-0001.
        """
        # TODO E06: implementar `Socio.clave`
        return self.__clave

    @property
    def nombre(self) -> str:
        """
           Obtiene el nombre del socio.

           Recupera el nombre almacenado en el atributo
           protegido _nombre, previamente validado y
           normalizado mediante el setter correspondiente.

           Returns:
               str: Nombre del socio sin espacios
                   exteriores.
           """
        # TODO E06: implementar `Socio.nombre`
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """
        Establece el nombre del socio.

        Verifica que el valor recibido sea una cadena de
        texto y elimina los espacios exteriores mediante
        strip(). Rechaza los nombres vacíos o formados
        únicamente por espacios.

        Args:
            valor (str): Nombre que se asignará al socio.

        Raises:
            ValueError: Si el valor no es una cadena de
                texto o el nombre queda vacío después
                de eliminar los espacios exteriores.
        """
        # TODO E06: implementar `Socio.nombre`
        if not isinstance(valor, str):
            raise ValueError("Texto no es una cadena")

        nombre_limpio = valor.strip()

        if not nombre_limpio:
            ValueError("Valor no puede ser vacio")

        self._nombre = nombre_limpio

    @property
    def correo(self) -> str:
        """
        Obtiene el correo electrónico del socio.

        Recupera el correo almacenado en el atributo
        protegido _correo, previamente validado mediante
        el setter correspondiente.

        Returns:
            str: Correo electrónico del socio.
        """
        # TODO E06: implementar `Socio.correo`
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """
        Establece el correo electrónico del socio.

        Verifica que el valor recibido sea una cadena
        de texto que contenga exactamente una arroba,
        con contenido antes y después de ella.

        Una vez validado, almacena el correo en el
        atributo protegido _correo.

        Args:
            valor (str): Correo electrónico que se
                asignará al socio.

        Raises:
            ValueError: Si el valor no es una cadena,
                no contiene exactamente una arroba
                o carece de contenido antes o después.
        """
        # TODO E06: implementar `Socio.correo`
        if not isinstance(valor, str):
            raise ValueError("Texto no es una cadena")

        if valor.count('@') != 1:
            raise ValueError("El correo debe de contener extactamente un  @")

        usuario, dominio = valor.split('@')

        if not usuario.strip() or not dominio.strip():
            ValueError("El correo debe de tener texto antes y después de @")

        self._correo = valor


    @property
    def nivel(self) -> Nivel:
        """
        Obtiene el nivel de membresía asociado al socio.

        Recupera la instancia de Nivel almacenada en el
        atributo protegido _nivel, previamente asignada
        mediante el setter correspondiente.

        El nivel puede ser una instancia Singleton de
        Basico, Plata u Oro.

        Returns:
            Nivel: Objeto que representa el nivel de
                membresía actual del socio.
        """
        # TODO E06: implementar `Socio.nivel`
        return self._nivel

    @nivel.setter
    def nivel(self, valor: Nivel) -> None:
        """
        Establece el nivel de membresía del socio.

        Verifica que el valor recibido sea una instancia
        de Nivel o de alguna de sus subclases concretas.

        Si el valor es válido, almacena la referencia
        al nivel en el atributo protegido _nivel.

        Args:
            valor (Nivel): Objeto que representa el nivel
                de membresía que se asignará al socio.

        Raises:
            ValueError: Si el valor recibido no es una
        """
        # TODO E06: implementar `Socio.nivel`
        if not isinstance(valor, Nivel):
            ValueError("El nivel debe ser una instancia de Nivel")

        self._nivel = valor

    def descuento(self) -> float:
        """
        Obtiene el descuento correspondiente al socio.

        Delega la operación en el objeto Nivel asociado
        al socio, utilizando polimorfismo para recuperar
        la fracción de descuento según su membresía.

        El porcentaje depende de la implementación
        concreta del nivel: Basico, Plata u Oro.

        Returns:
            float: Fracción de descuento correspondiente
                al nivel actual del socio, entre 0.0 y 1.0.
        """
        """Delegación en el nivel (polimorfismo)."""
        # TODO E06: implementar `Socio.descuento`
        return self.nivel.descuento()

    def __str__(self) -> str:
        return f"{self.clave} {self.nombre} [{self.nivel}]"
