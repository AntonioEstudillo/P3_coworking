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
        """
        Inserta o actualiza un espacio en la base de datos.

        Convierte los atributos del espacio en parámetros
        SQL y ejecuta la sentencia UPSERT definida
        en el repositorio.

        La operación se realiza dentro de una transacción
        para confirmar los cambios correctamente o
        revertirlos si ocurre un error.

        Args:
            objeto (Espacio): Instancia del espacio
                que se desea insertar o actualizar.

        Raises:
            sqlite3.Error: Si ocurre un error durante
                la operación de persistencia.
        """
        # TODO E13: implementar `RepositorioEspacio.guardar`
        with transaccion(self._con) as con:
            con.execute(
                self._UPSERT,
                self._parametros(objeto)
            )

    def guardar_varios(self, objetos: list[Espacio]) -> None:
        """
        Inserta o actualiza varios espacios en SQLite.

        Recorre los espacios recibidos y genera los
        parámetros necesarios para ejecutar la sentencia
        UPSERT mediante executemany().

        Todas las operaciones se realizan dentro de
        una misma transacción, confirmando los cambios
        si terminan correctamente o revirtiéndolos
        cuando ocurre un error.

        Args:
            objetos (list[Espacio]): Lista de espacios
                que se desean insertar o actualizar.

        Raises:
            sqlite3.Error: Si ocurre un error durante
                la ejecución de las instrucciones SQL.
        """
        """Inserción masiva con ``executemany``."""
        # TODO E13: implementar `RepositorioEspacio.guardar_varios`
        with transaccion(self._con) as con:
            con.executemany(
                self._UPSERT,
                (self._parametros(espacio) for espacio in objetos)
            )

    def obtener(self, clave: str) -> Espacio | None:
        """
        Busca un espacio en la base de datos mediante su clave.

        Ejecuta una consulta SQL para localizar el registro
        correspondiente a la clave proporcionada.

        Si encuentra el registro, utiliza el método _mapear()
        para reconstruir el objeto Espacio correspondiente.
        En caso contrario, devuelve None.

        Args:
            clave (str): Identificador único del espacio
                que se desea recuperar.

        Returns:
            Espacio | None: Objeto del espacio encontrado
                o None si la clave no existe.

        Raises:
            sqlite3.Error: Si ocurre un error al ejecutar
                la consulta sobre la base de datos.
        """
        # TODO E13: implementar `RepositorioEspacio.obtener`
        fila = self._con.execute(
            "SELECT * FROM espacios WHERE clave = ?",
            (clave,)
        ).fetchone()

        if fila is None:
            return None

        return self._mapear(fila)

    def todos(self) -> list[Espacio]:
        """
        Recupera todos los espacios almacenados en SQLite.

        Consulta los registros de la tabla espacios
        ordenados por su clave y convierte cada fila
        en un objeto Espacio mediante el método _mapear().

        Returns:
            list[Espacio]: Lista de espacios reconstruidos
                a partir de los registros encontrados.
                Devuelve una lista vacía si no existen
                espacios almacenados.

        Raises:
            sqlite3.Error: Si ocurre un error durante
                la consulta a la base de datos.
        """
        # TODO E13: implementar `RepositorioEspacio.todos`
        filas = self._con.execute(
            "SELECT * FROM espacios ORDER BY clave"
        ).fetchall()

        return [self._mapear(fila) for fila in filas]

    def _mapear(self, fila: sqlite3.Row) -> Espacio:
        """
        Reconstruye un espacio a partir de una fila SQLite.

        Utiliza la fábrica polimórfica Espacio.crear()
        para identificar el subtipo correspondiente
        mediante la columna tipo.

        Conserva la clave original almacenada en la
        base de datos para mantener la identidad
        del espacio recuperado.

        Args:
            fila (sqlite3.Row): Registro de la tabla
                espacios que contiene los atributos
                necesarios para reconstruir el objeto.

        Returns:
            Espacio: Instancia de Escritorio, SalaJuntas
                o Cabina, según el tipo almacenado.

        Raises:
            ValueError: Si el tipo del espacio no
                corresponde a un subtipo reconocido
                por la fábrica.
        """
        """Reconstrucción polimórfica por la columna ``tipo``."""
        # TODO E13: implementar `RepositorioEspacio._mapear`
        return Espacio(
            prefijo=fila["tipo"],
            nombre=fila["nombre"],
            precio_base=fila["precio_base"],
            valor=fila["valor"],
            clave=fila["clave"]
        )


class RepositorioSocio(Repositorio[Socio]):
    """Persistencia de socios."""

    def guardar(self, objeto: Socio) -> None:
        """
        Inserta o actualiza un socio en la base de datos.

        Almacena la clave, el nombre, el correo y el nivel
        de membresía del socio mediante una sentencia UPSERT.

        El nivel se convierte a su representación textual
        para almacenarlo en SQLite.

        La operación se realiza dentro de una transacción,
        confirmando los cambios cuando termina correctamente
        o revirtiéndolos si ocurre una excepción.

        Args:
            objeto (Socio): Instancia del socio que se
                desea insertar o actualizar.

        Raises:
            sqlite3.Error: Si ocurre un error durante
                la operación de persistencia.
        """
        sql = """
              INSERT INTO socios (clave, nombre, correo, nivel)
              VALUES (?, ?, ?, ?) ON CONFLICT(clave) DO \
              UPDATE SET
                  nombre = excluded.nombre, \
                  correo = excluded.correo, \
                  nivel = excluded.nivel \
              """
        # TODO E13: implementar `RepositorioSocio.guardar`
        parametros = (
            objeto.clave,
            objeto.nombre,
            objeto.correo,
            objeto.nivel.NOMBRE
        )

        with transaccion(self._con) as con:
            con.execute(sql, parametros)

    def obtener(self, clave: str) -> Socio | None:
        """
        Busca un socio en la base de datos mediante su clave.

        Ejecuta una consulta SQL para recuperar el registro
        que corresponde al identificador proporcionado.

        Si encuentra el registro, utiliza el método _mapear()
        para reconstruir el objeto Socio con sus atributos
        y su nivel de membresía.

        Si no existe un registro con esa clave, devuelve None.

        Args:
            clave (str): Identificador único del socio
                que se desea recuperar.

        Returns:
            Socio | None: Instancia del socio encontrado
                o None si no existe un registro con la clave.

        Raises:
            sqlite3.Error: Si ocurre un error durante
                la consulta a la base de datos.
        """
        # TODO E13: implementar `RepositorioSocio.obtener`
        fila = self._con.execute(
            "SELECT clave FROM socios WHERE clave = ?",
            (clave,)
        ).fetchone()
        if fila is None:
            return None

        return self._mapear(fila)

    def todos(self) -> list[Socio]:
        """
        Recupera todos los socios almacenados en SQLite.

        Consulta los registros de la tabla socios
        ordenados por su clave y convierte cada fila
        en una instancia de Socio mediante _mapear().

        Returns:
            list[Socio]: Lista de socios reconstruidos
                a partir de los registros encontrados.
                Devuelve una lista vacía cuando no
                existen socios almacenados.

        Raises:
            sqlite3.Error: Si ocurre un error durante
                la consulta a la base de datos.
        """
        # TODO E13: implementar `RepositorioSocio.todos`
        filas = self._con.execute(
            "SELECT clave FROM socios ORDER BY clave",
        ).fetchall()

        return [self._mapear(fila) for fila in filas]

    def _mapear(self, fila: sqlite3.Row) -> Socio:
        """
        Reconstruye un socio a partir de una fila SQLite.

        Obtiene los atributos almacenados en la tabla
        socios y convierte el nombre del nivel de
        membresía en su instancia Singleton mediante
        Nivel.desde_nombre().

        Conserva la clave original del socio para
        mantener su identidad dentro del sistema.

        Args:
            fila (sqlite3.Row): Registro que contiene
                la clave, nombre, correo y nivel
                del socio.

        Returns:
            Socio: Instancia reconstruida con sus
                atributos y nivel de membresía.

        Raises:
            ValueError: Si el nombre del nivel no
                corresponde a un nivel reconocido.
        """
        # TODO E13: implementar `RepositorioSocio._mapear`
        return Socio(
            nombre=fila["nombre"],
            correo=fila["correo"],
            nivel=Nivel.desde_nombre(fila["nivel"]),
            clave=fila["clave"],
        )


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
        """
        Inserta o actualiza una reservación y sus líneas.

        Guarda los datos principales de la reservación
        mediante UPSERT y reemplaza las líneas existentes
        por las que contiene actualmente el objeto.

        Todas las operaciones se ejecutan dentro de una
        misma transacción para mantener la consistencia
        entre la reservación y sus líneas.

        Args:
            objeto (Reservacion): Reservación que se
                desea insertar o actualizar.

        Raises:
            sqlite3.Error: Si ocurre un error al guardar
                la reservación o cualquiera de sus líneas.
        """
        sql_reservacion = """
                          INSERT INTO reservaciones (clave, socio, fecha, estado, alertada)
                          VALUES (?, ?, ?, ?, ?) ON CONFLICT(clave) DO \
                          UPDATE SET
                              socio = excluded.socio, \
                              fecha = excluded.fecha, \
                              estado = excluded.estado, \
                              alertada = excluded.alertada \
                          """

        sql_linea = """
                    INSERT INTO lineas (reservacion, espacio, dias)
                    VALUES (?, ?, ?) \
                    """

        """Upsert de la transacción y reemplazo de sus líneas en UNA transacción."""
        # TODO E13: implementar `RepositorioReservacion.guardar`
        with transaccion(self._con) as con:
            con.execute(sql_reservacion,(
                objeto.clave,
                objeto.socio.clave,
                objeto.fecha.isoformat(),
                objeto.estado,
                int(objeto.alertada)
            ))

            con.execute("DELETE FROM lineas WHERE reservacion = ?",(objeto.clave,))

            con.executemany(
                sql_linea,
                (
                    (objeto.clave,
                     linea.espacio.clave,
                     linea.dias)

                    for linea in objeto.lineas
                )
            )

    def obtener(self, clave: str) -> Reservacion | None:
        """
        Busca una reservación en SQLite mediante su clave.

        Ejecuta una consulta SQL para localizar el
        registro correspondiente a la clave recibida.

        Si encuentra la reservación, utiliza _mapear()
        para reconstruir el objeto, su socio y las
        líneas que le pertenecen.

        Si no existe un registro con esa clave,
        devuelve None.

        Args:
            clave (str): Identificador único de la
                reservación que se desea recuperar.

        Returns:
            Reservacion | None: Objeto de la reservación
                encontrada o None si no existe.

        Raises:
            sqlite3.Error: Si ocurre un error durante
                la consulta a la base de datos.
        """
        # TODO E13: implementar `RepositorioReservacion.obtener`
        fila = self._con.execute(
            "SELECT clave FROM reservaciones WHERE reservacion = ?",
            (clave,)
        ).fetchone()

        if fila is None:
            return None

        return self._mapear(fila)

    def todos(self) -> list[Reservacion]:
        """
        Recupera todas las reservaciones almacenadas en SQLite.

        Ejecuta una consulta sobre la tabla reservaciones
        y convierte cada registro en un objeto Reservacion
        mediante el método _mapear().

        Las reservaciones se recuperan ordenadas por clave.

        Returns:
            list[Reservacion]: Lista de reservaciones
                reconstruidas, incluyendo sus socios
                y líneas. Devuelve una lista vacía si
                no existen reservaciones almacenadas.

        Raises:
            sqlite3.Error: Si ocurre un error durante
                la consulta a la base de datos.
        """
        # TODO E13: implementar `RepositorioReservacion.todos`
        filas = self._con.execute(
            "SELECT clave FROM reservaciones ORDER BY clave",
        ).fetchall()

        return [self._mapear(fila) for fila in filas]

    def _mapear(self, fila: sqlite3.Row) -> Reservacion:
        """
        Reconstruye una reservación y sus líneas desde SQLite.

        Recupera el socio asociado mediante su repositorio
        y construye la reservación conservando su clave,
        fecha, estado e indicador de alerta originales.

        Posteriormente, consulta las líneas almacenadas
        y restaura cada una mediante _restaurar_linea(),
        utilizando los espacios recuperados del repositorio.

        Args:
            fila (sqlite3.Row): Registro principal de la
                reservación almacenada en SQLite.

        Returns:
            Reservacion: Objeto reconstruido con su socio
                y todas las líneas que le pertenecen.

        Raises:
            ValueError: Si no se encuentra el socio o
                alguno de los espacios referenciados.
            sqlite3.Error: Si ocurre un error en las
                consultas a la base de datos.
        """
        """Reconstruye la transacción, su socio y sus líneas."""
        # TODO E13: implementar `RepositorioReservacion._mapear`
        socio = self._repo_espacios.obtener(fila["socio"])

        if socio is None:
            raise ValueError(f"No se encuentra el socio {fila['socio']} ")

        reservacion = Reservacion(
            socio=socio,
            fecha = date.fromtimestamp(fila["fecha"]),
            clave = fila["clave"],
            estado = fila["estado"],
            alertada= bool(fila["alertada"]),
        )

        fila_lineas = self._con.execute(
            """
            SELECT espacio, dias
            FROM lineas
            WHERE reservacion = ?
            ORDER BY id
            """,
            (fila["clave"],)

        ).fetchall()

        for fila_linea in fila_lineas:
            espacio = self._repo_espacios.obtener(fila_linea["espacio"])

            if espacio is None:
                raise ValueError(f"No se encuentra el espacio {espacio} ")

            reservacion._restaurar_linea(
                espacio,
                fila_linea["dias"],
            )
        return reservacion
