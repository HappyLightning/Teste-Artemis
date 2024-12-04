import io


def last_lines(filename: str):
    """
    Devolve as linhas de um arquivo em ordem inversa como um iterador.
    """

    def reverse_lines():
        with open(filename, 'rb') as file:
            file.seek(0, io.SEEK_END)  # Vai para o final do arquivo
            buffer = b''  # Inicializa o buffer para linhas parciais
            position = file.tell()  # Tamanho do arquivo em bytes

            while position > 0:
                # Define o tamanho do bloco de leitura (mínimo entre o tamanho restante e o buffer padrão)
                block_size = min(io.DEFAULT_BUFFER_SIZE, position)
                position -= block_size
                file.seek(position)  # Move para a posição do bloco atual

                # Lê o bloco e concatena com o buffer existente
                chunk = file.read(block_size) + buffer
                lines = chunk.split(b'\n')  # Divide o bloco em linhas

                # O último elemento pode ser uma linha incompleta
                buffer = lines.pop(0)

                # Processa as linhas em ordem reversa
                for line in reversed(lines):
                    yield line.decode('utf-8') + '\n'

            # Garante que o buffer restante seja processado (caso contenha a última linha)
            if buffer:
                yield buffer.decode('utf-8') + '\n'

    return iter(reverse_lines())  # Retorna um iterador


# Exemplo de uso:
if __name__ == "__main__":
    print('\nUsando um loop: ')
    for line in last_lines('sample.txt'):
        print(line, end='')

    print('\nChamando o gerador diretamente: ')
    lines = last_lines('sample.txt')
    print(next(lines))
    print(next(lines))
    print(next(lines))
    print(next(lines))
    print(next(lines))
    print(next(lines))
