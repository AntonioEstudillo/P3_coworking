"""Pruebas de aceptación (14) — Espacio de coworking.

El docente ejecutará SU copia original de este archivo contra tu entrega:
    pytest -q pruebas_modelo.py
No lo modifiques.
"""

import hashlib
import pickle
import sqlite3
import time
from collections.abc import Iterator
from datetime import date, timedelta
from pathlib import Path

import pytest

from coworking.eventos.oyentes import OyenteMemoria
from coworking.funcional.reglas import Regla, aplicar, de_tipo, filtrar, precio_maximo
from coworking.modelo.actor import Basico, Nivel, Oro, Plata, Socio
from coworking.modelo.catalogo import DirectorioEspacios
from coworking.modelo.clave import Clave
from coworking.modelo.contrato import Tarifable
from coworking.modelo.elemento import Cabina, Equipado, Escritorio, Espacio, Privado, SalaJuntas
from coworking.modelo.transaccion import Reservacion
from coworking.persistencia.conexion import abrir
from coworking.persistencia.repositorios import (
    RepositorioEspacio,
    RepositorioReservacion,
    RepositorioSocio,
)
from coworking.servicio.servicio import ServicioCoworking

HOY = date(2026, 1, 15)


def _sello(*valores: float) -> str:
    """Oráculo sellado: huella SHA-256 de valores redondeados a 4 decimales.

    Las pruebas comparan huellas, no números: debes deducir las reglas de la
    especificación (§6 del DOCX) y comprobar tus hipótesis ejecutando pytest.
    """
    texto = ";".join(f"{v:.4f}" for v in valores)
    return hashlib.sha256(f"coworking|{texto}".encode()).hexdigest()[:20]


@pytest.fixture(autouse=True)
def _claves_limpias() -> Iterator[None]:
    Clave.reiniciar()
    yield


def _trio() -> tuple[Escritorio, SalaJuntas, Cabina]:
    return (
        Escritorio("Uno", 100.0, 2),
        SalaJuntas("Dos", 200.0, 10),
        Cabina("Tres", 300.0, 40),
    )


def _actor(nivel: Nivel | None = None) -> Socio:
    return Socio("Ada Lovelace", "ada@ejemplo.mx", nivel)


def test_01_clave_formato_y_secuencia() -> None:
    assert Clave.es_valida("ABC-0001") and not Clave.es_valida("AB-0001")
    assert Clave.siguiente("XYZ") == "XYZ-0001"
    assert Clave.siguiente("XYZ") == "XYZ-0002"
    Clave.registrar("XYZ-0040")
    assert Clave.siguiente("XYZ") == "XYZ-0041"
    with pytest.raises(ValueError):
        Clave.siguiente("xy")


def test_02_contrato_abstracto_y_plantilla() -> None:
    with pytest.raises(TypeError):
        Espacio("x", 1.0)  # type: ignore[abstract]
    e = Escritorio("Uno", 100.0, 2)
    assert isinstance(e, Tarifable) and Tarifable.moneda() == "MXN"
    with pytest.raises(ValueError):
        e.cotizar(0)
    assert e.cotizar_con_iva(1) == round(e.cotizar(1) * 1.16, 2)


def test_03_encapsulacion_y_validacion() -> None:
    e = Escritorio("  Uno  ", 100.0, 2)
    assert e.nombre == "Uno" and e.clave == "ESC-0001"
    with pytest.raises(ValueError):
        e.nombre = "   "
    with pytest.raises(ValueError):
        e.precio_base = 0
    with pytest.raises(ValueError):
        e.monitores = 3 + 1
    with pytest.raises(AttributeError):
        e.clave = "ESC-0009"  # type: ignore[misc]
    with pytest.raises(ValueError):
        Escritorio("Otro", 10.0, 2, clave="SAL-0001")


def test_04_tarifas_polimorficas() -> None:
    a, b, c = _trio()
    assert _sello(a.cotizar(2)) == "fb22498eb9a7757eb2be"
    assert _sello(b.cotizar(2)) == "14ed883e97c9bc429022"
    assert _sello(c.cotizar(2)) == "840d763d5123121bc8fc"
    assert [x.tipo for x in (a, b, c)] == ["ESC", "SAL", "CAB"]


def test_05_herencia_multiple_y_colision() -> None:
    c = Cabina("Tres", 300.0, 40)
    mro = Cabina.__mro__
    assert mro.index(Equipado) < mro.index(Privado) < mro.index(Espacio)
    assert _sello(round(c.recargo(), 4)) == "b60b5b55933954c589e5"
    assert c.etiquetas() == ["equipado", "privado"]
    assert Escritorio("Uno", 1.0, 2).etiquetas() == ["equipado"]


def test_06_niveles_singleton() -> None:
    assert Basico() is Basico() and Oro() is Nivel.desde_nombre("oro")
    a = Socio.desde_texto("Grace Hopper;grace@ejemplo.mx;PLATA")
    assert a.nivel is Plata() and a.clave == "SOC-0001"
    assert _sello(*(n.descuento() for n in (Basico(), Plata(), Oro()))) == "65bda76d7a57701824cd"
    assert _sello(a.descuento()) == "d2f36b2fabf8fcc6a9ca"
    with pytest.raises(ValueError):
        _actor().correo = "sin-arroba"
    with pytest.raises(ValueError):
        Nivel.desde_nombre("DIAMANTE")


def test_07_estados_y_transiciones() -> None:
    t = Reservacion(_actor(), HOY)
    assert t.estado == Reservacion.ABIERTA
    with pytest.raises(ValueError):
        t.cambiar_estado(Reservacion.EN_CURSO)
    t.agregar(_trio()[0], 1)
    t.cambiar_estado(Reservacion.EN_CURSO)
    with pytest.raises(ValueError):
        t.agregar(_trio()[1], 1)
    t.cambiar_estado(Reservacion.CERRADA)
    with pytest.raises(ValueError):
        t.cambiar_estado(Reservacion.ABIERTA)


def test_08_totales_con_descuento() -> None:
    a, b, c = _trio()
    t = Reservacion(_actor(Oro()), HOY)
    t.agregar(a, 1)
    t.agregar(b, 2)
    t.agregar(c, 3)
    esperado = round(a.cotizar(1) + b.cotizar(2) + c.cotizar(3), 2)
    assert t.subtotal() == esperado
    assert _sello(round(t.descuento() / esperado, 2)) == "a01f0717477dc8ca1d62"
    assert t.total() == round(t.subtotal() - t.descuento(), 2)


def test_09_catalogo_agregacion() -> None:
    a, b, c = _trio()
    cat = DirectorioEspacios(a, b)
    assert cat.agregar(c) == 1 and len(cat) == 3
    with pytest.raises(ValueError):
        cat.agregar(a)
    assert cat.buscar(tipo="SAL") == [b]
    assert cat.buscar(precio_max=250, texto="o") == [a, b]
    assert [e.nombre for e in cat.ordenados("precio", descendente=True)] == ["Tres", "Dos", "Uno"]
    assert cat.resumen_por_tipo() == {"ESC": 1, "SAL": 1, "CAB": 1}
    with pytest.raises(KeyError):
        cat.obtener("ZZZ-0001")


def test_10_tipos_anidados_y_copia() -> None:
    a, _, _ = _trio()
    t = Reservacion(_actor(), HOY)
    linea = t.agregar(a, 2)
    assert isinstance(linea, Reservacion.Linea) and linea.contenedora is t
    assert t.lineas == (linea,) and isinstance(t.lineas, tuple)
    copia = a.copiar()
    assert type(copia) is Escritorio and copia.clave != a.clave and copia.nombre == a.nombre
    assert type(Espacio.crear("CAB", "x", 1.0, 40)) is Cabina


def test_11_reglas_funcionales() -> None:
    a, b, c = _trio()
    barata = precio_maximo(250)
    regla = barata.y(de_tipo("ESC").negar()).o(de_tipo("CAB"))
    assert isinstance(regla, Regla) and callable(regla)
    assert filtrar([a, b, c], regla) == [b, c]
    assert filtrar([a, b, c], lambda e: e.precio_base > 150) == [b, c]
    assert aplicar([a, b], lambda e: e.precio_base * 2) == [200.0, 400.0]


def test_12_monitor_y_concurrencia() -> None:
    dia = [HOY]
    eventos = OyenteMemoria()
    with ServicioCoworking(reloj=lambda: dia[0]) as s:
        s.suscribir(eventos)
        a, b, _ = _trio()
        s.registrar_espacio(a)
        s.registrar_socio(_actor())
        vacia = s.abrir("SOC-0001")
        larga = s.abrir("SOC-0001")
        s.agregar_linea(larga.clave, a.clave, 1)
        s.cambiar_estado(larga.clave, Reservacion.EN_CURSO)
        dia[0] = HOY + timedelta(days=ServicioCoworking.PLAZO + 1)
        assert s.revisar() == (1, 1)
        assert s.revisar() == (0, 0)
        assert [t.estado for t in s.reservaciones()] == [Reservacion.CANCELADA, Reservacion.EN_CURSO]
        assert ("CANCELACION", vacia.clave) in eventos.eventos
        assert sum(1 for e, _ in eventos.eventos if e == "ALERTA") == 1
        s.iniciar_monitor(periodo=0.02)
        monitor = s.monitor
        assert isinstance(monitor, ServicioCoworking.Monitor)
        limite = time.monotonic() + 3
        while monitor.ejecuciones < 2 and time.monotonic() < limite:
            time.sleep(0.01)
        s.detener_monitor()
        assert monitor.ejecuciones >= 2 and not monitor.is_alive()


def test_13_persistencia_sqlite_y_pickle(tmp_path: Path) -> None:
    con = abrir(str(tmp_path / "prueba.db"))
    assert con.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    re = RepositorioEspacio(con)
    ra = RepositorioSocio(con)
    rt = RepositorioReservacion(con, re, ra)
    a, b, c = _trio()
    re.guardar_varios([a, b, c])
    b.precio_base = 250.0
    re.guardar(b)
    assert sorted(type(x).__name__ for x in re.todos()) == sorted(["Escritorio", "SalaJuntas", "Cabina"])
    obtenido = re.obtener(b.clave)
    assert obtenido is not None and obtenido.precio_base == 250.0
    actor = _actor(Plata())
    ra.guardar(actor)
    t = Reservacion(actor, HOY)
    t.agregar(c, 2)
    rt.guardar(t)
    leida = rt.obtener(t.clave)
    assert leida is not None and leida.total() == t.total() and leida.socio.nivel is Plata()
    with pytest.raises(sqlite3.IntegrityError):
        con.execute("INSERT INTO lineas (reservacion, espacio, dias) VALUES ('NOP-0001', ?, 1)", (a.clave,))
    copia = pickle.loads(pickle.dumps(t))
    assert "_candado" not in t.__getstate__()
    assert copia.total() == t.total() and copia.lineas[0].contenedora is copia
    copia.agregar(a, 1)


def test_14_servicio_y_reportes(tmp_path: Path) -> None:
    with ServicioCoworking(str(tmp_path / "s.db"), reloj=lambda: HOY) as s:
        a, b, c = _trio()
        for e in (a, b, c):
            s.registrar_espacio(e)
        s.registrar_socio(_actor(Oro()))
        t1 = s.abrir("SOC-0001")
        s.agregar_linea(t1.clave, a.clave, 2)
        s.agregar_linea(t1.clave, c.clave, 1)
        s.cambiar_estado(t1.clave, Reservacion.EN_CURSO)
        s.cambiar_estado(t1.clave, Reservacion.CERRADA)
        t2 = s.abrir("SOC-0001")
        s.agregar_linea(t2.clave, a.clave, 5)
        conteo = s.conteo_por_estado()
        assert conteo == {"ABIERTA": 1, "EN_CURSO": 0, "CERRADA": 1, "CANCELADA": 0}
        ingresos = s.ingresos_por_tipo()
        assert "SAL" not in ingresos
        assert _sello(round(ingresos["ESC"] / a.cotizar(2), 2)) == "b4ade1d42dae52f6d09b"
        assert s.top_espacios(2) == [(a.clave, 7), (c.clave, 1)]
        cerrada = s.reservaciones(Reservacion.CERRADA)[0]
        assert s.ticket_promedio() == cerrada.total()
        assert s.respaldar(tmp_path / "r.pkl") == 2
    with ServicioCoworking(str(tmp_path / "s.db")) as s2:
        assert len(s2.catalogo) == 3 and len(s2.reservaciones()) == 2
