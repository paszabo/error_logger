import csv

from .models import CsvFile


def get_headers_and_data(file_name):
    """
    Get headers and data from a saved CSV file

    Any rows that are all blank are stripped out

    Args:
        file_name: name of the file whose data needs to be retrieved

    Returns: 2-tuple of the form (headers, data)
        `headers` is a list of strings
        `data` is a list of lists of strings
    """
    table_data = CsvFile.objects.get(name=file_name)

    with open(table_data.file.name) as fp:
        reader = csv.reader(fp)
        data = [r for r in reader]

    headers = data[0]
    data = data[1:]

    # strip out blank rows
    data = [d for d in data if any(d)]

    return headers, data
