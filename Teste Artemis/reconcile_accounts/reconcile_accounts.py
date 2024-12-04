import csv
from pathlib import Path
from pprint import pprint
from datetime import datetime
from copy import deepcopy
from typing import List


def reconcile_accounts(transactions1: List[List[str]], transactions2: List[List[str]]):
    # Converte as listas de listas em cópias mutáveis para evitar alterar os dados originais
    t1 = deepcopy(transactions1)
    t2 = deepcopy(transactions2)

    # Adiciona uma coluna inicial de status a todas as transações como "MISSING"
    for transaction in t1:
        transaction.append("MISSING")
    for transaction in t2:
        transaction.append("MISSING")

    def transactions_match(t1_row, t2_row):
        return (
                t1_row[1] == t2_row[1] and  # Departamento
                t1_row[2] == t2_row[2] and  # Valor
                t1_row[3] == t2_row[3]  # Beneficiário
        )

    # Percorre cada transação em t1 e tenta conciliá-la em t2
    for t1_row in t1:
        t1_date = datetime.strptime(t1_row[0], "%Y-%m-%d")  # Data como objeto datetime
        found_match = False

        for t2_row in t2:
            if t2_row[4] == "FOUND":  # Ignorar transações já conciliadas
                continue

            t2_date = datetime.strptime(t2_row[0], "%Y-%m-%d")
            # Checa se as transações correspondem, considerando a data +/- 1 dia
            if transactions_match(t1_row, t2_row) and abs((t1_date - t2_date).days) <= 1:
                t1_row[4] = "FOUND"  # Atualiza a posição da transação
                t2_row[4] = "FOUND"
                found_match = True
                break

    return t1, t2


if __name__ == "__main__":
    transactions1 = list(csv.reader(Path('transactions1.csv').open(encoding='utf-8')))
    transactions2 = list(csv.reader(Path('transactions2.csv').open(encoding='utf-8')))

    out1, out2 = reconcile_accounts(transactions1, transactions2)
    pprint(out1)
    pprint(out2)
