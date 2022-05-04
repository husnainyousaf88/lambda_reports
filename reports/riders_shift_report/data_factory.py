from reports.riders_shift_report.queries import SHIFT_DATA
from settings.base import connection
from datetime import datetime, timedelta, timezone


class DataFactory:
    """
    Class  responsible for providing requrired data and stats for rider shift report
    """
    def __init__(self):
        pass

    @staticmethod
    def get_rider_shift_data(start_date, end_date, rider):
        """
        get rider shift data
        ___________________
        :param start_date: datetime.date
        :param end_date: datetime.date
        :param rider: id
        ___________________
        :return: tuples of tuple
        """
        query = SHIFT_DATA.format(rider, start_date, end_date)
        connection.execute(query)
        shifts = connection.fetchall()
        return shifts
