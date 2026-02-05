import csv
import uuid
from typing import TextIO
from datetime import datetime
from app.utils.normalizer.strings import normalize_string_utf8_to_ascii
from app.models.transaction import Transaction


class NubankParser:

    def parseBankStatementCSV(self, file: TextIO) -> list[Transaction]:

        reader = csv.DictReader(file)
        fieldname_normalizes = [normalize_string_utf8_to_ascii(
            fieldname.lower()) for fieldname in reader.fieldnames]

        for fieldname in fieldname_normalizes:
            if fieldname not in ['data', 'valor', 'identificador', 'descricao']:
                raise ValueError(
                    f"The CSV has an unexpected fieldname: {fieldname} \n"
                    f"Expected fieldnames are: ['data', 'valor', 'identificador', 'descricao']")

        transaction_array = []

        for row in reader:
            transaction_data = {}
            for key, value in row.items():
                key = normalize_string_utf8_to_ascii(key.lower())
                value = normalize_string_utf8_to_ascii(value)
                transaction_data[key] = value
            date_obj = datetime.strptime(
                transaction_data['data'], "%d/%m/%Y").date()
            transaction = Transaction(
                date=date_obj,
                id=transaction_data['identificador'],
                value=abs(float(transaction_data['valor'])),
                is_expense=True if float(
                    transaction_data['valor']) < 0 else False,
                description=transaction_data['descricao'],
            )
            transaction_array.append(transaction)

        return transaction_array

    def parseCreditCardStatementCSV(self, file: TextIO) -> list[Transaction]:

        reader = csv.DictReader(file)
        fieldname_normalizes = [normalize_string_utf8_to_ascii(
            fieldname.lower()) for fieldname in reader.fieldnames]

        for fieldname in fieldname_normalizes:
            if fieldname not in ['date', 'title', 'amount']:
                raise ValueError(
                    f"The CSV has an unexpected fieldname: {fieldname} \n"
                    f"Expected fieldnames are: ['date', 'title', 'amount']")

        transaction_array = []

        for row in reader:
            transaction_data = {}
            for key, value in row.items():
                key = normalize_string_utf8_to_ascii(key.lower())
                value = normalize_string_utf8_to_ascii(value)
                transaction_data[key] = value
            date_obj = datetime.strptime(
                transaction_data['date'], "%d/%m/%Y").date()
            transaction = Transaction(
                date=date_obj,
                id=str(uuid.uuid4()),
                value=abs(float(transaction_data['amount'])),
                is_expense=True if float(
                    transaction_data['amount']) > 0 else False,
                description=transaction_data['title'],
            )
            transaction_array.append(transaction)

        return transaction_array
