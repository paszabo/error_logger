import csv

from .models import CsvFile


def get_headers_and_data(file_name, strip_blank_lines=True):
    """
    Get headers and data from a saved CSV file

    Any rows that are all blank are stripped out

    Args:
        file_name: name of the file whose data needs to be retrieved
        strip_blank_lines: set True if lines of all empty (Python falsey)
            values should be removed.

            Note: 0 is a falsey value so be careful, a line of all 0s will
                be stripped if this is true

    Returns: 2-tuple of the form (headers, data)
        `headers` is a list of strings
        `data` is a list of lists of strings
    """
    csv_file = CsvFile.objects.get(name=file_name)

    csv_file.file.open(mode='rt')
    reader = csv.reader(csv_file.file)
    data = [r for r in reader]
    csv_file.file.close()

    assert csv_file.file.closed

    headers = data[0]
    data = data[1:]

    if strip_blank_lines:
        data = [d for d in data if any(d)]

    return headers, data
