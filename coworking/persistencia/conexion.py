"""E13. Conexión SQLite, esquema y transacciones como context manager.

Referencias: p21_contexto1.py y p22_contexto2.py (``@contextmanager``),
p23_contexto3.py (adquirir y liberar un recurso). Biblioteca: ``sqlite3``
(estándar). Investigación del estudiante: ``row_factory``, ``PRAGMA``,
``executemany`` e ``INSERT ... ON CONFLICT`` en la documentación de sqlite3.
"""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager

DDL = """
CREATE TABLE IF NOT EXISTS espacios (
    clave        TEXT PRIMARY KEY CHECK (length(clave) = 8),
    tipo         TEXT NOT NULL CHECK (tipo IN ('ESC', 'SAL', 'CAB')),
    nombre       TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    precio_base  REAL NOT NULL CHECK (precio_base > 0),
    atributo     INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS socios (
    clave   TEXT PRIMARY KEY CHECK (length(clave) = 8),
    nombre  TEXT NOT NULL,
    correo  TEXT NOT NULL UNIQUE,
    nivel   TEXT NOT NULL CHECK (nivel IN ('BASICO', 'PLATA', 'ORO'))
);
CREATE TABLE IF NOT EXISTS reservaciones (
    clave     TEXT PRIMARY KEY CHECK (length(clave) = 8),
    socio   TEXT NOT NULL REFERENCES socios(clave),
    fecha     TEXT NOT NULL,
    estado    TEXT NOT NULL
              CHECK (estado IN ('ABIERTA', 'EN_CURSO', 'CERRADA', 'CANCELADA')),
    alertada  INTEGER NOT NULL DEFAULT 0 CHECK (alertada IN (0, 1))
);
    
    
CREATE TABLE IF NOT EXISTS lineas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    reservacion TEXT NOT NULL,
    espacio TEXT NOT NULL,
    dias INTEGER NOT NULL CHECK (dias >= 1),

    FOREIGN KEY (reservacion)
        REFERENCES reservaciones(clave)
        ON DELETE CASCADE,

    FOREIGN KEY (espacio)
        REFERENCES espacios(clave)
        ON DELETE RESTRICT
);
-- TODO E13: diseña la tabla lineas (composición): llave, llaves foráneas,
-- política de borrado y restricciones. Justifícala en el README (§7).
"""


def abrir(ruta: str) -> sqlite3.Connection:
    """
    Abre y configura una conexión a SQLite.

    Establece una conexión con la base de datos
    indicada, permite su uso entre distintos hilos,
    habilita las restricciones de claves foráneas
    y configura el acceso a las filas mediante
    nombres de columnas.

    Finalmente, ejecuta las instrucciones DDL
    para crear las tablas que todavía no existan.

    Args:
        ruta (str): Ruta del archivo SQLite que
            se desea abrir o crear. También puede
            utilizarse ":memory:".

    Returns:
        sqlite3.Connection: Conexión SQLite
            configurada y lista para utilizarse.

    Raises:
        sqlite3.Error: Si ocurre un error al abrir
            la base o ejecutar las instrucciones SQL.
    """
    """Abre la base, activa llaves foráneas, configura ``row_factory`` y crea el esquema."""
    # TODO E13: implementar `abrir`
    con = sqlite3.connect(
        ruta, check_same_thread=False
    )

    try:
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys=ON")
        con.executescript(DDL)

    except Exception:
        con.close()
        raise

    return con


@contextmanager
def transaccion(con: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    """
    Administra una transacción sobre una conexión SQLite.

    Permite ejecutar varias operaciones SQL como una
    unidad de trabajo mediante un administrador de
    contexto.

    Si las operaciones terminan correctamente,
    confirma los cambios utilizando commit().

    Si ocurre una excepción, revierte los cambios
    pendientes mediante rollback() y propaga
    nuevamente la excepción.

    Args:
        con (sqlite3.Connection): Conexión SQLite
            utilizada para ejecutar las operaciones.

    Yields:
        sqlite3.Connection: Conexión disponible
            durante el bloque de la transacción.

    Raises:
        Exception: Propaga cualquier excepción
            ocurrida durante las operaciones o
            la confirmación de los cambios.
    """
    """Unidad de trabajo: ``commit`` al salir bien, ``rollback`` ante excepción."""
    # TODO E13: implementar `transaccion`
    try:
        yield con
        con.commit()

    except Exception:
        con.rollback()
        raise
