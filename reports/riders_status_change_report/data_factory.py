from reports.riders_status_change_report.queries import LOGS_SQL
from settings.base import connection
from datetime import datetime, timedelta, timezone


class DataFactory:
    """
    Class  responsible for providing required data and stats for rider enable disable report
    """
    def __init__(self):
        pass

    @staticmethod
    def logs_query(start_date, end_date):
        """
        get agent and rider data
        __________________
        :param start_date: datetime.date
        :param end_date: datetime.date
        _________________
        :return: tuples of tuple
        """
        query = LOGS_SQL.format(start_date, end_date)
        connection.execute(query)
        logs_data = connection.fetchall()
        return logs_data
