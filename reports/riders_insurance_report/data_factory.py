from reports.riders_insurance_report.queries import INSURANCE_DATA_SQL, RIDER_INSURANCE_SQL
from settings.base import connection
from datetime import datetime, timedelta


class DataFactory:
    """
    Class  responsible for providing required data and stats for rider receivable  report
    """
    def __init__(self):
        pass

    @staticmethod
    def get_insurance_data(start_time, end_time):
        query = INSURANCE_DATA_SQL.format(start_time, end_time)
        connection.execute(query)
        rider_settlement = connection.fetchall()
        return rider_settlement

    @staticmethod
    def get_rider_insurance(res):
        query = RIDER_INSURANCE_SQL.format(res)
        connection.execute(query)
        rider_insurance = connection.fetchall()
        return rider_insurance