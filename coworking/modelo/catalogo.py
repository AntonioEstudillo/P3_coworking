"""E09–E10. Catálogo (agregación) y tipos anidados/locales.

Referencias: construccion05.py (``*args`` y ``**kwargs``), demo.py (el todo
referencia partes que existen por sí mismas), jerarquia13.py (clase anidada),
p10_match.py (``match``).
"""

from .elemento import Espacio


class DirectorioEspacios:
    """Agregación de espacios: los contiene, pero no los crea ni los destruye."""

    def __init__(self, *espacios: Espacio) -> None:
        """
        Inicializa un directorio de espacios de coworking.

        Crea un diccionario privado para almacenar los
        espacios utilizando sus claves como identificadores.

        Si se proporcionan espacios inicialmente, delega
        su incorporación al método agregar(), que será
        responsable de validar los registros.

        Args:
            *espacios (Espacio): Cantidad variable de
                espacios que se desean incorporar al
                directorio.

        Raises:
            ValueError: Si agregar() detecta claves
                repetidas o espacios inválidos.
        """
        # TODO E09: implementar `DirectorioEspacios.__init__`
        self.__espacios: dict[str, Espacio] = {}

        if espacios:
            self.agregar(*espacios)

    def agregar(self, *espacios: Espacio) -> int:
        """
        Agrega uno o varios espacios al directorio.

        Valida que cada elemento sea una instancia de
        Espacio y que su clave no se encuentre registrada
        previamente ni repetida entre los nuevos elementos.

        Primero valida todos los espacios y después los
        incorpora al diccionario interno.

        Args:
            *espacios (Espacio): Espacios que se desean
                registrar en el directorio.

        Returns:
            int: Cantidad de espacios agregados.

        Raises:
            ValueError: Si algún elemento no es un Espacio
                válido o si existe una clave duplicada.
        """
        """Agrega uno o varios; rechaza claves repetidas. Devuelve cuántos agregó."""
        # TODO E09: implementar `DirectorioEspacios.agregar`
        nuevos: dict[str, Espacio] = {}

        for espacio in espacios:
            if not isinstance(espacio, Espacio):
                raise ValueError("El elemento debe de ser un espacio")

            clave = espacio.clave

            if clave in self.__espacios or clave in nuevos:
                raise ValueError(f"El clave ya existe {clave}")
            nuevos[clave] = espacio

        self.__espacios.update(espacios)

        return len(espacios)



    def obtener(self, clave: str) -> Espacio:
        """
        Obtiene un espacio registrado en el directorio.

        Busca el espacio utilizando su clave de
        identificación dentro del diccionario interno.

        Args:
            clave (str): Clave del espacio que se
                desea recuperar.

        Returns:
            Espacio: Instancia asociada a la clave
                proporcionada.

        Raises:
            KeyError: Si no existe un espacio registrado
                con la clave indicada.
        """
        """Raises: KeyError si no existe."""
        # TODO E09: implementar `DirectorioEspacios.obtener`
        return self.__espacios[clave]


    def quitar(self, clave: str) -> Espacio:
        """
        Elimina un espacio del directorio mediante su clave.

        Busca la clave indicada en el diccionario interno,
        elimina la entrada correspondiente y devuelve
        la instancia del espacio retirado.

        El espacio conserva su existencia independiente
        del directorio, de acuerdo con la relación
        de agregación.

        Args:
            clave (str): Identificador del espacio
                que se desea retirar.

        Returns:
            Espacio: Instancia del espacio eliminado
                del directorio.

        Raises:
            KeyError: Si la clave proporcionada no
                está registrada en el directorio.
        """
        # TODO E09: implementar `DirectorioEspacios.quitar`
        return self.__espacios.pop(clave)

    def todos(self) -> tuple[Espacio, ...]:
        """Vista inmutable en orden de inserción."""
        """
        Obtiene todos los espacios registrados en el directorio.

        Recupera los valores del diccionario interno y
        los convierte en una tupla, conservando el orden
        en que fueron incorporados.

        La tupla impide modificar directamente la
        colección de espacios desde el exterior.

        Returns:
            tuple[Espacio, ...]: Tupla con las instancias
                de espacios registradas, en orden de
                inserción. Si el directorio está vacío,
                devuelve una tupla vacía.
        """
        # TODO E09: implementar `DirectorioEspacios.todos`
        return tuple(self.__espacios.values())

    def __len__(self) -> int:
        """
        Obtiene la cantidad de espacios registrados.

        Consulta el número de elementos almacenados
        en el diccionario privado del directorio.

        Este método permite utilizar la función len()
        directamente sobre una instancia de
        DirectorioEspacios.

        Returns:
            int: Cantidad de espacios registrados
                actualmente en el directorio.
        """
        # TODO E09: implementar `DirectorioEspacios.__len__`
        return len(self.__espacios)

    def buscar(self, **criterios: object) -> list[Espacio]:
        """
        Busca espacios que cumplan los criterios indicados.

        Permite filtrar por tipo de espacio, texto contenido
        en el nombre y precio base máximo. Cuando se reciben
        varios criterios, todos deben cumplirse.

        Args:
            **criterios (object): Criterios opcionales:
                tipo (str): Prefijo del tipo de espacio.
                texto (str): Texto que debe aparecer en
                    el nombre, sin distinguir mayúsculas.
                precio_max (int | float): Precio base
                    máximo permitido.

        Returns:
            list[Espacio]: Espacios que cumplen todos
                los criterios, en orden de inserción.

        Raises:
            ValueError: Si se proporciona un criterio
                desconocido o un valor de tipo incorrecto.
        """
        """Filtra por ``tipo=``, ``texto=`` (en el nombre) y ``precio_max=``.

        Raises:
            ValueError: criterio desconocido.
        """
        # TODO E09: implementar `DirectorioEspacios.buscar`
        tipo: str | None = None
        texto: str | None = None
        precio_max: float | None = None

        for nombre, valor in criterios.items():
            match nombre:
                case "tipo":
                    if not isinstance(valor, str):
                        raise ValueError("Tipo debe de ser una cadema")
                    tipo = valor.upper()

                case "texto":
                    if not isinstance(valor, str):
                        raise ValueError("Texto debe de ser una cadena")
                    texto = valor.casefold()

                case "precio_max":
                    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                        raise ValueError("Precio max debe ser un numero")
                case _:
                    raise ValueError(f"Criterio desconocido: {nombre}")
            return [espacio for espacio in self.__espacios.values()
                    if (tipo is None or espacio.tipo == tipo) and (texto is None or texto in espacio.nombre.casefold())
                    and (precio_max is None or espacio.precio_base <= precio_max)]


    def ordenados(self, por: str = "nombre", descendente: bool = False) -> list[Espacio]:
        """
            Obtiene los espacios ordenados según un criterio.

            Permite ordenar los espacios por nombre, precio
            base o clave de identificación, tanto de manera
            ascendente como descendente.

            Utiliza expresiones lambda para definir la clave
            de ordenamiento correspondiente.

            Args:
                por (str): Criterio de ordenamiento.
                    Puede ser "nombre", "precio" o "clave".
                    Por defecto es "nombre".
                descendente (bool): Indica si el orden debe
                    ser descendente. Por defecto es False.

            Returns:
                list[Espacio]: Nueva lista con los espacios
                    ordenados según el criterio solicitado.

            Raises:
                ValueError: Si el criterio de ordenamiento
                    no es reconocido.
            """
        """Ordena por ``"nombre"``, ``"precio"`` o ``"clave"`` usando ``key=lambda``."""
        # TODO E09: implementar `DirectorioEspacios.ordenados`
        claves = {
            "nombre": lambda espacio: espacio.nombre.casefold(),
            "precio": lambda espacio: espacio.precio_base,
            "clave": lambda espacio: espacio.clave,
        }

        if por not in claves:
            raise ValueError(f"Criterio desconocido: {por}")

        return sorted(
            self.__espacios.values(),
            key=claves[por],
            reverse=descendente
        )

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
