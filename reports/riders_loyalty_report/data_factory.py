from reports.riders_loyalty_report.queries import RIDER_DATA, POINT_STATS
from settings.base import connection


class DataFactory:
    """
    Class  responsible for providing required data and stats for rider receivable  report
    """
    def __init__(self):
        pass

    @staticmethod
    def get_eligible_rider_report(start_date, end_date):
        """
        get rider data
        ____________
        :param start_date: datetime.date
        :param end_date: datetime.time
        ____________
        :return: tuples of tuple
        """
        query = RIDER_DATA.format(start_date, end_date)
        connection.execute(query)
        eligible_riders = connection.fetchall()
        return eligible_riders

    @staticmethod
    def get_points_stats(rider, start_date, end_date):
        """
        get rider Loyalty Points History
        ______________
        :param rider: id
        :param start_date: datetime.date
        :param end_date: datetime.time
        ______________
        :return: dictionary
        """
        query = POINT_STATS.format(start_date, end_date, rider)
        connection.execute(query)
        point_stats = connection.fetchall()
        return {
            'point_at_beginning': point_stats[0][0] or 0,
            'point_bw_period': point_stats[0][2] or 0,
            'point_at_end': point_stats[0][1] or 0,
            'redeem_points': point_stats[0][3] or 0,
            'penalty_points': point_stats[0][4] or 0
            }
