from reports.riders_detail_report.queries import RIDER_DETAIL
from settings.base import connection


class DataFactory:
    """
    Class responsible providing all required data for the report
    """

    def __init__(self):
        pass

    @staticmethod
    def get_riders_all_data(wallet_type):
        """
        get riders detail according to there wallet type
        ______________________
        :param wallet_type: wallet id
        ______________________
        :return: tuples of tuple
        """
        query = RIDER_DETAIL.format(wallet_type)
        connection.execute(query)
        detail = connection.fetchall()
        return detail
