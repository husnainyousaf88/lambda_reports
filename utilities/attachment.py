import csv
import zipfile
from io import StringIO, BytesIO


class ZiPFile:
    """
        Class responsible for create ZIP and CSV files..
    """

    def __init__(self):
        pass

    @classmethod
    def create_zip(cls, results, col_names, zip_file_name):
        """
        Create Zip file from headers and rows
        Parameters
        ----------
        results : File Headers(list of string)
        col_names : list of tuple, rows
        zip_file_name : str
        Returns
        -------
        tuple: (zipfile, file_name)
        """
        csv_file = StringIO()
        writer = csv.DictWriter(csv_file, fieldnames=col_names)
        writer.writeheader()
        writer.writerows(results)
        zipped_file = BytesIO()
        with zipfile.ZipFile(zipped_file, 'w', zipfile.ZIP_DEFLATED) as zip:
            zip.writestr(zip_file_name, csv_file.getvalue())
        return zip_file_name, zipped_file
