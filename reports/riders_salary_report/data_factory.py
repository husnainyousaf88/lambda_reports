from reports.riders_salary_report.queries import GET_USER_LOGS,GET_LOGISTICS_INSTANCE,GET_PENALTY_FAILED_ORDERS,GET_INSTANCE_SQL,GET_RIDER_CERTIFICATE_SQL,RIDER_SECURITY_DEPOSIT_SQL,RIDER_SECURITY_SQL,GET_UPDATE_VALUE_SQL, ELIGIBLE_RIDERS_SQL, GET_PAID_FALSE_SQL ,PICK_UP_DISTANCE_SQL, RIDER_DROP_OFF_DISTANCE_SQL, RIDER_EARNINGS_SQL, RIDER_EARNING_BY_CATEGORY_SQL, RIDER_PENALTY_SQL, RIDER_BONUS_SQL, EARNINGS_STATS_SQL,  CITY_CONFIGURATIONS_INSTANCE_SQL, RIDER_ORDER_STATS_SQL, RIDER_NON_PAID_FUEL_EARNINGS_SQL, ORDER_IDS_SQL,RIDER_ORDER_DATES_STATS_SQL, RIDER_ORDER_ACCEPT_STATS_SQL, RIDER_ON_TIME_DELIVERY_STATS_SQL, RIDER_ON_TIME_PICKUP_STATS_SQL, LOYALTY_BONUS_SQL,CERTIFICATE_BONUS_SQL, PREVIOUS_PAID_SQL
from settings.base import connection
from datetime import datetime


RIDER_CATEGORIES = {
    1: "Food",
    2: "3PL General",
    3: "3PL Restaurant",
    4: "3PL Errand",
    5: "MILK",
    6: "CMART"

}


class DataFactory:
    """
    Class  responsible for providing requrired data and stats for salary report
    """
    def __init__(self):
        pass

    @staticmethod
    def get_rider_category(cat_id):
        """
        get the name of rider_categories
        _______________________________
        :param cat_id: value
        _______________________________
        :return: name of RIDER_CATEGORIES
        """
        return RIDER_CATEGORIES[cat_id]

    @staticmethod
    def get_eligible_riders(end_date):
        """
        Get Eligible Riders Details Between Given Date Range
        Parameters
        ----------
        end_date: Date Object
        Returns
        -------
        shifts: tuple of tuples
        """
        query = ELIGIBLE_RIDERS_SQL.format(end_date)
        connection.execute(query)
        eligible_riders = connection.fetchall()
        return eligible_riders

    @staticmethod
    def get_rider_pickup_distance(rider, start_time, end_time):
        """
        get sum of pick_up_distance between given date and given rider_id
        __________
        :param rider:id
        :param start_time:date_time_format
        :param end_time: date_time_format
        :param log_type: PB
        __________
        :return:
                pickup distance value if value is null return zero
        """
        query = PICK_UP_DISTANCE_SQL.format(start_time, end_time, "PB", rider)
        connection.execute(query)
        pick_up_distance = connection.fetchall()[0][0] or 0
        return float(pick_up_distance)

    @staticmethod
    def get_rider_drop_off_distances(rider, start_time, end_time):
        """
        get the sum of drop_off_distance between given date and time and given rider
         ______________
        :param rider:id
        :param start_time:date_time_format
        :param end_time: date_time_format
        :param log_type: DDP
        ______________
        :return:
                sum of drop_off_distance value if value is null return zero
        """
        query = RIDER_DROP_OFF_DISTANCE_SQL.format(start_time, end_time, "DDP", rider)
        connection.execute(query)
        drop_off_distance = connection.fetchall()[0][0] or 0
        return float(drop_off_distance)

    @staticmethod
    def get_rider_earnings(rider, start_time, end_time):
        """
        calculate and return rider's earning amount based category earnings...
        :param rider: id
        :param start_time: date_time_format
        :param end_time: :date_time_format
        :return:
        rider_earning : dictionary
        """
        query = RIDER_EARNINGS_SQL.format(start_time, end_time,  rider)
        connection.execute(query)
        rider_earning = connection.fetchall()[0]
        return {
            "pick_up_distance_bonus": rider_earning[0] or 0,
            "pick_up_pay": rider_earning[1] or 0,
            "drop_off_distance_pay": rider_earning[2] or 0,
            "drop_off_pay": rider_earning[3] or 0,
            "delivery_charges_based_pay": rider_earning[4] or 0,
            "per_order_pay": rider_earning[5] or 0,
            "slab_based_pay": rider_earning[6] or 0,
            "tips": rider_earning[7] or 0,
            "late_night_bonus": rider_earning[12] or 0
        }

    @staticmethod
    def get_rider_earnings_by_category(rider, start_time, end_time):
        """
        calculate and return rider's order's based category earnings...
        ________________
        :param rider: id
        :param start_time: date_time_format
        :param end_time: date_time_format
        ________________
        :return:
        rider_earning_by_category : dictionary (container categorized earning)
        """
        query = RIDER_EARNING_BY_CATEGORY_SQL.format(start_time, end_time, rider)
        connection.execute(query)
        rider_earning_by_category = connection.fetchall()[0]
        return {
            "food_order_pay": rider_earning_by_category[0] or 0,
            "healthcare_order_pay": rider_earning_by_category[1] or 0,
            "errand_pay": rider_earning_by_category[2] or 0,
            "books_order_pay": rider_earning_by_category[3] or 0,
            "beauty_order_pay": rider_earning_by_category[4] or 0,
            "babycare_order_pay": rider_earning_by_category[5] or 0,
            "pantry_order_pay": rider_earning_by_category[6] or 0,
            "pharma_order_pay": rider_earning_by_category[7] or 0,
            "tiffin_order_pay": rider_earning_by_category[8] or 0,
            "xoom_order_pay": rider_earning_by_category[9] or 0
        }

    @staticmethod
    def get_rider_penalty(rider, start_time, end_time):
        """
        get amount and no of off days from rider_penalty between given date and given rider_id
        _______________
        :param rider: id
        :param start_time: date_time_format
        :param end_time: date_time_format
        _______________
        :return:  dictionary
        """
        query = RIDER_PENALTY_SQL.format(start_time, end_time, rider)
        connection.execute(query)
        get_penalty = connection.fetchall()[0]
        return {
            'total_penalty': float(get_penalty[0] or 0),
            'no_show_days': get_penalty[1] or 0}

    @staticmethod
    def get_rider_bonus(rider, start_time, end_time):
        """
        get bonus from rider_referral_bonus_log between given date and rider
        ________________
        :param rider: id
        :param start_time: date_time_format
        :param end_time: date_time_format
        ________________
        :return: value if value is null return zero
        """
        query = RIDER_BONUS_SQL.format(start_time, end_time, rider)
        connection.execute(query)
        get_bonus = connection.fetchall()[0]
        return get_bonus[0] or 0

    @staticmethod
    def can_get_minimum_guarantee(rider, start_time, end_time, total_pay):
        """
        Check if rider qualifies for salary or not
        ___________________
        :param rider: id
        :param start_time:  date_time_format
        :param end_time: date_time_format
        :param total_pay: value
        ___________________
        :return: two parameters
        stats : return the dictionary and
        value of can_get_minimum_guarantee
        """
        shifts_stats = DataFactory.get_earnings_stats(rider, start_time, end_time)
        rider_instance = DataFactory.city_configuration()
        order_stats = DataFactory.get_rider_order_stats(rider, start_time, end_time)
        stats = {'shifts_stats': shifts_stats, 'order_stats': order_stats}
        return (total_pay < shifts_stats['total_pay'] and shifts_stats['hours_percent'] >=
                rider_instance[0][0]), stats

    @staticmethod
    def get_earnings_stats(rider, start_time, end_time):
        """
         get rider earning stats
         ________________
         :param rider: id
         :param start_time: date_time_format
         :param end_time: date_time_format
         _________________
         :return: dictionary
        """
        query = EARNINGS_STATS_SQL.format(rider, start_time, end_time)
        connection.execute(query)
        get_stats = connection.fetchall()[0]
        total_pause_time = get_stats[1] or 0
        total_worked_time = get_stats[0] or 0
        total_problem_time = get_stats[2] or 0
        total_shift_hours = get_stats[3]
        total_active_hours = total_worked_time - total_pause_time - total_problem_time
        hours = float(round(total_active_hours, 2))
        hours_percent = round(total_active_hours * 100 / total_shift_hours, 1) if total_shift_hours else 0
        hours_percent = float(hours_percent if hours_percent <= 100 else 100)  # added to round off to 100
        calculate_total_pay = True
        response = {'hours': hours, 'hours_percent': hours_percent}
        if calculate_total_pay:
            response['total_pay'] = float(get_stats[6] or 0)
            response['over_time_pay'] = float(get_stats[5] or 0)
            response['total_over_time'] = get_stats[4] or 0
        return response

    @staticmethod
    def city_configuration():
        """
        get hourly_pay_min_app_on_time from city_configuration
        ______________
        :return: tuple
        """
        rider_instance = CITY_CONFIGURATIONS_INSTANCE_SQL.format()
        connection.execute(rider_instance)
        rider_instance = connection.fetchall()
        return rider_instance

    @staticmethod
    def get_rider_order_stats(rider, start_time, end_time):
        """
        get rider order stats
        ________________
        :param rider: id
        :param start_time: date_time_format
        :param end_time: date_time_format
        ________________
        :return: dictionary
        """
        query = RIDER_ORDER_STATS_SQL.format(start_time, end_time, rider)
        connection.execute(query)
        get_rider_stats = connection.fetchall()[0]
        total_orders = get_rider_stats[0] or 0
        total_picked_up_orders = get_rider_stats[1] or 0
        delivered_orders = float(get_rider_stats[2] or 0)
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
    def get_cash_in_hand_without_fuel_amounts(rider):
        """
        get data from get_rider_non_paid_fuel_earnings function by given rider
        ______________
        :param rider:id
        _______________
        :return:
        fuel_amount : value
        """
        fuel_amount, order_ids = DataFactory.get_rider_non_paid_fuel_earnings(rider)
        return fuel_amount

    @staticmethod
    def get_rider_non_paid_fuel_earnings(rider):
        """
        get amount from rider_earnings and call the function get_order_ids
        and then append the order_ids in res_order_ids list by given rider
        ________________
        :param rider: id
        ______________________
        :return: two parameters
        1 : value of fuel_amount
        2: list of tuples
        """
        query = RIDER_NON_PAID_FUEL_EARNINGS_SQL.format(rider)
        connection.execute(query)
        get_earning = connection.fetchall()[0]
        fuel_amount = get_earning[0] or 0
        order_ids = DataFactory.get_order_ids(rider)
        res_order_ids = []
        [res_order_ids.append(x) for x in order_ids if x not in res_order_ids]
        return fuel_amount, res_order_ids

    @staticmethod
    def get_order_ids(rider):
        """
        get order_id's
        _________________
        :param rider: id
        _________________
        :return: tuples of tuple
        """
        query = ORDER_IDS_SQL.format(rider)
        connection.execute(query)
        order_id = connection.fetchall()
        return order_id

    @staticmethod
    def get_rider_order_dates_stats(rider_id, weekends):
        """
        Get order date stats of a rider
        ___________________
        :param rider_id: id
        :param weekends: tuple
        ___________________
        :return: dictionary
        """
        query = RIDER_ORDER_DATES_STATS_SQL.format(weekends, rider_id)
        connection.execute(query)
        get_rider_order = connection.fetchall()[0]
        total_orders = get_rider_order[0] or 0
        total_picked_up_orders = get_rider_order[1] or 0
        delivered_orders = get_rider_order[2] or 0
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
    def get_rider_order_accept_stats(rider, start_time, end_time):
        """
        get rider accept stats according to their log_type
        __________________
        :param rider: id
        :param start_time: date_time_format
        :param end_time: date_time_format
        _________________
        :return: dictionary
        """
        query = RIDER_ORDER_ACCEPT_STATS_SQL.format(start_time, end_time, rider)
        connection.execute(query)
        get_rider_order_accept = connection.fetchall()[0]
        total_orders = get_rider_order_accept[0] or 0
        accepted_orders = get_rider_order_accept[1] or 0
        rejected_orders = get_rider_order_accept[2] or 0
        return {
            'total_orders': total_orders,
            'total_accepted_orders': accepted_orders,
            'total_rejected_orders': rejected_orders,
            'acceptance_rate': round(accepted_orders * 100 / total_orders, 1) if total_orders else 0}

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
    def get_calculate_on_time_rates(rider, start_time, end_time, total_delivered_orders, total_picked_up_orders):
        """
           get  on time rate from total deliveries and on time pickup
            __________
            :param rider: id
            :param start_time: date_time_format
            :param end_time: date_time_format
            :param total_delivered_orders: value
            :param total_picked_up_orders: value
            __________
            :return: dictionary
        """
        total_on_time_deliveries = DataFactory.get_rider_on_time_delivery_stats(rider, start_time, end_time)
        total_on_time_pickups = DataFactory.get_rider_on_time_pickup_stats(rider, start_time, end_time)
        on_time_rate = DataFactory.get_on_time_rate(total_on_time_deliveries, total_on_time_pickups,
                                                    total_delivered_orders, total_picked_up_orders)
        return on_time_rate

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

    @staticmethod
    def get_loyalty_bonus(rider, start_time, end_time):
        """
         calculate loyalty bonus
        ________________
        :param rider: id
        :param start_time: date_time_format
        :param end_time: date_time_format
        ________________
        :return:
        get_rider_certificate : float value
        """
        query = LOYALTY_BONUS_SQL.format(rider, start_time, end_time)
        connection.execute(query)
        get_rider_certificate = connection.fetchall()[0]
        return float(get_rider_certificate[0] or 0)

    @staticmethod
    def get_certificate_bonus(rider, start_date, end_date):
        """
        return payment from rider_certificate
        _______________
        :param rider: id
        :param start_date: date_time_format
        :param end_date: date_time_format
        _______________
        :return: integer
        """

        already_paid = False
        payment = 0

        stats = DataFactory.get_rider_certificate_earnings(start_date, end_date, rider)

        if stats:
            previous_paid_stats = DataFactory.get_previous_paid_stats(start_date, end_date, rider)
            if len(previous_paid_stats) > 0:
                payment = previous_paid_stats[0][2]
                already_paid = True

            stats = DataFactory.get_paid_false(start_date, end_date, rider)
            if len(stats) > 0:
                for item in stats:
                    certificate_instance = item[0]
                    time_diff = int((datetime.now() - item[4]).total_seconds() / 3600)
                    if time_diff < item[3]:
                        stats = list(stats[0][0])
                        for remove_item in stats:
                            if remove_item == item[0]:
                                stats.remove(remove_item)
                    if not already_paid and stats:
                        payment = stats[0][2]
                date = datetime.now()
                stats = DataFactory.get_update_value(start_date, end_date, rider, date)
            return payment

        else:
            return float(0)

    @staticmethod
    def rider_security_deduction(rider, start_date, end_date, salary):
        """
             return rider final salary after deducting security deposits

             parameters
             ----------
             rider : Rider
             start_date : date
             end_date : date
             salary : int

             Returns
             -------
             Tuple( deducted salary, security_deduction_amount)
                """
        oct_month = datetime(2021, 10, 1).date()
        rider_security_deposit_log = DataFactory.get_rider_security(rider)
        if rider_security_deposit_log:
            security_deposit = DataFactory.get_rider_security_amount(rider_security_deposit_log, end_date)
            salary -= security_deposit
            DataFactory.get_rider_security_deposit(rider, type='s', amount=security_deposit)
            return salary, security_deposit
        elif end_date < oct_month:
            start_date_ = end_date.replace(month=end_date.month - 1, day=15)
            cert_issue_date = DataFactory.get_rider_certificate(rider)
            if cert_issue_date and cert_issue_date.date() >= start_date_:
                config = DataFactory.get_logistics_config()
                security_deposit = config
                salary -= security_deposit
                DataFactory.get_rider_security_deposit(rider, type='s', amount=security_deposit)
                return salary, security_deposit
            else:
                return salary, 0
        else:
            return salary, 0

    @staticmethod
    def get_rider_security(rider):
        """
        get security_deposit from rider_security_deposit_log
        _______________
        :param rider: id
        _______________
        :return: tuples of tuple
        """
        query = RIDER_SECURITY_SQL.format(rider)
        connection.execute(query)
        security_value = connection.fetchall()
        return security_value

    @staticmethod
    def get_logistics_config():
        """
        get single instance from logistics_configuration
        _____________
        :return: integer
        """
        query = GET_INSTANCE_SQL.format()
        connection.execute(query)
        instance_value = connection.fetchall()
        return instance_value[0][0]

    @staticmethod
    def get_rider_certificate(rider):
        """
        get certificate_issue_date from rider_certificate
        _______________
        :param rider: id
        _______________
        :return: integer
        """
        query = GET_RIDER_CERTIFICATE_SQL.format(rider)
        connection.execute(query)
        get_certificate = connection.fetchall()
        return get_certificate[0][0]

    @staticmethod
    def get_rider_security_deposit(rider, type, amount):
        """
        insert value in rider_security_deposit
        _______________
        :param rider: id
        :param type: string
        :param amount: int
        _______________
        :return: tuples of tuple
        """
        query = RIDER_SECURITY_DEPOSIT_SQL.format(rider, type, amount)
        connection.execute(query)
        security_deposit = connection.fetchall()
        return security_deposit

    @staticmethod
    def get_rider_security_amount(instance, end_date):
        """
         get security deposit value
        ___________________
        :param instance:  tuples of tuple
        :param end_date: date_time format
        ____________________
        :return: integer
        """
        if instance[0][1] == end_date.month and instance[0][2] == end_date.year:
            return instance[0][0]
        return 0

    @staticmethod
    def get_rider_certificate_earnings(start_date, end_date, rider):
        """
        get amount to pay from rider_certificate if is_active is true
        ____________________
        :param start_date: date
        :param end_date: date
        :param rider: id
        ________________
        :return: tuples of tuple
        """
        query = CERTIFICATE_BONUS_SQL.format(start_date, end_date, rider)
        connection.execute(query)
        get_rider_certificate = connection.fetchall()
        return get_rider_certificate

    @staticmethod
    def get_previous_paid_stats(start_date, end_date, rider):
        """
        get amount to pay from rider_certificate if is_active is true and is_paid is true
        ______________
        :param start_date: date
        :param end_date: date
        :param rider: id
        ______________
        :return: tuples of tuple
        """
        query = PREVIOUS_PAID_SQL.format(start_date, end_date, rider)
        connection.execute(query)
        get_previous_paid = connection.fetchall()
        return get_previous_paid

    @staticmethod
    def get_paid_false(start_date, end_date, rider):
        """
        get amount to pay from rider_certificate if is_active is false
        ______________________
        :param start_date: date
        :param end_date: date
        :param rider: id
        ____________________
        :return: tuples of tuple
        """
        query = GET_PAID_FALSE_SQL.format(start_date, end_date, rider)
        connection.execute(query)
        paid_false = connection.fetchall()
        return paid_false

    @staticmethod
    def get_update_value(start_date, end_date, rider, date):
        """
        update the rider_certificate
        __________________
        :param start_date: date
        :param end_date: date
        :param rider: id
        :param date: user_is_assigned at
        __________________
        :return: tuples of tuple
        """
        query = GET_UPDATE_VALUE_SQL.format(start_date, end_date, rider, date)
        connection.execute(query)
        update_value = connection.fetchall()
        return update_value

    @staticmethod
    def get_rider_penalty_failed_orders(rider_id, start_time, end_time):
        """
        get total amount from order_state
        _________________
        :param rider_id: id
        :param start_time: date_time format
        :param end_time: date_time format
        __________________
        :return: integer
        """
        query = GET_PENALTY_FAILED_ORDERS.format(start_time, end_time, rider_id)
        connection.execute(query)
        failed_orders = connection.fetchall()
        total_amount = failed_orders[0][0] or 0
        return total_amount

    @staticmethod
    def get_insurance_pay(rider, start_date, end_date, date_join):
        """
            Get insurance pay for given date range
            Parameters
            ----------
            rider : Queryset
                Rider instance
            start_date : date
            end_date : date

            Returns
            -------
            insurance_amount
                amount will deduct from rider salary
            """
        try:
            insurance_pay_per_month = DataFactory.logistic_instance()
            days = 0
            is_activated = False
            user_status_logs = list(DataFactory.get_user_status_logs(rider))
            user_status_logs.insert(0, ("Active", date_join.date()))
            if len(user_status_logs) == 0:
                return days
            previous_logs = [item for item in user_status_logs if item[1] < start_date]
            current_logs = [item for item in user_status_logs if start_date <= item[1] <= end_date]
            if len(previous_logs) >= 1:
                if previous_logs[-1][0] == "Active":
                    is_activated = True
            days_counter = start_date if is_activated else None
            for item in current_logs:
                if item[0] == "Active":
                    days_counter = item[1]
                    continue
                if item[0] == "Inactive":

                    days += DataFactory.get_days_between_date(days_counter, item[1])
                    days_counter = None
            if days_counter:

                days += DataFactory.get_days_between_date(days_counter, end_date)
            insurance_amount = min(int(days * (insurance_pay_per_month / 30)), insurance_pay_per_month)
            return -insurance_amount

        except:
            return 0

    @staticmethod
    def get_days_between_date(d1, d2):
        """
        get days from dates
        :param d1: date
        :param d2: date
        :return: days
        """
        return (d2 - d1).days

    @staticmethod
    def logistic_instance():
        """
        get insurance_pay_per_month from logistics_configuration
        :return: integer
        """
        query = GET_LOGISTICS_INSTANCE.format()
        connection.execute(query)
        logistics_ins = connection.fetchall()
        return logistics_ins[0][0]

    @staticmethod
    def get_user_status_logs(rider):
        """
        get action type and date from user_status_change_log
        _______________
        :param rider: id
        _______________
        :return: tuples of tuple
        """
        query = GET_USER_LOGS.format(rider)
        connection.execute(query)
        status_logs = connection.fetchall()
        return status_logs
