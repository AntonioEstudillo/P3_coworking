# TODO — Espacio de coworking

Total: **146** tareas en 16 grupos.

| Grupo | Tema | Tareas | Semana |
|---|---|---|---|
| E01 | Configuración del proyecto | 3 | 1 |
| E02 | Contrato raíz (abstracción) | 4 | 1 |
| E03 | Clave (identidad) | 3 | 1 |
| E04 | Clase base abstracta | 7 | 1 |
| E05 | Subtipos y capacidades (herencia múltiple) | 30 | 2 |
| E06 | Actor y niveles (Singleton) | 15 | 2 |
| E07 | Transacción, estados y composición | 16 | 2 |
| E08 | Totales | 4 | 2 |
| E09 | Catálogo (agregación) | 8 | 3 |
| E10 | Tipos anidados y locales | 1 | 3 |
| E11 | Programación funcional | 8 | 3 |
| E12 | Concurrencia y monitor | 8 | 3 |
| E13 | Persistencia SQLite | 15 | 4 |
| E14 | Respaldo pickle | 5 | 4 |
| E15 | Servicio y eventos | 15 | 4 |
| E16 | Reportes | 4 | 4 |

## Detalle

| Grupo | Archivo | Línea | Tarea |
|---|---|---|---|
| E01 | `coworking/__init__.py` | 13 | implementar `info` |
| E01 | `pyproject.toml` | 6 | escribe tu nombre y correo institucional |
| E01 | `pyproject.toml` | 11 | conserva sólo la tecnología de UI que elijas (tkinter viene con Python) |
| E02 | `coworking/modelo/contrato.py` | 25 | implementar `Tarifable.cotizar` |
| E02 | `coworking/modelo/contrato.py` | 30 | implementar `Tarifable.cotizar_con_iva` |
| E02 | `coworking/modelo/contrato.py` | 40 | implementar `Tarifable.redondear` |
| E02 | `coworking/modelo/contrato.py` | 46 | implementar `Tarifable.moneda` |
| E03 | `coworking/modelo/clave.py` | 20 | implementar `Clave.es_valida` |
| E03 | `coworking/modelo/clave.py` | 30 | implementar `Clave.siguiente` |
| E03 | `coworking/modelo/clave.py` | 36 | implementar `Clave.registrar` |
| E04 | `coworking/modelo/elemento.py` | 23 | implementar `Espacio.__init__` |
| E04 | `coworking/modelo/elemento.py` | 29 | implementar `Espacio.clave` |
| E04 | `coworking/modelo/elemento.py` | 35 | implementar `Espacio.nombre` |
| E04 | `coworking/modelo/elemento.py` | 40 | implementar `Espacio.nombre` |
| E04 | `coworking/modelo/elemento.py` | 46 | implementar `Espacio.precio_base` |
| E04 | `coworking/modelo/elemento.py` | 51 | implementar `Espacio.precio_base` |
| E04 | `coworking/modelo/elemento.py` | 73 | implementar `Espacio._calcular` |
| E05 | `coworking/modelo/elemento.py` | 78 | implementar `Espacio.copiar` |
| E05 | `coworking/modelo/elemento.py` | 90 | implementar `Espacio.crear` |
| E05 | `coworking/modelo/elemento.py` | 112 | valor por deducir de los ejemplos (§6) |
| E05 | `coworking/modelo/elemento.py` | 115 | implementar `Equipado.recargo` |
| E05 | `coworking/modelo/elemento.py` | 119 | implementar `Equipado.etiquetas` |
| E05 | `coworking/modelo/elemento.py` | 126 | valor por deducir de los ejemplos (§6) |
| E05 | `coworking/modelo/elemento.py` | 129 | implementar `Privado.recargo` |
| E05 | `coworking/modelo/elemento.py` | 133 | implementar `Privado.etiquetas` |
| E05 | `coworking/modelo/elemento.py` | 140 | declarar las capacidades que hereda y su orden (§6 y prueba 05) |
| E05 | `coworking/modelo/elemento.py` | 145 | valor por deducir de los ejemplos (§6) |
| E05 | `coworking/modelo/elemento.py` | 148 | implementar `Escritorio.__init__` |
| E05 | `coworking/modelo/elemento.py` | 154 | implementar `Escritorio.monitores` |
| E05 | `coworking/modelo/elemento.py` | 159 | implementar `Escritorio.monitores` |
| E05 | `coworking/modelo/elemento.py` | 164 | implementar `Escritorio.factor` |
| E05 | `coworking/modelo/elemento.py` | 168 | implementar `Escritorio.valor_atributo` |
| E05 | `coworking/modelo/elemento.py` | 175 | declarar las capacidades que hereda y su orden (§6 y prueba 05) |
| E05 | `coworking/modelo/elemento.py` | 180 | valor por deducir de los ejemplos (§6) |
| E05 | `coworking/modelo/elemento.py` | 183 | implementar `SalaJuntas.__init__` |
| E05 | `coworking/modelo/elemento.py` | 189 | implementar `SalaJuntas.capacidad` |
| E05 | `coworking/modelo/elemento.py` | 194 | implementar `SalaJuntas.capacidad` |
| E05 | `coworking/modelo/elemento.py` | 199 | implementar `SalaJuntas.factor` |
| E05 | `coworking/modelo/elemento.py` | 203 | implementar `SalaJuntas.valor_atributo` |
| E05 | `coworking/modelo/elemento.py` | 210 | declarar las capacidades que hereda y su orden (§6 y prueba 05) |
| E05 | `coworking/modelo/elemento.py` | 215 | valor por deducir de los ejemplos (§6) |
| E05 | `coworking/modelo/elemento.py` | 220 | implementar `Cabina.__init__` |
| E05 | `coworking/modelo/elemento.py` | 226 | implementar `Cabina.aislamiento_db` |
| E05 | `coworking/modelo/elemento.py` | 231 | implementar `Cabina.aislamiento_db` |
| E05 | `coworking/modelo/elemento.py` | 236 | implementar `Cabina.factor` |
| E05 | `coworking/modelo/elemento.py` | 240 | implementar `Cabina.valor_atributo` |
| E05 | `coworking/modelo/elemento.py` | 245 | implementar `Cabina.recargo` |
| E06 | `coworking/modelo/actor.py` | 22 | implementar `Nivel.__new__` |
| E06 | `coworking/modelo/actor.py` | 32 | implementar `Nivel.desde_nombre` |
| E06 | `coworking/modelo/actor.py` | 46 | implementar `Basico.descuento` |
| E06 | `coworking/modelo/actor.py` | 57 | implementar `Plata.descuento` |
| E06 | `coworking/modelo/actor.py` | 68 | implementar `Oro.descuento` |
| E06 | `coworking/modelo/actor.py` | 81 | implementar `Socio.__init__` |
| E06 | `coworking/modelo/actor.py` | 87 | implementar `Socio.desde_texto` |
| E06 | `coworking/modelo/actor.py` | 92 | implementar `Socio.clave` |
| E06 | `coworking/modelo/actor.py` | 97 | implementar `Socio.nombre` |
| E06 | `coworking/modelo/actor.py` | 102 | implementar `Socio.nombre` |
| E06 | `coworking/modelo/actor.py` | 107 | implementar `Socio.correo` |
| E06 | `coworking/modelo/actor.py` | 112 | implementar `Socio.correo` |
| E06 | `coworking/modelo/actor.py` | 117 | implementar `Socio.nivel` |
| E06 | `coworking/modelo/actor.py` | 122 | implementar `Socio.nivel` |
| E06 | `coworking/modelo/actor.py` | 127 | implementar `Socio.descuento` |
| E07 | `coworking/modelo/transaccion.py` | 26 | traducir el diagrama de estados (§6) a una tabla de transiciones |
| E07 | `coworking/modelo/transaccion.py` | 33 | implementar `Reservacion.Linea.__init__` |
| E07 | `coworking/modelo/transaccion.py` | 39 | implementar `Reservacion.Linea.contenedora` |
| E07 | `coworking/modelo/transaccion.py` | 44 | implementar `Reservacion.Linea.espacio` |
| E07 | `coworking/modelo/transaccion.py` | 49 | implementar `Reservacion.Linea.dias` |
| E07 | `coworking/modelo/transaccion.py` | 65 | implementar `Reservacion.__init__` |
| E07 | `coworking/modelo/transaccion.py` | 70 | implementar `Reservacion.clave` |
| E07 | `coworking/modelo/transaccion.py` | 75 | implementar `Reservacion.socio` |
| E07 | `coworking/modelo/transaccion.py` | 80 | implementar `Reservacion.fecha` |
| E07 | `coworking/modelo/transaccion.py` | 85 | implementar `Reservacion.estado` |
| E07 | `coworking/modelo/transaccion.py` | 91 | implementar `Reservacion.lineas` |
| E07 | `coworking/modelo/transaccion.py` | 96 | implementar `Reservacion.agregar` |
| E07 | `coworking/modelo/transaccion.py` | 101 | implementar `Reservacion._restaurar_linea` |
| E07 | `coworking/modelo/transaccion.py` | 110 | implementar `Reservacion.cambiar_estado` |
| E07 | `coworking/modelo/transaccion.py` | 115 | implementar `Reservacion.antiguedad` |
| E07 | `coworking/modelo/transaccion.py` | 144 | implementar `Reservacion.__str__` |
| E08 | `coworking/modelo/transaccion.py` | 54 | implementar `Reservacion.Linea.importe` |
| E08 | `coworking/modelo/transaccion.py` | 120 | implementar `Reservacion.subtotal` |
| E08 | `coworking/modelo/transaccion.py` | 125 | implementar `Reservacion.descuento` |
| E08 | `coworking/modelo/transaccion.py` | 130 | implementar `Reservacion.total` |
| E09 | `coworking/modelo/catalogo.py` | 15 | implementar `DirectorioEspacios.__init__` |
| E09 | `coworking/modelo/catalogo.py` | 20 | implementar `DirectorioEspacios.agregar` |
| E09 | `coworking/modelo/catalogo.py` | 25 | implementar `DirectorioEspacios.obtener` |
| E09 | `coworking/modelo/catalogo.py` | 29 | implementar `DirectorioEspacios.quitar` |
| E09 | `coworking/modelo/catalogo.py` | 34 | implementar `DirectorioEspacios.todos` |
| E09 | `coworking/modelo/catalogo.py` | 38 | implementar `DirectorioEspacios.__len__` |
| E09 | `coworking/modelo/catalogo.py` | 47 | implementar `DirectorioEspacios.buscar` |
| E09 | `coworking/modelo/catalogo.py` | 52 | implementar `DirectorioEspacios.ordenados` |
| E10 | `coworking/modelo/catalogo.py` | 67 | implementar `DirectorioEspacios.resumen_por_tipo` |
| E11 | `coworking/funcional/reglas.py` | 23 | implementar `Regla.__call__` |
| E11 | `coworking/funcional/reglas.py` | 28 | implementar `Regla.y` |
| E11 | `coworking/funcional/reglas.py` | 33 | implementar `Regla.o` |
| E11 | `coworking/funcional/reglas.py` | 38 | implementar `Regla.negar` |
| E11 | `coworking/funcional/reglas.py` | 47 | implementar `precio_maximo` |
| E11 | `coworking/funcional/reglas.py` | 53 | implementar `de_tipo` |
| E11 | `coworking/funcional/reglas.py` | 59 | implementar `filtrar` |
| E11 | `coworking/funcional/reglas.py` | 65 | implementar `aplicar` |
| E12 | `coworking/concurrencia/tarea.py` | 15 | implementar `TareaPeriodica.__init__` |
| E12 | `coworking/concurrencia/tarea.py` | 20 | implementar `TareaPeriodica.run` |
| E12 | `coworking/concurrencia/tarea.py` | 25 | implementar `TareaPeriodica.detener` |
| E12 | `coworking/servicio/servicio.py` | 39 | implementar `ServicioCoworking.Monitor.__init__` |
| E12 | `coworking/servicio/servicio.py` | 43 | implementar `ServicioCoworking.Monitor.ejecutar` |
| E12 | `coworking/servicio/servicio.py` | 125 | implementar `ServicioCoworking.revisar` |
| E12 | `coworking/servicio/servicio.py` | 129 | implementar `ServicioCoworking.iniciar_monitor` |
| E12 | `coworking/servicio/servicio.py` | 133 | implementar `ServicioCoworking.detener_monitor` |
| E13 | `coworking/persistencia/conexion.py` | 42 | implementar `abrir` |
| E13 | `coworking/persistencia/conexion.py` | 49 | implementar `transaccion` |
| E13 | `coworking/persistencia/repositorios.py` | 55 | implementar `RepositorioEspacio.guardar` |
| E13 | `coworking/persistencia/repositorios.py` | 60 | implementar `RepositorioEspacio.guardar_varios` |
| E13 | `coworking/persistencia/repositorios.py` | 64 | implementar `RepositorioEspacio.obtener` |
| E13 | `coworking/persistencia/repositorios.py` | 68 | implementar `RepositorioEspacio.todos` |
| E13 | `coworking/persistencia/repositorios.py` | 73 | implementar `RepositorioEspacio._mapear` |
| E13 | `coworking/persistencia/repositorios.py` | 81 | implementar `RepositorioSocio.guardar` |
| E13 | `coworking/persistencia/repositorios.py` | 85 | implementar `RepositorioSocio.obtener` |
| E13 | `coworking/persistencia/repositorios.py` | 89 | implementar `RepositorioSocio.todos` |
| E13 | `coworking/persistencia/repositorios.py` | 93 | implementar `RepositorioSocio._mapear` |
| E13 | `coworking/persistencia/repositorios.py` | 112 | implementar `RepositorioReservacion.guardar` |
| E13 | `coworking/persistencia/repositorios.py` | 116 | implementar `RepositorioReservacion.obtener` |
| E13 | `coworking/persistencia/repositorios.py` | 120 | implementar `RepositorioReservacion.todos` |
| E13 | `coworking/persistencia/repositorios.py` | 125 | implementar `RepositorioReservacion._mapear` |
| E14 | `coworking/modelo/transaccion.py` | 135 | implementar `Reservacion.__getstate__` |
| E14 | `coworking/modelo/transaccion.py` | 140 | implementar `Reservacion.__setstate__` |
| E14 | `coworking/persistencia/respaldo.py` | 16 | implementar `respaldar` |
| E14 | `coworking/persistencia/respaldo.py` | 26 | implementar `restaurar` |
| E14 | `coworking/servicio/servicio.py` | 142 | implementar `ServicioCoworking.respaldar` |
| E15 | `coworking/eventos/oyentes.py` | 26 | implementar `OyenteMemoria.notificar` |
| E15 | `coworking/eventos/oyentes.py` | 37 | implementar `OyenteCola.notificar` |
| E15 | `coworking/eventos/oyentes.py` | 42 | implementar `OyenteCola.pendientes` |
| E15 | `coworking/servicio/servicio.py` | 61 | implementar `ServicioCoworking.__enter__` |
| E15 | `coworking/servicio/servicio.py` | 70 | implementar `ServicioCoworking.__exit__` |
| E15 | `coworking/servicio/servicio.py` | 75 | implementar `ServicioCoworking.suscribir` |
| E15 | `coworking/servicio/servicio.py` | 79 | implementar `ServicioCoworking._emitir` |
| E15 | `coworking/servicio/servicio.py` | 84 | implementar `ServicioCoworking.registrar_espacio` |
| E15 | `coworking/servicio/servicio.py` | 88 | implementar `ServicioCoworking.registrar_socio` |
| E15 | `coworking/servicio/servicio.py` | 92 | implementar `ServicioCoworking.socios` |
| E15 | `coworking/servicio/servicio.py` | 97 | implementar `ServicioCoworking.abrir` |
| E15 | `coworking/servicio/servicio.py` | 101 | implementar `ServicioCoworking.agregar_linea` |
| E15 | `coworking/servicio/servicio.py` | 105 | implementar `ServicioCoworking.cambiar_estado` |
| E15 | `coworking/servicio/servicio.py` | 110 | implementar `ServicioCoworking.reservaciones` |
| E15 | `coworking/servicio/servicio.py` | 114 | implementar `ServicioCoworking._requerir` |
| E16 | `coworking/servicio/servicio.py` | 148 | implementar `ServicioCoworking.conteo_por_estado` |
| E16 | `coworking/servicio/servicio.py` | 153 | implementar `ServicioCoworking.ingresos_por_tipo` |
| E16 | `coworking/servicio/servicio.py` | 158 | implementar `ServicioCoworking.top_espacios` |
| E16 | `coworking/servicio/servicio.py` | 163 | implementar `ServicioCoworking.ticket_promedio` |
