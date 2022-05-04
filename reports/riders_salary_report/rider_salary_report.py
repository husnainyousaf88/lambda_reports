from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_salary_report.data_factory import DataFactory
from datetime import timedelta
from reports.date_time import DateTime
########################################
#  CSV HEADERS
########################################

NIC = 'CNIC'
CITY = 'City'
RIDER_CATEGORY = "Rider Category"
RIDER_TYPE = "Rider Type"
TOTAL_PICKED_UP_ORDERS = 'Total Orders(Failed + Delivered)'
WEEKEND_ORDERS = 'Weekend Total Orders'
HOURS_WORKED = 'Sum of Hours worked(Worked hours - Pause time)'
UTR = 'UTR'
PICKUP_PAY = 'Pickup PKR (PP)'
DROP_OFF_DISTANCE_PAY = 'Total Drop-off Pay PKR (DDP)'
DROP_OFF_DISTANCE = "Drop-off Distance KM"
PICKUP_BONUS = 'Total Pickup bonus (PKR) (PB)'
PICKUP_DISTANCE = "Pickup Distance KM"
DROP_OFF_PAY = 'Total Drop-off pay (DP)'
NO_SHOW_DAYS = 'No show days (only the days when at least one shift was scheduled)'
PENALTY = 'Penalty'
TOTAL_WITHOUT_GUARANTEE = 'Total without guarantee'
PER_HOUR_INCOME = 'Per hour income'
GUARANTEED_PAY_PER_HOUR = 'Per hour income on the basis of weighted average of hours'
ACCEPTANCE_RATE = 'Acceptance %'
FAILED_ORDERS = 'Failed orders'
UNACCEPTED_ORDERS = 'UnAccepted orders'
FAILED_RATE = 'Failed Order Percentage'
APP_ON_RATE = 'App on-time % (cumulative)'
GUARANTEE_QUALIFIES = 'Guarantee Qualifies'
GUARANTEE_RATE = 'Guarantee rate'
FOOD_ORDER_PAY = 'Food Order Pay'
HEALTH_CARE_ORDER_PAY = 'HealthCare Order Pay'
ERRAND_ORDER_PAY = "Errand Order Pay"
BOOKS_ORDER_PAY = 'Books Order Pay'
BEAUTY_ORDER_PAY = 'Beauty Order Pay'
BABY_CARE_ORDER_PAY = 'BabyCare Order Pay'
PANTRY_ORDER_PAY = 'Pantry Order Pay'
PHARMA_ORDER_PAY = 'Pharma Order Pay'
TIFFIN_ORDER_PAY = 'Tiffin Order Pay'
XOOM_ORDER_PAY = 'Xoom Order Pay'
TOTAL_PAY_WITH_GUARANTEE = 'Total pay with guarantee'
SIGN_UP_BONUS = 'Sign Up Bonus'
LAST_SALARY_DIFFERENCE = 'Last Salary Difference'
LOYALTY_BONUS_REDEEMED = 'Loyalty bonus redeemed'
OVER_TIME_PAY = 'Over Time Pay'
FINAL_PAYOUT = 'Final Payout'
FUEL_ALLOWANCE = "Fuel Allowance"
ON_TIME_RATE = 'One Time Rate'
TOTAL_ON_TIME_DELIVERIES = 'Number of on time drop offs'
TOTAL_ON_TIME_PICK_UPS = 'Number of on time pickups'
REFERRAL_BONUS = 'Referral Bonus'
CERTIFICATE_BONUS = 'Certificate Bonus'
SECURITY_DEPOSITS_DEDUCTION = "Security Deposits Deduction"
RIDER_WALLET = "Rider Wallet"
JOB_MODEL_FIXED = 2
JOB_TYPE_FULL_TIME = 1
PER_ORDER_PAY = 'Per Order Compensation'
DELIVERY_CHARGES_BASED_PAY_PAY = 'Delivery Charges Percentage Compensation'
SLAB_BASED_PAY = 'Distance Slab Per Order Compensation'
LATE_NIGHT_BONUS = 'Late Night Bonus Pay'
INSURANCE_AMOUNT = "Insurance Deduction"
FAILED_ORDER_AMOUNT = 'Failed Order Amount(Due to Rider Reason)'


def get_rider_salary(start_date, end_date, email, wallet_type=None):
    """
    Create and Send Email Rider Salary Report Report
    Parameters
    ----------
    wallet_type
    start_date: Date Object
    end_date: Date Object
    email: str( user_email)
    Returns
    -------
        None
    """
    riders_data = []

    data = DateTime.get_dates(start_date, end_date)
    start_time, end_time = data['start_time'], data['end_time']
    start_date, end_date = data['start_date'], data['end_date']

    get_weekends = []
    for days in range((end_time - start_time).days + 1):
        date = start_date + timedelta(days=days)
        if 5 <= date.weekday() <= 6:
            get_weekends.append(str(date))
    weekends = tuple(get_weekends)

    riders = DataFactory.get_eligible_riders(end_time)
    for rider in riders:
        rider_id = rider[0]  # get rider_id
        rider_job_model = rider[1]  # get rider_job_model
        rider_job_type = rider[2]  # get rider_job_type
        rider_nic = rider[3]  # get rider_nic
        city_name = rider[4]  # get city_name
        rider_category = rider[5]  # get rider_category
        cash_in_hand = rider[6]  # get rider cash_in_hand
        user_id = rider[7]  # get user_id
        date_join = rider[8]  # get user_date_joined

        insurance_pay = DataFactory.get_insurance_pay(user_id, start_date, end_date, date_join)
        pickup_distance = DataFactory.get_rider_pickup_distance(rider_id, start_time, end_time)
        delivered_distance = DataFactory.get_rider_drop_off_distances(rider_id, start_time, end_time)

        rider_earning = DataFactory.get_rider_earnings(rider_id, start_time, end_time)
        pick_up_distance_bonus = rider_earning["pick_up_distance_bonus"]
        pick_up_pay = rider_earning["pick_up_pay"]
        drop_off_distance_pay = rider_earning["drop_off_distance_pay"]
        drop_off_pay = rider_earning["drop_off_pay"]
        delivery_charges_based_pay = rider_earning["delivery_charges_based_pay"]
        per_order_pay = rider_earning["per_order_pay"]
        slab_based_pay = rider_earning["slab_based_pay"]
        tips = rider_earning["tips"]
        late_night_bonus = rider_earning["late_night_bonus"]

        rider_earning_category = DataFactory.get_rider_earnings_by_category(rider_id, start_time, end_time)
        food_order_pay = rider_earning_category["food_order_pay"]
        healthcare_order_pay = rider_earning_category["healthcare_order_pay"]
        errand_pay = rider_earning_category["errand_pay"]
        books_order_pay = rider_earning_category["books_order_pay"]
        beauty_order_pay = rider_earning_category["beauty_order_pay"]
        babycare_order_pay = rider_earning_category["babycare_order_pay"]
        pantry_order_pay = rider_earning_category["pantry_order_pay"]
        pharma_order_pay = rider_earning_category["pharma_order_pay"]
        tiffin_order_pay = rider_earning_category["tiffin_order_pay"]
        xoom_order_pay = rider_earning_category["xoom_order_pay"]

        failed_orders_amount = DataFactory.get_rider_penalty_failed_orders(rider_id, start_time, end_time)
        certificate_bonus = DataFactory.get_certificate_bonus(rider_id, start_date, end_date)
        penalty_stats = DataFactory.get_rider_penalty(rider_id, start_date, end_date)
        total_penalty, no_show_days = penalty_stats['total_penalty'], penalty_stats['no_show_days']
        referral_bonus = DataFactory.get_rider_bonus(rider_id, start_time, end_time)
        total_pay = max(pick_up_distance_bonus + pick_up_pay + drop_off_distance_pay + drop_off_pay +
                        delivery_charges_based_pay + per_order_pay + slab_based_pay + tips + late_night_bonus -
                        total_penalty, 0)

        can_get_minimum_guarantees, stats = DataFactory.can_get_minimum_guarantee(rider_id, start_time, end_time,
                                                                                  total_pay)
        shifts_stats = stats["shifts_stats"]
        hours = shifts_stats['hours']
        app_on_rate = shifts_stats['hours_percent']
        guaranteed_pay = shifts_stats['total_pay']
        over_time_pay = shifts_stats['over_time_pay']
        total_picked_up_orders = orders_per_hour = acceptance_rate = per_hour_income = guaranteed_pay_per_hour = \
            total_failed_orders = failed_rate = guarantee_rate = weekend_orders = on_time_rate = \
            total_on_time_deliveries = total_on_time_pickups = total_unaccepted_orders = 0
        guarantee_qualifies = 'No'
        total_pay_with_guarantee = total_pay
        cash = DataFactory.get_cash_in_hand_without_fuel_amounts(rider_id)

        cash_in_hand_without_fuel_amount = cash_in_hand - cash
        category = rider_category
        if hours:
            order_stats = stats['order_stats']
            total_picked_up_orders = order_stats['total_picked_up_orders']
            total_delivered_orders = order_stats['total_delivered_orders']
            total_failed_orders = order_stats['total_failed_orders']
            failed_rate = order_stats['failed_rate']
            orders_per_hour = round(total_delivered_orders / hours, 1)
            per_hour_income = round(float(total_pay) / hours, 1)
            guaranteed_pay_per_hour = round(guaranteed_pay / hours, 2)
            weekend_orders_stats = DataFactory.get_rider_order_dates_stats(rider_id, weekends)
            weekend_orders = weekend_orders_stats['total_picked_up_orders']
            order_accept_stats = DataFactory.get_rider_order_accept_stats(rider_id, start_time, end_time)
            acceptance_rate = order_accept_stats['acceptance_rate']
            total_unaccepted_orders = order_accept_stats['total_rejected_orders']
            total_on_time_deliveries = DataFactory.get_rider_on_time_delivery_stats(rider_id, start_time, end_time)
            total_on_time_pickups = DataFactory.get_rider_on_time_pickup_stats(rider_id, start_time, end_time)

            if can_get_minimum_guarantees:
                guarantee_qualifies = 'Yes'
                guarantee_rate = float(guaranteed_pay_per_hour)

                total_pay_with_guarantee = float(guaranteed_pay) - total_penalty
            on_time_rate = DataFactory.get_calculate_on_time_rates(rider_id, start_time, end_time,
                                                                   total_delivered_orders, total_picked_up_orders)

        start_dates = start_time - timedelta(days=14)
        end_dates = end_time - timedelta(days=14)
        loyalty_bonus = DataFactory.get_loyalty_bonus(rider_id, start_dates, end_dates)
        final_payout = max((total_pay_with_guarantee + over_time_pay),
                           0) + loyalty_bonus + float(referral_bonus) + float(certificate_bonus)

        final_payout, security_deposit_deduction = DataFactory.rider_security_deduction(rider_id, start_date, end_date,
                                                                                        final_payout)
        fuel_allowance = pick_up_distance_bonus + drop_off_distance_pay
        final_payout -= fuel_allowance
        final_payout += insurance_pay
        final_payout -= failed_orders_amount
        rider_type = "Freelance"
        if rider_job_model == JOB_MODEL_FIXED:
            if rider_job_type == JOB_TYPE_FULL_TIME:
                rider_type = "Full-Time"
            else:
                rider_type = "Part-Time"
            riders_data.append({
                NIC: rider_nic, CITY: city_name, RIDER_CATEGORY: DataFactory.get_rider_category(category),
                RIDER_TYPE: rider_type,
                TOTAL_PICKED_UP_ORDERS: total_picked_up_orders,
                WEEKEND_ORDERS: weekend_orders, HOURS_WORKED: hours, UTR: orders_per_hour, PICKUP_PAY: pick_up_pay,
                DROP_OFF_DISTANCE_PAY: drop_off_distance_pay, DROP_OFF_DISTANCE: delivered_distance,
                PICKUP_BONUS: pick_up_distance_bonus, PICKUP_DISTANCE: pickup_distance,
                DROP_OFF_PAY: drop_off_pay, DELIVERY_CHARGES_BASED_PAY_PAY: delivery_charges_based_pay,
                PER_ORDER_PAY: per_order_pay, SLAB_BASED_PAY: slab_based_pay, LATE_NIGHT_BONUS: late_night_bonus,
                NO_SHOW_DAYS: no_show_days, PENALTY: total_penalty, TOTAL_WITHOUT_GUARANTEE: total_pay,
                PER_HOUR_INCOME: per_hour_income,
                GUARANTEED_PAY_PER_HOUR: guaranteed_pay_per_hour, ACCEPTANCE_RATE: acceptance_rate,
                ON_TIME_RATE: on_time_rate, TOTAL_ON_TIME_PICK_UPS: total_on_time_pickups,
                TOTAL_ON_TIME_DELIVERIES: total_on_time_deliveries, FAILED_ORDERS: total_failed_orders,
                FAILED_ORDER_AMOUNT: -failed_orders_amount,
                UNACCEPTED_ORDERS: total_unaccepted_orders, FAILED_RATE: failed_rate,
                APP_ON_RATE: app_on_rate, GUARANTEE_QUALIFIES: guarantee_qualifies, GUARANTEE_RATE: guarantee_rate,
                FOOD_ORDER_PAY: food_order_pay, HEALTH_CARE_ORDER_PAY: healthcare_order_pay,
                ERRAND_ORDER_PAY: errand_pay,
                BOOKS_ORDER_PAY: books_order_pay, BEAUTY_ORDER_PAY: beauty_order_pay,
                BABY_CARE_ORDER_PAY: babycare_order_pay,
                PANTRY_ORDER_PAY: pantry_order_pay, PHARMA_ORDER_PAY: pharma_order_pay,
                TIFFIN_ORDER_PAY: pharma_order_pay,
                TIFFIN_ORDER_PAY: tiffin_order_pay, XOOM_ORDER_PAY: xoom_order_pay,
                TOTAL_PAY_WITH_GUARANTEE: total_pay_with_guarantee, SIGN_UP_BONUS: '-', LAST_SALARY_DIFFERENCE: '-',
                LOYALTY_BONUS_REDEEMED: loyalty_bonus, REFERRAL_BONUS: referral_bonus, INSURANCE_AMOUNT: insurance_pay,
                CERTIFICATE_BONUS: certificate_bonus,
                SECURITY_DEPOSITS_DEDUCTION: -security_deposit_deduction, FUEL_ALLOWANCE: fuel_allowance,
                OVER_TIME_PAY: over_time_pay, RIDER_WALLET: cash_in_hand_without_fuel_amount,
                FINAL_PAYOUT: final_payout})
    cumulative_stats = {
        NIC: len(riders_data), CITY: '', RIDER_CATEGORY: '', RIDER_TYPE: '',
        TOTAL_PICKED_UP_ORDERS: sum(rider_data[TOTAL_PICKED_UP_ORDERS] for rider_data in riders_data),
        WEEKEND_ORDERS: sum(rider_data[WEEKEND_ORDERS] for rider_data in riders_data),
        HOURS_WORKED: sum(rider_data[HOURS_WORKED] for rider_data in riders_data),
        PICKUP_PAY: sum(rider_data[PICKUP_PAY] for rider_data in riders_data),
        DROP_OFF_DISTANCE_PAY: sum(rider_data[DROP_OFF_DISTANCE_PAY] for rider_data in riders_data),
        DROP_OFF_DISTANCE: sum(rider_data[DROP_OFF_DISTANCE] for rider_data in riders_data),
        PICKUP_BONUS: sum(rider_data[PICKUP_BONUS] for rider_data in riders_data),
        PICKUP_DISTANCE: sum(rider_data[PICKUP_DISTANCE] for rider_data in riders_data),
        DROP_OFF_PAY: sum(rider_data[DROP_OFF_PAY] for rider_data in riders_data),
        DELIVERY_CHARGES_BASED_PAY_PAY: sum(rider_data[DELIVERY_CHARGES_BASED_PAY_PAY] for rider_data in riders_data),
        PER_ORDER_PAY: sum(rider_data[PER_ORDER_PAY] for rider_data in riders_data),
        SLAB_BASED_PAY: sum(rider_data[SLAB_BASED_PAY] for rider_data in riders_data),
        LATE_NIGHT_BONUS: sum(rider_data[LATE_NIGHT_BONUS] for rider_data in riders_data),
        NO_SHOW_DAYS: sum(rider_data[NO_SHOW_DAYS] for rider_data in riders_data),
        PENALTY: sum(rider_data[PENALTY] for rider_data in riders_data),
        TOTAL_WITHOUT_GUARANTEE: sum(rider_data[TOTAL_WITHOUT_GUARANTEE] for rider_data in riders_data),
        PER_HOUR_INCOME: sum(rider_data[PER_HOUR_INCOME] for rider_data in riders_data),
        GUARANTEED_PAY_PER_HOUR: sum(rider_data[GUARANTEED_PAY_PER_HOUR] for rider_data in riders_data),
        ACCEPTANCE_RATE: sum(rider_data[ACCEPTANCE_RATE] for rider_data in riders_data),
        ON_TIME_RATE: sum(rider_data[ON_TIME_RATE] for rider_data in riders_data),
        TOTAL_ON_TIME_PICK_UPS: sum(rider_data[TOTAL_ON_TIME_PICK_UPS] for rider_data in riders_data),
        TOTAL_ON_TIME_DELIVERIES: sum(rider_data[TOTAL_ON_TIME_DELIVERIES] for rider_data in riders_data),
        FAILED_ORDERS: sum(rider_data[FAILED_ORDERS] for rider_data in riders_data),
        FAILED_ORDER_AMOUNT: sum(rider_data[FAILED_ORDER_AMOUNT] for rider_data in riders_data),
        UNACCEPTED_ORDERS: sum(rider_data[UNACCEPTED_ORDERS] for rider_data in riders_data),
        FAILED_RATE: sum(rider_data[FAILED_RATE] for rider_data in riders_data), GUARANTEE_QUALIFIES: '-',
        GUARANTEE_RATE: sum(rider_data[GUARANTEE_RATE] for rider_data in riders_data),
        FOOD_ORDER_PAY: sum(rider_data[FOOD_ORDER_PAY] for rider_data in riders_data),
        HEALTH_CARE_ORDER_PAY: sum(rider_data[HEALTH_CARE_ORDER_PAY] for rider_data in riders_data),
        ERRAND_ORDER_PAY: sum(rider_data[ERRAND_ORDER_PAY] for rider_data in riders_data),
        BOOKS_ORDER_PAY: sum(rider_data[BOOKS_ORDER_PAY] for rider_data in riders_data),
        BEAUTY_ORDER_PAY: sum(rider_data[BEAUTY_ORDER_PAY] for rider_data in riders_data),
        BABY_CARE_ORDER_PAY: sum(rider_data[BABY_CARE_ORDER_PAY] for rider_data in riders_data),
        PANTRY_ORDER_PAY: sum(rider_data[PANTRY_ORDER_PAY] for rider_data in riders_data),
        PHARMA_ORDER_PAY: sum(rider_data[PHARMA_ORDER_PAY] for rider_data in riders_data),
        TIFFIN_ORDER_PAY: sum(rider_data[TIFFIN_ORDER_PAY] for rider_data in riders_data),
        XOOM_ORDER_PAY: sum(rider_data[XOOM_ORDER_PAY] for rider_data in riders_data),
        TOTAL_PAY_WITH_GUARANTEE: sum(rider_data[TOTAL_PAY_WITH_GUARANTEE] for rider_data in riders_data),
        SIGN_UP_BONUS: '-', LAST_SALARY_DIFFERENCE: '-',
        LOYALTY_BONUS_REDEEMED: sum(rider_data[LOYALTY_BONUS_REDEEMED] for rider_data in riders_data),
        REFERRAL_BONUS: sum(rider_data[REFERRAL_BONUS] for rider_data in riders_data),
        INSURANCE_AMOUNT: sum(rider_data[INSURANCE_AMOUNT] for rider_data in riders_data),
        CERTIFICATE_BONUS: sum(rider_data[CERTIFICATE_BONUS] for rider_data in riders_data),
        SECURITY_DEPOSITS_DEDUCTION: sum(rider_data[SECURITY_DEPOSITS_DEDUCTION] for rider_data in riders_data),
        FUEL_ALLOWANCE: sum(rider_data[FUEL_ALLOWANCE] for rider_data in riders_data),
        OVER_TIME_PAY: sum(rider_data[OVER_TIME_PAY] for rider_data in riders_data),
        RIDER_WALLET: '',
        FINAL_PAYOUT: sum(rider_data[FINAL_PAYOUT] for rider_data in riders_data),
    }
    cumulative_stats[UTR] = round(sum(rider_data[UTR] for rider_data in riders_data) / cumulative_stats[NIC], 1)

    riders_data.append(cumulative_stats)
    header = [NIC, CITY, RIDER_CATEGORY, RIDER_TYPE, TOTAL_PICKED_UP_ORDERS, WEEKEND_ORDERS, HOURS_WORKED, UTR,
              PICKUP_PAY, DROP_OFF_DISTANCE_PAY, DROP_OFF_DISTANCE, PICKUP_BONUS, PICKUP_DISTANCE, DROP_OFF_PAY,
              DELIVERY_CHARGES_BASED_PAY_PAY, PER_ORDER_PAY, SLAB_BASED_PAY, LATE_NIGHT_BONUS,
              NO_SHOW_DAYS, PENALTY, TOTAL_WITHOUT_GUARANTEE, PER_HOUR_INCOME, GUARANTEED_PAY_PER_HOUR, ACCEPTANCE_RATE,
              ON_TIME_RATE,
              TOTAL_ON_TIME_PICK_UPS, TOTAL_ON_TIME_DELIVERIES, FAILED_ORDERS, FAILED_ORDER_AMOUNT, UNACCEPTED_ORDERS,
              FAILED_RATE, APP_ON_RATE,
              GUARANTEE_QUALIFIES, GUARANTEE_RATE, FOOD_ORDER_PAY, HEALTH_CARE_ORDER_PAY, ERRAND_ORDER_PAY,
              BOOKS_ORDER_PAY,
              BEAUTY_ORDER_PAY, BABY_CARE_ORDER_PAY, PANTRY_ORDER_PAY, PHARMA_ORDER_PAY, TIFFIN_ORDER_PAY,
              XOOM_ORDER_PAY,
              TOTAL_PAY_WITH_GUARANTEE, SIGN_UP_BONUS, LAST_SALARY_DIFFERENCE, LOYALTY_BONUS_REDEEMED, REFERRAL_BONUS,
              INSURANCE_AMOUNT, CERTIFICATE_BONUS, SECURITY_DEPOSITS_DEDUCTION, FUEL_ALLOWANCE, OVER_TIME_PAY,
              RIDER_WALLET, FINAL_PAYOUT]
    subject = "RIDER SALARY REPORT"
    zip_file = ZiPFile.create_zip(riders_data, header, "Salary Report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(start_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
