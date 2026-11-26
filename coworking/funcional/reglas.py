"""E11. Programación funcional: reglas invocables y combinables.

Referencias: construccion15.py (objetos invocables con ``__call__``),
jerarquia10b.py (funciones como valores), uso de ``lambda`` en los ejemplos.
"""

from collections.abc import Callable, Iterable

from ..modelo.elemento import Espacio

Predicado = Callable[[Espacio], bool]


class Regla:
    """Predicado con nombre; se usa como función: ``regla(espacio)``."""

    def __init__(self, predicado: Predicado, nombre: str = "regla") -> None:
        self._predicado = predicado
        self.nombre = nombre

    def __call__(self, espacio: Espacio) -> bool:
        """
        Evalúa el predicado asociado a la regla.

        Ejecuta la función almacenada en _predicado,
        utilizando el espacio recibido como argumento.

        Permite que una instancia de Regla se utilice
        como si fuera una función.

        Args:
            espacio (Espacio): Espacio sobre el cual
                se evaluará la condición.

        Returns:
            bool: True si el espacio cumple la regla;
                False en caso contrario.
        """
        """Evalúa la regla (construccion15.py)."""
        # TODO E11: implementar `Regla.__call__`
        return self._predicado(espacio)


    def y(self, otra: "Regla") -> "Regla":
        """
        Combina dos reglas mediante una conjunción lógica.

        Crea una nueva instancia de Regla cuyo predicado
        evalúa la regla actual y la regla recibida
        utilizando el operador lógico and.

        La función lambda captura las referencias a
        ambas reglas y devuelve True solamente cuando
        las dos condiciones se cumplen.

        Args:
            otra (Regla): Regla que se combinará con
                la instancia actual.

        Returns:
            Regla: Nueva regla que representa la
                conjunción lógica de ambas condiciones.
        """
        """Conjunción: nueva regla con lambda que captura self y otra."""
        # TODO E11: implementar `Regla.y`
        return Regla(
            lambda espacio: self(espacio) and otra(espacio),
            f"({self.nombre} y {otra.nombre})"
        )

    def o(self, otra: "Regla") -> "Regla":
        """
        Combina dos reglas mediante una disyunción lógica.

        Crea una nueva instancia de Regla cuyo predicado
        evalúa la regla actual o la regla recibida,
        utilizando el operador lógico or.

        La función lambda captura las referencias a
        ambas reglas y devuelve True cuando al menos
        una de las condiciones se cumple.

        Args:
            otra (Regla): Regla que se combinará con
                la instancia actual.

        Returns:
            Regla: Nueva instancia que representa la
                disyunción lógica de ambas reglas.
        """
        """Disyunción."""
        # TODO E11: implementar `Regla.o`
        return Regla(
            lambda espacio: self(espacio) or otra(espacio),
            f"({self.nombre} o {otra.nombre})"
        )

    def negar(self) -> "Regla":
        """
        Crea una nueva regla que niega la condición actual.

        Construye una instancia de Regla cuyo predicado
        evalúa la regla original y utiliza el operador
        lógico not para invertir su resultado.

        La función lambda conserva una referencia a la
        regla original mediante una clausura.

        Returns:
            Regla: Nueva instancia que devuelve True
                cuando la regla original devuelve False,
                y viceversa.
        """
        """Negación."""
        # TODO E11: implementar `Regla.negar`
        return Regla(
            lambda espacio: not self(espacio),
            f"(No {self.nombre}.)"
        )

    def __str__(self) -> str:
        return self.nombre


def precio_maximo(limite: float) -> Regla:
    """
    Crea una regla que comprueba el precio máximo.

    Construye una instancia de Regla cuyo predicado
    verifica que el precio base de un espacio sea
    menor o igual al límite proporcionado.

    La expresión lambda captura el valor de limite
    para utilizarlo cuando se evalúe la regla.

    Args:
        limite (float): Precio base máximo permitido
            para que un espacio cumpla la condición.

    Returns:
        Regla: Nueva regla que devuelve True si el
            precio base del espacio es menor o igual
            al límite y False en caso contrario.
    """
    """Fábrica de reglas: la lambda captura ``limite``."""
    # TODO E11: implementar `precio_maximo`
    return Regla(
        lambda espacio: espacio.precio_base <= limite,
        f"Precio máximo {limite}"
    )


def de_tipo(prefijo: str) -> Regla:
    """
    Crea una regla para identificar un tipo de espacio.

    Construye una instancia de Regla cuyo predicado
    compara el tipo del espacio con el prefijo recibido.

    La función lambda captura el valor del prefijo
    para utilizarlo al evaluar cada espacio.

    Args:
        prefijo (str): Identificador del tipo de espacio
            que se desea comprobar, como "ESC",
            "SAL" o "CAB".

    Returns:
        Regla: Nueva regla que devuelve True cuando
            el tipo del espacio coincide con el
            prefijo indicado y False en caso contrario.
    """
    """Fábrica de reglas por prefijo de subtipo."""
    # TODO E11: implementar `de_tipo`
    return Regla(
        lambda espacio: espacio.tipo == prefijo,
        f"Tipo {prefijo}"
    )


def filtrar(espacios: Iterable[Espacio], regla: Callable[[Espacio], bool]) -> list[Espacio]:
    """
    Filtra una colección de espacios mediante una regla.

    Recorre los espacios recibidos y evalúa cada uno
    utilizando la función proporcionada como regla.

    Devuelve una nueva lista que contiene únicamente
    los espacios para los cuales la regla devuelve True.

    Args:
        espacios (Iterable[Espacio]): Colección de
            espacios que se desea filtrar.
        regla (Callable[[Espacio], bool]): Función
            o instancia invocable que recibe un
            espacio y devuelve un resultado booleano.

    Returns:
        list[Espacio]: Lista de espacios que cumplen
            la regla, conservando su orden original.
    """
    """Función de orden superior: recibe la regla como argumento."""
    # TODO E11: implementar `filtrar`
    return [
        espacio for espacio in espacios if regla(espacio)
    ]


def aplicar(espacios: Iterable[Espacio], funcion: Callable[[Espacio], float]) -> list[float]:
    """
       Aplica una función de transformación a varios espacios.

       Recorre los espacios proporcionados y ejecuta
       la función recibida sobre cada uno de ellos.

       Devuelve una lista con los resultados de la
       transformación, conservando el orden original.

       Args:
           espacios (Iterable[Espacio]): Colección de
               espacios que se desea transformar.
           funcion (Callable[[Espacio], float]): Función
               que recibe un espacio y devuelve un
               valor de tipo float.

       Returns:
           list[float]: Lista con los resultados
               obtenidos al aplicar la función a
               cada espacio.
       """
    """Función de orden superior: transforma cada espacio con ``funcion``."""
    # TODO E11: implementar `aplicar`
    return [
        funcion(espacio) for espacio in espacios
    ]
