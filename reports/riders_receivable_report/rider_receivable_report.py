from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_receivable_report.data_factory import DataFactory
from reports.date_time import DateTime

ID = 'ID'
NAME = 'Name'
MOBILE_NUMBER = 'Mobile Number'
NIC = 'CNIC'
RIDER_CITY = 'Rider City'
EQUIPMENT_COST = 'Equipment Cost'
PICKUP_BONUS = 'Pickup Bonus (PB)'
PICKUP_DISTANCE = "Pickup Distance KM"
DROP_OFF_DISTANCE_PAY = 'Drop-off Pay (DDP)'
DROP_OFF_DISTANCE = "Drop-off Distance KM"
RECEIVABLE_AMOUNT = 'Receivable Amount'
FUEL_ALLOWANCE = "Fuel Allowance"
FINAL_RECEIVABLE_AMOUNT = "Final Receivable Amount"
LAST_SETTLEMENT_DATE = 'Last Settlement Date'
DATE_LAST_SETTLEMENT = 'Date'
TIME_LAST_SETTLEMENT = 'Time'


def get_rider_receivables(start_date=None, end_date=None, email=None, wallet_type=None):
    """
    Rider's actual receivables summary report till report date

    Parameters
    ----------
    :param email: typing.List[str]
    email(s) of the user(s) to whom the report will be sent
    :param end_date: datetime.date
    :param wallet_type: None
    :param start_date: None
    """

    riders_data = []
    riders = DataFactory.get_eligible_riders()

    for rider in riders:
        rider_id = rider[0]  # get rider id
        cash_in_hand = rider[1]  # get rider cash in hand
        rider_name = rider[2]  # get rider name
        city_name = rider[3]  # get city name
        rider_mobile_number = rider[4]  # get rider mobile number
        rider_nic = rider[5]  # get rider nic

        report_last_settlement = ''
        report_last_settlement_date = ''
        report_last_settlement_time = ''
        last_settlement = DataFactory.get_last_settlement_query(end_date, rider_id)
        if last_settlement:
            report_last_settlement = str(last_settlement)
            last_settlement_date = str(last_settlement.date())
            report_last_settlement_time = str(last_settlement.time())
            report_last_settlement_date = last_settlement_date
            # start and end times for filter earnings
            data = DateTime.get_dates(last_settlement_date, end_date)
            start_time, end_time = report_last_settlement, data['end_time']
        else:
            config = DataFactory.get_logistics_configuration_instance()
            # start and end times for filter earnings
            data = DateTime.get_dates(config, end_date)
            start_time, end_time = data['start_time'], data['end_time']
        rc_sum = DataFactory.get_rc_sum_query(end_date, rider_id)
        trans_type_c = rc_sum["trans_type_c"]
        trans_type_d = rc_sum["trans_type_d"]
        sum_total = trans_type_c - trans_type_d
        receivable_amount = cash_in_hand - sum_total
        equipment_cost = DataFactory.get_equipment_cost(rider_id, start_time, end_time)
        pickup_distance = DataFactory.get_rider_pickup_distances(rider_id, start_time, end_time)
        delivered_distance = DataFactory.get_rider_drop_off_distances(rider_id, start_time, end_time)
        earnings_data = DataFactory.get_rider_earnings(rider_id, start_time, end_time)
        pick_up_distance_bonus = earnings_data["pick_up_distance_bonus"]
        drop_off_distance_pay = earnings_data["drop_off_distance_pay"]
        fuel_allowance = pick_up_distance_bonus + drop_off_distance_pay
        final_receivable_amount = receivable_amount - fuel_allowance
        if final_receivable_amount >= 1:
            riders_data.append({ID: rider_id, NAME: rider_name, MOBILE_NUMBER: rider_mobile_number,
                                RIDER_CITY: city_name, NIC: rider_nic,
                                EQUIPMENT_COST: equipment_cost,
                                PICKUP_BONUS: pick_up_distance_bonus,
                                PICKUP_DISTANCE: pickup_distance,
                                DROP_OFF_DISTANCE_PAY: drop_off_distance_pay,
                                DROP_OFF_DISTANCE: delivered_distance,
                                RECEIVABLE_AMOUNT: receivable_amount,
                                FUEL_ALLOWANCE: fuel_allowance,
                                FINAL_RECEIVABLE_AMOUNT: final_receivable_amount,
                                LAST_SETTLEMENT_DATE: report_last_settlement,
                                DATE_LAST_SETTLEMENT: report_last_settlement_date,
                                TIME_LAST_SETTLEMENT: report_last_settlement_time
                                })
    header = [ID, NAME, MOBILE_NUMBER, NIC, RIDER_CITY, EQUIPMENT_COST, PICKUP_BONUS, PICKUP_DISTANCE,
              DROP_OFF_DISTANCE_PAY, DROP_OFF_DISTANCE, RECEIVABLE_AMOUNT, FUEL_ALLOWANCE, FINAL_RECEIVABLE_AMOUNT,
              LAST_SETTLEMENT_DATE, DATE_LAST_SETTLEMENT, TIME_LAST_SETTLEMENT]
    subject = "RIDER RECEIVABLE REPORT"
    zip_file = ZiPFile.create_zip(riders_data, header, "receivable Report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(end_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
