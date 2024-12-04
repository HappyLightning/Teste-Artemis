from typing import Any, Callable


class cached_property:
    """
    Um decorador que cacheia o valor de uma propriedade, recalculando-o apenas quando
    um dos atributos dos quais depende for alterado.

    Atributos:
        dependencies: Uma lista de atributos da instância dos quais a propriedade depende.
    """
    def __init__(self, *dependencies: str):
        """
        Inicializa o decorador com os nomes dos atributos que a propriedade depende.

        Args:
            dependencies: nomes dos atributos que afetam o valor da propriedade.
        """
        self.dependencies = dependencies

    def __call__(self, func: Callable[..., Any]) -> property:
        """
        Faz o decorador funcionar como um decorador de propriedade.

        Args:
            func: A função que será usada para calcular o valor da propriedade.

        Returns:
            property: Um objeto de propriedade que faz o cache e valida a dependência.
        """
        def getter(instance: Any) -> Any:
            """
            Recupera o valor da propriedade cacheada ou recalcula se as dependências mudaram.

            Args:
                instance: A instância da classe que usa a propriedade decorada.

            Returns:
                O valor cacheado ou recalculado da propriedade.
            """
            # Verifica se a instância possui cache ou estados de dependência
            if not hasattr(instance, '_cache'):
                instance._cache = {}
            if not hasattr(instance, '_dependency_states'):
                instance._dependency_states = {}

            # Obtém os estados atuais das dependências
            current_states = {dep: getattr(instance, dep) for dep in self.dependencies}

            # Verifica se o valor está cacheado e as dependências não mudaram
            if (func.__name__ in instance._cache and
                    instance._dependency_states.get(func.__name__) == current_states):
                return instance._cache[func.__name__]

            # Se as dependências mudaram ou o valor não está cacheado, recalcula o valor
            value = func(instance)
            instance._cache[func.__name__] = value
            instance._dependency_states[func.__name__] = current_states
            return value

        return property(getter)



class Vector:
    def __init__(self, x, y, z, color=None):
        self.x, self.y, self.z = x, y, z
        self.color = color

    @cached_property('x', 'y', 'z')
    def magnitude(self):
        print('computing magnitude')

        # A magnitude (norma) deve incluir a raiz quadrada.
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5


if __name__ == "__main__":
    v = Vector(9, 2, 6)
    print(v.magnitude)  # 11.0.
    v.color = 'red'
    print(v.magnitude)  # 11.0, não recalculado porque 'color' não é dependência.
    v.y = 18
    print(v.magnitude)  # Recalcula porque 'y' mudou.
