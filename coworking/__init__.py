"""Espacio de coworking — miniproyecto de Tecnologías de Programación (TecNM, IT Orizaba).

Paquetes: modelo, funcional, eventos, concurrencia, persistencia, servicio, app, ui.
Dependencias permitidas: ui → app → servicio → {modelo, funcional, eventos,
concurrencia, persistencia}; persistencia → modelo; modelo no depende de nadie.
"""

PROYECTO = "Espacio de coworking"


def info() -> dict[str, str]:
    """Metadatos del proyecto mostrados por la UI y el README."""
    # TODO E01: implementar `info`
    return {
        "PROYECTO": PROYECTO,
        "version": "1.0",
        "descripcion": "Sistema de gestión de espacios de Coworking",
    }
