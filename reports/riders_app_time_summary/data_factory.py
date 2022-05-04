from reports.riders_app_time_summary.queries import PAUSE_TIME, RESUME_TIME, RIDER_STATS
from settings.base import connection


class DataFactory:
    """
    Class responsible providing all required data for the report
    """

    def __init__(self):
        pass

    @staticmethod
    def get_rider_stats(report_date):
        """
        get rider stats
        ______________
        :param report_date: datetime.date
        ______________
        :return: tuples of tuple
        """
        query = RIDER_STATS.format(report_date)
        connection.execute(query)
        rider_stat = connection.fetchall()
        return rider_stat

    @staticmethod
    def get_resume_time(report_date, rider_id):
        """
        get resume time detail
        __________________
        :param report_date: datetime.date
        :param rider_id: id
        __________________
        :return: tuples of tuple
        """
        query = RESUME_TIME.format(report_date, rider_id)
        connection.execute(query)
        resume_time = connection.fetchall()
        return resume_time

    @staticmethod
    def get_pause_time(report_date, rider_id):
        """
        get pause time
        _______________
        :param report_date: datetime.date
        :param rider_id: id
        _______________
        :return: tuples of tuple
        """
        query = PAUSE_TIME.format(report_date, rider_id)
        connection.execute(query)
        pause_time = connection.fetchall()
        return pause_time
