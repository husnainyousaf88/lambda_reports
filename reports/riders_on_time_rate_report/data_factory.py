from reports.riders_on_time_rate_report.queries import RIDER_ON_TIME_PICKUP_STATS_SQL, ELIGIBLE_RIDERS_SQL, ORDER_STATE_SQL, RIDER_ON_TIME_DELIVERY_STATS_SQL
from settings.base import connection
from datetime import datetime, timedelta


class DataFactory:
    """
    Class  responsible for providing required data and stats for rider receivable  report
    """
    def __init__(self):
        pass

    @staticmethod
    def get_rider_data(start_time, end_time):
        query = ELIGIBLE_RIDERS_SQL.format(start_time, end_time)
        connection.execute(query)
        eligible_riders = connection.fetchall()
        return eligible_riders

    @staticmethod
    def get_rider_order_stats(rider, start_time, end_time):
        """
                Calculate rider order stats

                Parameters
                ----------
                rider : Rider
                start_time : datetime.datetime
                    time from when to consider orders
                end_time : datetime.datetime
                    time till when to consider orders

                Returns
                -------
                dict
                    rider order stats
                """
        order_stats = DataFactory.get_order_state(rider, start_time, end_time)
        total_orders = order_stats['total_orders'] or 0
        total_picked_up_orders = order_stats['total_picked_up_orders'] or 0
        delivered_orders = order_stats['delivered_orders'] or 0
        total_failed_orders = total_picked_up_orders - delivered_orders
        return {
            'total_orders': total_orders,
            'total_picked_up_orders': total_picked_up_orders,
            'total_delivered_orders': delivered_orders,
            'total_failed_orders': total_failed_orders,
            'failed_rate': (round(total_failed_orders * 100 / total_picked_up_orders, 1)
                            if total_picked_up_orders else 0),
        }

    @staticmethod
    def get_order_state(rider, start_time, end_time):
        """
        get total orders of the rider
        ____________________
        :param rider: id
        :param start_time: datetime.time
        :param end_time: datetime.time
        __________________
        :return: dictionary
        """
        query = ORDER_STATE_SQL.format(start_time, end_time, rider)
        connection.execute(query)
        order_state = connection.fetchall()
        return {
            'total_orders': order_state[0][0],
            'total_picked_up_orders': order_state[0][1],
            'delivered_orders': order_state[0][2]
        }

    @staticmethod
    def calculate_on_time_rates(rider, start_time, end_time, total_delivered_orders, total_picked_up_orders):
        """
        Calculate performance summary of top performing rider

        Parameters
        ----------
        rider : Rider
        start_time : datetime.datetime
            time from when to calculate summary
        end_time : datetime.datetime
            time till when to calculate summary
        total_delivered_orders: int
            total orders delivered by the rider
        total_picked_up_orders: int
            total orders picked up by the rider
        Returns
        -------
        dict
            On Time Rates
        """
        total_on_time_deliveries = DataFactory.get_rider_on_time_delivery_stats(rider, start_time, end_time)
        total_on_time_pickups = DataFactory.get_rider_on_time_pickup_stats(rider, start_time, end_time)
        on_time_rate = DataFactory.get_on_time_rate(total_on_time_deliveries, total_on_time_pickups,
                                                    total_delivered_orders, total_picked_up_orders)
        return on_time_rate

    @staticmethod
    def get_rider_on_time_delivery_stats(rider, start_time, end_time):
        """
        get rider delivery stats from order_state
        ________________
        :param rider: id
        :param start_time: date_time_format
        :param end_time: date_time_format
        ______________
        :return: value
        """
        query = RIDER_ON_TIME_DELIVERY_STATS_SQL.format(start_time, end_time, rider)
        connection.execute(query)
        get_rider_on_time = connection.fetchall()[0]
        return get_rider_on_time[0] or 0

    @staticmethod
    def get_rider_on_time_pickup_stats(rider, start_time, end_time):
        """
        get rider pickup stats from order_state
        ________________
        :param rider: id
        :param start_time: date_time_format
        :param end_time: date_time_format
        ______________
        :return: value
        """
        query = RIDER_ON_TIME_PICKUP_STATS_SQL.format(start_time, end_time, rider)
        connection.execute(query)
        get_rider_on_time_pickup = connection.fetchall()[0]
        return get_rider_on_time_pickup[0] or 0

    @staticmethod
    def get_on_time_rate(on_time_deliveries, on_time_pickups, total_delivered_orders, total_picked_up_orders):
        """
        calculate on time rate
        _________________________
        :param on_time_deliveries:  value
        :param on_time_pickups: value
        :param total_delivered_orders: value
        :param total_picked_up_orders: value
        ________________________
        :return: integer value
        """

        return int(round((on_time_deliveries + on_time_pickups) * 100 /
                         ((total_delivered_orders + total_picked_up_orders) or 1), 0))
