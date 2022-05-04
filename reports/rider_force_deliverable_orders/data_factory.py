from reports.rider_force_deliverable_orders.queries import FORCE_DELIVERABLE_SQL
from settings.base import connection


class DataFactory:
    """
    Class responsible providing all required data for the report
    """

    def __init__(self):
        pass

    @staticmethod
    def get_riders_data(start_date, end_date):
        """
        get resume time detail
        __________________
        :param report_date: datetime.date
        :param rider_id: id
        __________________
        :return: tuples of tuple
        """
        query = FORCE_DELIVERABLE_SQL.format(start_date, end_date)
        connection.execute(query)
        rider_data = connection.fetchall()
        return rider_data
