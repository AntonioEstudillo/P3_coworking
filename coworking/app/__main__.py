"""``python -m coworking.app [ruta.db]``: crea/actualiza la base de demostración."""

import sys

from ..servicio.servicio import ServicioCoworking
from .controlador import Controlador, poblar_demo


def main() -> None:
    ruta = sys.argv[1] if len(sys.argv) > 1 else "datos.db"
    with ServicioCoworking(ruta) as servicio:
        poblar_demo(servicio)
        c = Controlador(servicio)
        print(
            f"{len(c.espacios())} espacios, {len(c.socios())} socios, "
            f"{len(c.reservaciones())} reservaciones en {ruta}"
        )
        for nombre, valor in c.reportes().items():
            print(f"{nombre}: {valor}")


if __name__ == "__main__":
    main()
