from reports.riders_settlement_request.queries import RIDER_SETTLEMENT_SQL
from settings.base import connection
import pytz
from datetime import datetime, timedelta


class DataFactory:
    """
    Class  responsible for providing requrired data and stats for rider shift report
    """
    def __init__(self):
        pass

    @staticmethod
    def get_settlement_request(start_time, end_time):
        """
        get eligible riders details
        _______________________
        :param start_time: datetime.time
        :param end_time: datetime.time
        ______________________
        :return: tuples of tuple
        """
        query = RIDER_SETTLEMENT_SQL.format(start_time, end_time)
        connection.execute(query)
        rider_settlement = connection.fetchall()
        return rider_settlement

    @staticmethod
    def convert_to_localtime(utctime, fmt='%d/%m/%Y %H:%M:%S %p'):
        if utctime is None:
            return utctime
        utc = utctime.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(pytz.timezone('Asia/Karachi'))
        return localtz.strftime(fmt)
