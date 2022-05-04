from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_cash_collection.data_factory import DataFactory
from datetime import timedelta
########################################
#  CSV HEADERS
########################################

NAME = 'Rider'
NIC = 'NIC'
RIDER_CITY = 'Rider City'
PICKUP_PAY = 'Pickup Pay'
PICKUP_DISTANCE = "Pickup Distance KM"
DROP_OFF_PAY = 'Drop-off Pay'
DROP_OFF_DISTANCE = "Drop-off Distance KM"
FUEL_ALLOWANCE = "Fuel Allowance"
INITIAL_RECEIVABLE = 'Initial Receivable'
RECEIVABLES_AT_DEPOSITED_TIME = "Receivables at Deposited Time"
AMOUNT_RECEIVED = "Amount Received"
RECEIVABLES_LEFT = "Receivables Left"
DEPOSITED_AT = "Deposited At"
JAZZ_CASH_ID = "Jazzcash ID"


def rider_cash_collection(start_date, end_date, email, wallet_type=None):
    """
    Rider's jazz cash collection summary report

    Parameters
    ----------
    wallet_type : None
    start_date : datetime.date
    end_date : datetime.date
    email : str
        email of the user to whom the report will be sent
    """
    riders_data = []
    jc_logs = DataFactory.rider_cash_collection_log(start_date, end_date)
    for jc_log in jc_logs:
        rider_id = jc_log[0]   # get rider id
        rider_cash_id = jc_log[1]  # get rider_cash_id
        actual_receivables = jc_log[2]  # get actual_receivables
        rider_cash_created_at = jc_log[3]  # get rider_cash_created_at
        rider_nic = jc_log[4]  # get rider_nic
        rider_name = jc_log[5]  # get rider_name
        city_name = jc_log[6]  # get city_name
        auth_id = jc_log[7]  # get auth_id
        amount = jc_log[8]  # get rider_cash_amount

        second_last_jc_log = DataFactory.get_riders_cash(rider_id, rider_cash_id)
        if second_last_jc_log:
            rider_cash_ids = DataFactory.get_rider_cash_ids(rider_id, rider_cash_id, second_last_jc_log)
        else:
            rider_cash_ids = DataFactory.get_rider_cash_id(rider_id, rider_cash_id)
        pick_up_distance_bonus = pickup_distance = drop_off_distance_pay = delivered_distance = fuel_allowance = 0
        rc_fuel_logs = DataFactory.get_rider_order_id(rider_id, rider_cash_ids)
        if rc_fuel_logs:
            list_order_ids = []
            for rc_fuel_log in rc_fuel_logs:
                try:
                    order_ids = eval(rc_fuel_log[0])  # get order_ids
                    if len(order_ids) > 0:
                        list_order_ids = list_order_ids + order_ids
                except Exception as e:
                    pass

            pickup_distance, delivered_distance = DataFactory.get_rider_pickup_delivery_stats(tuple(list_order_ids), rider_id)
            earnings_data = DataFactory.get_riders_earning(tuple(list_order_ids), rider_id)
            pick_up_distance_bonus = earnings_data['pick_up_distance_bonus']
            drop_off_distance_pay = earnings_data['drop_off_distance_pay']
            fuel_allowance = pick_up_distance_bonus + drop_off_distance_pay
        receivables_without_fuel_amount = actual_receivables - fuel_allowance
        updated_deposited_time = rider_cash_created_at + timedelta(hours=5)
        riders_data.append({NAME: rider_name, NIC: rider_nic,
                            RIDER_CITY: city_name,
                            PICKUP_PAY: pick_up_distance_bonus,
                            PICKUP_DISTANCE: pickup_distance,
                            DROP_OFF_PAY: drop_off_distance_pay,
                            DROP_OFF_DISTANCE: delivered_distance,
                            FUEL_ALLOWANCE: fuel_allowance,
                            INITIAL_RECEIVABLE: actual_receivables,
                            RECEIVABLES_AT_DEPOSITED_TIME: receivables_without_fuel_amount,
                            AMOUNT_RECEIVED: amount,
                            RECEIVABLES_LEFT: receivables_without_fuel_amount - amount,
                            DEPOSITED_AT: updated_deposited_time,
                            JAZZ_CASH_ID: auth_id
                            })
    header = [NAME, NIC, RIDER_CITY, PICKUP_PAY, PICKUP_DISTANCE, DROP_OFF_PAY,
              DROP_OFF_DISTANCE, FUEL_ALLOWANCE, INITIAL_RECEIVABLE, RECEIVABLES_AT_DEPOSITED_TIME, AMOUNT_RECEIVED,
              RECEIVABLES_LEFT, DEPOSITED_AT, JAZZ_CASH_ID]
    subject = "RIDER CASH COLLECTION REPORT"
    zip_file = ZiPFile.create_zip(riders_data, header, "cash collection Report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(start_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
