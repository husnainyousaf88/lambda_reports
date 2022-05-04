from reports.riders_cash_collection.queries import (RIDERS_EARNING_SQL, DELIVERED_DISTANCE_SQL,PICK_UP_DISTANCE_SQL,
                                                    RIDER_FUEL_EARNING_SQL, RIDER_CASH_IDS_SQL,
                                                    JAZZ_CASH_COLLECTION_SQL, RIDER_CASH_SQL, RIDER_CASH_ID_SQL)
from settings.base import connection
from datetime import datetime, timedelta


class DataFactory:
    """
    Class responsible providing all required data for the report
    """

    def __init__(self):
        pass

    @staticmethod
    def rider_cash_collection_log(start_date, end_date):
        """
        get all the rider whose transaction is made between given date
        __________________
        :param start_date: datetime date
        :param end_date: datetime date
        __________________
        :return: tuples of tuple
        """
        query = JAZZ_CASH_COLLECTION_SQL.format(start_date, end_date)
        connection.execute(query)
        jc_log = connection.fetchall()
        return jc_log

    @staticmethod
    def get_riders_cash(rider_id, rider_cash_id):
        """
        get id from rider cash
        ________________
        :param rider_id: id
        :param rider_cash_id: id
        ________________
        :return: integer
        """
        query = RIDER_CASH_SQL.format(rider_cash_id, rider_id)
        connection.execute(query)
        rider_cash = connection.fetchall()
        if rider_cash:
            return rider_cash[0][0]
        return 0

    @staticmethod
    def get_rider_cash_ids(rider_id, rider_cash_id, second_last_jc_log):
        """
        get id from rider cash
        ______________
        :param rider_id: id
        :param rider_cash_id: id
        :param second_last_jc_log: id
        ______________
        :return: integer
        """
        query = RIDER_CASH_ID_SQL.format(second_last_jc_log, rider_cash_id, rider_id)
        connection.execute(query)
        rider_cash = connection.fetchall()
        return rider_cash[0][0] or 0

    @staticmethod
    def get_rider_cash_id(rider_id, rider_cash_id):
        """
        get id from rider cash
        ___________________
        :param rider_id: id
        :param rider_cash_id: id
        __________________
        :return: integer
        """
        query = RIDER_CASH_IDS_SQL.format(rider_cash_id, rider_id)
        connection.execute(query)
        rider_cash = connection.fetchall()
        return rider_cash[0][0] or 0

    @staticmethod
    def get_rider_order_id(rider_id, rider_cash_id):
        """
        get rider order_id's
        ________________
        :param rider_id: id
        :param rider_cash_id: id
        ________________
        :return: tuples of tuple
        """
        query = RIDER_FUEL_EARNING_SQL.format(rider_cash_id, rider_id)
        connection.execute(query)
        rider_fuel = connection.fetchall()
        return rider_fuel

    @staticmethod
    def get_rider_pickup_delivery_stats(order_ids, rider_id):
        """
        get rider pickup and delivery stats
        __________________
        :param order_ids: id
        :param rider_id: id
        _________________
        :return: float
        """
        if len(order_ids) >= 1:
            pickup_distance = DataFactory.pick_distance_query(order_ids, rider_id)
            delivered_distance = DataFactory.delivered_distance_query(order_ids, rider_id)
            return float(pickup_distance), float(delivered_distance)
        else:
            pickup_distance= 0
            delivered_distance= 0
            return float(pickup_distance), float(delivered_distance)

    @staticmethod
    def pick_distance_query(order_ids, rider_id):
        """
        get total pickup distance
        ________________
        :param order_ids: id
        :param rider_id: id
        ________________
        :return: integer
        """
        query = PICK_UP_DISTANCE_SQL.format(rider_id, order_ids)
        connection.execute(query)
        pickup_distance = connection.fetchall()[0][0] or 0
        return pickup_distance

    @staticmethod
    def delivered_distance_query(order_ids, rider_id):
        """
        get total delivered distance
        ___________________
        :param order_ids: id
        :param rider_id: id
        ___________________
        :return: integer
        """
        query = DELIVERED_DISTANCE_SQL.format(rider_id, order_ids)
        connection.execute(query)
        delivered_distance = connection.fetchall()[0][0] or 0
        return delivered_distance

    @staticmethod
    def get_riders_earning(order_ids, rider_id):
        """
        get pickup and drop off amount according to their log type
        _________________
        :param order_ids:
        :param rider_id:
        _________________
        :return: dictionary
        """
        if len(order_ids) >= 1:
            query = RIDERS_EARNING_SQL.format(rider_id, order_ids)
            connection.execute(query)
            earning_data = connection.fetchall()
            return {
                'pick_up_distance_bonus': earning_data[0][0] or 0,
                'drop_off_distance_pay': earning_data[0][1] or 0
            }
        else:
            return {
                'pick_up_distance_bonus': 0,
                'drop_off_distance_pay': 0
            }
