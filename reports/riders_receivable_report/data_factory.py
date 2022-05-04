from reports.riders_receivable_report.queries import RIDER_EARNING_SQL, DROP_OFF_DISTANCE_SQL ,PICK_UP_DISTANCE_SQL, EQUIPMENT_COST_SQL,RIDER_CASH_SUM_SQL, ELIGIBLE_RIDERS_SQL, SETTLEMENT_SQL, LOGISTICS_CONFIGURATION_SQL
from settings.base import connection
from datetime import datetime, timedelta, timezone


class DataFactory:
    """
    Class  responsible for providing required data and stats for rider receivable  report
    """
    def __init__(self):
        pass

    @staticmethod
    def get_eligible_riders():
        """
        Get Eligible Riders Details
        _________
        :return: tuples of tuple

        """
        query = ELIGIBLE_RIDERS_SQL.format()
        connection.execute(query)
        eligible_riders = connection.fetchall()
        return eligible_riders

    @staticmethod
    def get_last_settlement_query(end_date, rider_id):
        """
        get created at date from rider cash
        ____________________
        :param end_date: date
        :param rider_id: id
        ____________________
        :return: integer
        """
        query = SETTLEMENT_SQL.format(end_date, rider_id)
        connection.execute(query)
        last_settlement = connection.fetchall()
        if last_settlement:
            return last_settlement[0][0]
        return 0

    @staticmethod
    def get_logistics_configuration_instance():
        """
        get single instance from logistics_configuration
        _______________
        :return: string
        """
        query = LOGISTICS_CONFIGURATION_SQL.format()
        connection.execute(query)
        logistic_configuration = connection.fetchall()[0][0] or 0
        return str(logistic_configuration)

    @staticmethod
    def get_rc_sum_query(end_date, rider_id):
        """
        sum rider_cash trnas_types
        __________________
        :param end_date: date
        :param rider_id: id
        ___________________
        :return: dictionary
        """
        query = RIDER_CASH_SUM_SQL.format(end_date, rider_id)
        connection.execute(query)
        rc_sum = connection.fetchall()
        return {
            "trans_type_c": rc_sum[0][0] or 0,
            "trans_type_d": rc_sum[0][1] or 0
        }

    @staticmethod
    def get_equipment_cost(rider_id, start_time, end_time):
        """
        sum rider equipment cost
        ____________________
        :param rider_id: id
        :param start_time: datetime_format
        :param end_time: datetime_format
        ___________________
        :return: integer
        """
        query = EQUIPMENT_COST_SQL.format(start_time, end_time, rider_id)
        connection.execute(query)
        equipment_cost = connection.fetchall()[0][0] or 0
        return equipment_cost

    @staticmethod
    def get_rider_pickup_distances(rider_id, start_time, end_time):
        """
        get sum of pick_up_distance between given date and given rider_id
        _________________
        :param rider_id: id
        :param start_time: datetime_format
        :param end_time: datetime_format
        _________________
        :return: float
        """
        query = PICK_UP_DISTANCE_SQL.format(start_time, end_time, "PB", rider_id)
        connection.execute(query)
        pick_up_distance = connection.fetchall()[0][0] or 0
        return float(pick_up_distance)

    @staticmethod
    def get_rider_drop_off_distances(rider_id, start_time, end_time):
        """
            get total drop_off_distance between given date
            _________________
            :param rider_id: id
            :param start_time: datetime_format
            :param end_time: datetime_format
            _________________
            :return: float
        """
        query = DROP_OFF_DISTANCE_SQL.format(start_time, end_time, "DDP", rider_id)
        connection.execute(query)
        drop_off_distance = connection.fetchall()[0][0] or 0
        return float(drop_off_distance)

    @staticmethod
    def get_rider_earnings(rider_id, start_time, end_time):
        """
        get pick up and drop off amount according to their log type
        __________________
        :param rider_id: id
        :param start_time: datetime_format
        :param end_time: datetime_format
        ___________________
        :return: dictionary
        """
        query = RIDER_EARNING_SQL.format(start_time, end_time, rider_id)
        connection.execute(query)
        earnings_data = connection.fetchall()
        return {
            "pick_up_distance_bonus": earnings_data[0][0] or 0,
            "drop_off_distance_pay": earnings_data[0][1] or 0
        }
