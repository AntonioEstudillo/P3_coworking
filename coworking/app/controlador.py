"""Capa de aplicación: puerto único entre la UI y el servicio.

La UI (escritorio o web) SÓLO importa este módulo: recibe y entrega tipos
simples (``str``, ``int``, ``float``, ``dict``) y nunca toca ``sqlite3``.
"""

from datetime import date, timedelta

from ..eventos.oyentes import OyenteCola
from ..modelo.actor import Nivel, Socio
from ..modelo.elemento import Espacio
from ..servicio.servicio import ServicioCoworking

Fila = dict[str, str]

TIPOS: dict[str, str] = {
    "ESC": "Escritorio (monitores)",
    "SAL": "SalaJuntas (capacidad)",
    "CAB": "Cabina (aislamiento_db)",
}
ESTADOS: tuple[str, ...] = ("ABIERTA", "EN_CURSO", "CERRADA", "CANCELADA")


class Controlador:
    """Adaptador de la UI: traduce eventos de interfaz a casos de uso."""

    def __init__(self, servicio: ServicioCoworking) -> None:
        self._s = servicio
        self.eventos = OyenteCola()
        servicio.suscribir(self.eventos)

    def espacios(self) -> list[Fila]:
        return [
            {
                "clave": e.clave,
                "tipo": e.tipo,
                "nombre": e.nombre,
                "precio": f"{e.precio_base:.2f}",
                "atributo": str(e.valor_atributo()),
            }
            for e in self._s.catalogo.ordenados("clave")
        ]

    def socios(self) -> list[Fila]:
        return [
            {"clave": a.clave, "nombre": a.nombre, "correo": a.correo, "nivel": str(a.nivel)}
            for a in self._s.socios()
        ]

    def reservaciones(self) -> list[Fila]:
        return [
            {
                "clave": t.clave,
                "socio": t.socio.nombre,
                "fecha": t.fecha.isoformat(),
                "estado": t.estado,
                "lineas": str(len(t.lineas)),
                "total": f"{t.total():.2f}",
            }
            for t in self._s.reservaciones()
        ]

    def alta_espacio(self, tipo: str, nombre: str, precio: float, valor: int) -> str:
        e = Espacio.crear(tipo, nombre, precio, valor)
        self._s.registrar_espacio(e)
        return e.clave

    def alta_socio(self, nombre: str, correo: str, nivel: str) -> str:
        a = Socio(nombre, correo, Nivel.desde_nombre(nivel))
        self._s.registrar_socio(a)
        return a.clave

    def abrir(self, clave_socio: str) -> str:
        return self._s.abrir(clave_socio).clave

    def agregar(self, clave_reservacion: str, clave_espacio: str, dias: int) -> None:
        self._s.agregar_linea(clave_reservacion, clave_espacio, dias)

    def cambiar(self, clave_reservacion: str, estado: str) -> None:
        self._s.cambiar_estado(clave_reservacion, estado)

    def revisar(self) -> tuple[int, int]:
        return self._s.revisar()

    def reportes(self) -> dict[str, str]:
        return {
            "Conteo por estado": str(self._s.conteo_por_estado()),
            "Ingresos por tipo": str(self._s.ingresos_por_tipo()),
            "Top espacios": str(self._s.top_espacios()),
            "Ticket promedio": f"{self._s.ticket_promedio():.2f}",
        }

    def pendientes(self) -> list[str]:
        """Eventos acumulados por otros hilos (se consumen en el hilo de la UI)."""
        return [f"{e}: {d}" for e, d in self.eventos.pendientes()]


def poblar_demo(servicio: ServicioCoworking) -> None:
    """Datos mínimos exigidos: 6 espacios, 3 socios y 4 reservaciones (una por estado)."""
    if servicio.catalogo.todos():
        return
    ejemplos = [
        Espacio.crear("ESC", "Escritorio ventana", 150.0, 2),
        Espacio.crear("ESC", "Escritorio flex", 120.0, 1),
        Espacio.crear("SAL", "Sala Pico", 700.0, 12),
        Espacio.crear("SAL", "Sala Río Blanco", 450.0, 6),
        Espacio.crear("CAB", "Cabina A", 200.0, 45),
        Espacio.crear("CAB", "Cabina B", 180.0, 30),
    ]
    for e in ejemplos:
        servicio.registrar_espacio(e)
    actores = [
        Socio.desde_texto("Luis Martínez;luis0@ejemplo.mx;BASICO"),
        Socio.desde_texto("Startup Nogales;startup1@ejemplo.mx;PLATA"),
        Socio.desde_texto("Despacho Rincón;despacho2@ejemplo.mx;ORO"),
    ]
    for a in actores:
        servicio.registrar_socio(a)
    abierta = servicio.abrir(actores[0].clave)
    servicio.agregar_linea(abierta.clave, ejemplos[0].clave, 1)
    en_curso = servicio.abrir(actores[1].clave)
    servicio.agregar_linea(en_curso.clave, ejemplos[2].clave, 2)
    servicio.cambiar_estado(en_curso.clave, "EN_CURSO")
    cerrada = servicio.abrir(actores[2].clave)
    servicio.agregar_linea(cerrada.clave, ejemplos[4].clave, 3)
    servicio.agregar_linea(cerrada.clave, ejemplos[1].clave, 1)
    servicio.cambiar_estado(cerrada.clave, "EN_CURSO")
    servicio.cambiar_estado(cerrada.clave, "CERRADA")
    cancelada = servicio.abrir(actores[0].clave)
    servicio.cambiar_estado(cancelada.clave, "CANCELADA")


def reloj_demo() -> date:
    """Reloj de ejemplo desplazado; útil para observar el monitor en la UI."""
    return date.today() + timedelta(days=ServicioCoworking.PLAZO + 1)
