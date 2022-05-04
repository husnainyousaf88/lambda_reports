from reports.riders_covid_19_sops.queries import RIDER_DETAIL
from settings.base import connection


class DataFactory:
    """
    Class responsible providing all required data for the report
    """

    def __init__(self):
        pass

    @staticmethod
    def get_riders_detail(start_date, end_date):
        """
        COVID-19 sops report
        __________________
        :param start_date: datetime.date
        :param end_date: datetime.date
        ___________________
        :return: tuples of tuple
        """
        query = RIDER_DETAIL.format(start_date, end_date)
        connection.execute(query)
        detail = connection.fetchall()
        return detail
