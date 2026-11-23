"""E07–E08 y E14. Transacción con estados, composición de líneas y totales.

Referencias: demo.py y jerarquia13.py (clase anidada), construccion13.py
(la parte la crea el todo), thread07.py (sección crítica), persistencia03.py
(pickle de objetos).
"""

import threading
from datetime import date
from typing import ClassVar

from .actor import Socio
from .clave import Clave
from .contrato import Tarifable
from .elemento import Espacio


class Reservacion:
    """Transacción del dominio: reservación de espacios."""

    PREFIJO: ClassVar[str] = "RES"
    ABIERTA: ClassVar[str] = "ABIERTA"
    EN_CURSO: ClassVar[str] = "EN_CURSO"
    CERRADA: ClassVar[str] = "CERRADA"
    CANCELADA: ClassVar[str] = "CANCELADA"
    # TODO E07: traducir el diagrama de estados (§6) a una tabla de transiciones
    TRANSICIONES: ClassVar[dict[str, tuple[str, ...]]] = {
        ABIERTA: (EN_CURSO, CANCELADA),
        EN_CURSO: (CERRADA, CANCELADA),
        CERRADA: (),
        CANCELADA: (),
    }

    class Linea:
        """Parte de la composición: sólo existe dentro de su transacción."""

        def __init__(self, contenedora: "Reservacion", espacio: Espacio, dias: int) -> None:
            """
            Inicializa una línea perteneciente a una reservación.

            Almacena una referencia a la reservación contenedora,
            el espacio reservado y la cantidad de días.

            Verifica que la reservación y el espacio sean objetos
            de los tipos esperados, y que la cantidad de días
            sea un número entero mayor o igual a uno.

            Args:
                contenedora (Reservacion): Reservación a la que
                    pertenece la línea.
                espacio (Espacio): Espacio que será reservado.
                dias (int): Número de días de la reservación,
                    mayor o igual a uno.

            Raises:
                ValueError: Si la reservación o el espacio no
                    son objetos válidos, o si la cantidad de
                    días no es un entero positivo.
            """
            # TODO E07: implementar `Reservacion.Linea.__init__`
            if not isinstance(contenedora, Reservacion):
                raise ValueError("La contenedora debe de ser una reservación")

            if not isinstance(espacio, Espacio):
                raise ValueError("El espacio debe de ser una instancia de espacio")
            if  isinstance(dias, bool) or not isinstance(dias, int):
                raise ValueError("Los días deben de ser igual o mayor a uno")

            self._contenedora = contenedora
            self._espacio = espacio
            self._dias = dias




        @property
        def contenedora(self) -> "Reservacion":
            """
            Obtiene la reservación a la que pertenece la línea.

            Recupera la referencia a la reservación contenedora
            almacenada durante la inicialización de la línea.

            Esta asociación permite identificar el objeto
            propietario dentro de la relación de composición.

            Returns:
                Reservacion: Instancia de la reservación
                    que contiene a la línea.
            """
            # TODO E07: implementar `Reservacion.Linea.contenedora`
            return self._contenedora

        @property
        def espacio(self) -> Espacio:
            """
            Obtiene la reservación a la que pertenece la línea.

            Recupera la referencia a la reservación contenedora
            almacenada durante la inicialización de la línea.

            Esta asociación permite identificar el objeto
            propietario dentro de la relación de composición.

            Returns:
                Reservacion: Instancia de la reservación
                    que contiene a la línea.
            """
            # TODO E07: implementar `Reservacion.Linea.espacio`
            return self._espacio

        @property
        def dias(self) -> int:
            """
            Obtiene la cantidad de días de la línea de reservación.

            Recupera el número de días almacenado durante la
            inicialización de la línea, previamente validado
            para garantizar que sea un entero positivo.

            Returns:
                int: Cantidad de días reservados, mayor
                    o igual a uno.
            """
            # TODO E07: implementar `Reservacion.Linea.dias`
            return self._dias

        def importe(self) -> float:
            """Importe de la línea = cotización polimórfica del espacio."""
            # TODO E08: implementar `Reservacion.Linea.importe`
            raise NotImplementedError

    def __init__(
        self,
        socio: Socio,
        fecha: date,
        clave: str | None = None,
        estado: str = "ABIERTA",
        alertada: bool = False,
    ) -> None:
        """
        Inicializa una reservación del sistema de coworking.

        Asocia la reservación con un socio y una fecha de
        apertura. Establece su estado inicial, el indicador
        de alerta y una colección vacía de líneas.

        Genera o registra la clave de identificación y
        crea un candado para proteger las operaciones
        concurrentes sobre la reservación.

        Args:
            socio (Socio): Socio propietario de la reservación.
            fecha (date): Fecha de apertura de la reservación.
            clave (str | None): Identificador opcional con
                prefijo RES. Si es None, se genera uno nuevo.
            estado (str): Estado inicial de la reservación.
                Por defecto es ABIERTA.
            alertada (bool): Indica si la reservación ya
                generó una alerta. Por defecto es False.

        Raises:
            ValueError: Si el socio, fecha, clave, estado
                o indicador de alerta son inválidos.
        """
        # TODO E07: implementar `Reservacion.__init__`
        if not isinstance(fecha, date):
            raise ValueError("Fecha debe ser un date")
        if estado not in self.TRANSICIONES:
            raise ValueError("Estado de reservación incorrecto")

        self._socio = socio
        self._fecha = fecha
        self._estado = estado
        self.alertada = alertada

        self._lineas: list[Reservacion.Linea] = []
        self._candado = threading.Lock()

        if clave is None:
            self._clave = Clave.siguiente(self.PREFIJO)
        else:
            if (
                not isinstance(clave, str)
                or not Clave.es_valida(clave)
                or not clave.startwith(f"{self.PREFIJO}")
            ):
                raise ValueError("Clave incorrecto")

            Clave.registrar(clave)
            self.__clave = clave


    @property
    def clave(self) -> str:
        """
        Obtiene la clave de identificación de la reservación.

        Recupera el identificador almacenado en el
        atributo privado __clave, generado o registrado
        durante la inicialización de la reservación.

        La propiedad permite consultar la clave sin
        proporcionar un setter público para modificarla.

        Returns:
            str: Clave de identificación de la reservación,
                con formato RES-0001.
        """
        # TODO E07: implementar `Reservacion.clave`
        return self.__clave


    @property
    def socio(self) -> Socio:
        """
        Obtiene el socio asociado a la reservación.

        Recupera la referencia al objeto Socio almacenado
        durante la inicialización de la reservación.

        Returns:
            Socio: Instancia del socio propietario
                de la reservación.
        """
        # TODO E07: implementar `Reservacion.socio`
        return self._socio

    @property
    def fecha(self) -> date:
        """
        Obtiene la fecha de apertura de la reservación.

        Recupera el objeto date almacenado durante
        la inicialización de la reservación.

        Returns:
            date: Fecha en la que se abrió la reservación.
        """
        # TODO E07: implementar `Reservacion.fecha`
        return self._fecha

    @property
    def estado(self) -> str:
        """
        Obtiene el estado actual de la reservación.

        Recupera el estado almacenado durante la
        inicialización o actualizado mediante el
        método cambiar_estado().

        Returns:
            str: Estado actual de la reservación.
                Puede ser ABIERTA, EN_CURSO, CERRADA
                o CANCELADA.
        """
        # TODO E07: implementar `Reservacion.estado`
        return self._estado

    @property
    def lineas(self) -> tuple["Reservacion.Linea", ...]:
        """
        Obtiene las líneas de la reservación como una tupla.

        Devuelve una representación de solo lectura de la
        colección de líneas, evitando exponer directamente
        la lista interna que administra la reservación.

        Returns:
            tuple[Reservacion.Linea, ...]: Tupla con las
                líneas asociadas a la reservación. Puede
                estar vacía si aún no se han agregado líneas.
        """
        """Vista inmutable de las líneas."""
        # TODO E07: implementar `Reservacion.lineas`
        return tuple(self._lineas)

    def agregar(self, espacio: Espacio, dias: int) -> "Reservacion.Linea":
        """
            Agrega una línea de espacio a la reservación.

            Comprueba que la reservación se encuentre en estado
            ABIERTA. Si se cumple la condición, crea una línea
            asociada a la reservación y la incorpora a su
            colección interna.

            La operación se protege mediante un candado para
            evitar modificaciones concurrentes inconsistentes.

            Args:
                espacio (Espacio): Espacio que se desea reservar.
                dias (int): Cantidad de días de la reservación,
                    mayor o igual a uno.

            Returns:
                Reservacion.Linea: Nueva línea creada y agregada
                    a la reservación.

            Raises:
                ValueError: Si la reservación no está ABIERTA
                    o los datos de la línea son inválidos.
            """
        """Crea y posee una línea; sólo en estado ABIERTA. Sección crítica."""
        # TODO E07: implementar `Reservacion.agregar`
        with self._candado:
            if self._estado != self.ABIERTA:
                raise ValueError("Solo se pueden agregar líneas en estado ABIERTA")

            linea = Reservacion.Linea(self, espacio, dias)
            self._lineas.append(linea)
            return linea

    def _restaurar_linea(self, espacio: Espacio, dias: int) -> None:
        """
        Restaura una línea previamente almacenada.

        Crea una línea asociada a la reservación y la
        incorpora a su colección interna sin comprobar
        el estado actual de la transacción.

        Este método está destinado exclusivamente a
        reconstruir reservaciones desde la persistencia.

        Args:
            espacio (Espacio): Espacio asociado a la línea
                que se desea reconstruir.
            dias (int): Cantidad de días originalmente
                reservados, mayor o igual a uno.

        Raises:
            ValueError: Si el espacio o la cantidad de
                días no cumplen las validaciones de Linea.
        """
        """Uso exclusivo de persistencia: agrega sin validar el estado."""
        # TODO E07: implementar `Reservacion._restaurar_linea`
        with self._candado:
            linea = Reservacion.Linea(self, espacio, dias)
            self._lineas.append(linea)

    def cambiar_estado(self, nuevo: str) -> None:
        """
        Cambia el estado de la reservación.

        Verifica que la transición solicitada esté permitida
        en la tabla TRANSICIONES. Para pasar al estado
        EN_CURSO, comprueba además que la reservación
        contenga al menos una línea.

        Protege la validación y la actualización del estado
        mediante un candado para evitar modificaciones
        concurrentes inconsistentes.

        Args:
            nuevo (str): Estado al que se desea cambiar
                la reservación.

        Raises:
            ValueError: Si la transición no está permitida
                o si se intenta iniciar una reservación
                que no contiene líneas.
        """
        """Aplica una transición válida de TRANSICIONES.

        Raises:
            ValueError: transición no permitida o EN_CURSO sin líneas.
        """
        # TODO E07: implementar `Reservacion.cambiar_estado`
        with self._candado:
            permitidos = self.TRANSICIONES[self._estado]

            if nuevo not in permitidos:
                raise ValueError(f"No se puede cambiar estado: {self._estado} -> {nuevo}")

            if nuevo == self.EN_CURSO and not self._lineas:
                raise ValueError("No se puede iniciar una reservación sin líneas")

            self._estado = nuevo



    def antiguedad(self, hoy: date) -> int:
        """
        Calcula la antigüedad de la reservación en días.

        Obtiene la diferencia entre la fecha proporcionada
        y la fecha de apertura de la reservación.

        Args:
            hoy (date): Fecha de referencia utilizada
                para calcular los días transcurridos.

        Returns:
            int: Diferencia en días entre la fecha de
                referencia y la fecha de apertura.
        """
        """Días transcurridos desde la apertura."""
        # TODO E07: implementar `Reservacion.antiguedad`
        return (hoy - self.fecha).days

    def subtotal(self) -> float:
        """Suma de importes de las líneas."""
        # TODO E08: implementar `Reservacion.subtotal`
        raise NotImplementedError

    def descuento(self) -> float:
        """Monto de descuento según el nivel del socio."""
        # TODO E08: implementar `Reservacion.descuento`
        raise NotImplementedError

    def total(self) -> float:
        """Total = subtotal - descuento."""
        # TODO E08: implementar `Reservacion.total`
        raise NotImplementedError

    def __getstate__(self) -> dict[str, object]:
        """Excluye el candado (no serializable), equivalente a ``transient``."""
        # TODO E14: implementar `Reservacion.__getstate__`
        raise NotImplementedError

    def __setstate__(self, estado: dict[str, object]) -> None:
        """Restaura atributos y crea un candado nuevo."""
        # TODO E14: implementar `Reservacion.__setstate__`
        raise NotImplementedError

    def __str__(self) -> str:
        """
        Devuelve una representación textual de la reservación.

        Construye una cadena con la clave de identificación,
        el nombre del socio, el estado actual, la fecha de
        apertura y la cantidad de líneas registradas.

        Returns:
            str: Descripción legible de la reservación.
        """
        # TODO E07: implementar `Reservacion.__str__`
        return (
            f"{self.clave} {self.socio.nombre}"
            f"[{self.estado}]"
            f"({self.fecha.isoformat()}, "
            f"{len(self.lineas)} lineas)"
        )
