"""E02. Contrato raíz del dominio Espacio de coworking.

Abstracción (Booch): define QUÉ se puede pedir a todo objeto cotizable,
sin decir CÓMO. Referencias: jerarquia06.py (ABC y @abstractmethod),
construccion09.py (@classmethod y @staticmethod), construccion01.py
(atributos de clase).
"""

from abc import ABC, abstractmethod
from typing import ClassVar


class Tarifable(ABC):
    """Contrato raíz: todo lo que puede cotizarse por un número de días."""

    MONEDA: ClassVar[str] = "MXN"
    IVA: ClassVar[float] = 0.16

    def cotizar(self, dias: int) -> float:
        """Método plantilla: valida ``dias`` y delega en ``_calcular``.
            Valida que la cantidad de días sea positiva y delega
            el cálculo al método _calcular(), implementado por
            las clases concretas que heredan de Tarifable.

            Args:
                dias (int): Número de días de la reservación.
                    Debe ser mayor o igual a 1.
            Returns:
                float: Costo de la reservación, calculado
                    según las reglas del objeto.
            Raises:
                ValueError: Si la cantidad de días es menor que 1..
        """
        # TODO E02: implementar `Tarifable.cotizar`
        if dias < 1:
            return ValueError("dias es menor que 1")
        return self._calcular(dias)

    def cotizar_con_iva(self, dias: int) -> float:
        """Cotización con IVA, redondeada a dos decimales.

            Calcula el costo de una reservación incluyendo el IVA.

            Obtiene el subtotal mediante cotizar(), aplica el
            porcentaje de IVA definido en la clase y redondea
            el resultado a dos decimales.

            Args:
                dias (int): Número de días de la reservación.
                    Debe ser mayor o igual a 1.

            Returns:
                float: Costo total de la reservación con IVA,
                    redondeado a dos decimales.

            Raises:
                ValueError: Si la cantidad de días es menor que 1.
            """

        # TODO E02: implementar `Tarifable.cotizar_con_iva`
        subtotal = self.cotizar(dias)
        total = subtotal * (1 + self.IVA)

        return self.redondear(total)

    @abstractmethod
    def _calcular(self, dias: int) -> float:
        """Paso variable del método plantilla (lo define cada subtipo)."""

    @staticmethod
    def redondear(valor: float) -> float:
        """Redondea a dos decimales (no depende de la instancia)

        Utiliza la función integrada round() de Python
        para obtener un resultado con precisión de dos
        decimales, independientemente de la instancia.

        Args:
            valor (float): Número que se desea redondear.

        Returns:
            float: Valor redondeado a dos decimales.
        """

        # TODO E02: implementar `Tarifable.redondear`
        return round(valor, 2)

    @classmethod
    def moneda(cls) -> str:
        """Devuelve la moneda declarada en la clase (construccion09bis.py).

            Devuelve el atributo de clase MONEDA, permitiendo
            que las subclases utilicen su propia moneda cuando
            sobrescriban dicho atributo.

            Returns:
                str: Código de la moneda definida en la clase.
        """
        # TODO E02: implementar `Tarifable.moneda`
        return cls.MONEDA
