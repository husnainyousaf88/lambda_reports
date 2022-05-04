from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_on_time_rate_report.data_factory import DataFactory
from reports.date_time import DateTime

NAME = 'Name'
CITY = 'City'
NIC = 'CNIC'
ID = 'ID'
MOBILE_NUMBER = 'Mobile Number'
ON_TIME_RATE = 'On Time Rate'


def on_time_rate(start_date, end_date, email, Wallet_type=None):
    """
    Takes start and end date range. Calculates on time rate of each rider and sends report as an email to admin.
    """
    data = DateTime.get_dates(start_date, end_date)
    start_time, end_time = data['start_time'], data['end_time']
    start_date, end_date = data['start_date'], data['end_date']
    riders_data = []
    riders = DataFactory.get_rider_data(start_time, end_time)
    for rider in riders:
        rider_id = rider[0]  # get ride id
        rider_name = rider[1]  # get rider name
        rider_nic = rider[2]  # get rider nic
        rider_mobile = rider[3]  # get rider mobile number
        city_name = rider[4]  # get city name
        order_stats = DataFactory.get_rider_order_stats(rider_id, start_time, end_time)
        total_picked_up_orders = order_stats['total_picked_up_orders']
        total_delivered_orders = order_stats['total_delivered_orders']
        on_time_rate = DataFactory.calculate_on_time_rates(rider_id, start_time, end_time, total_delivered_orders,
                                                           total_picked_up_orders)
        riders_data.append(
            {ID: rider_id, NAME: rider_name, NIC: rider_nic, MOBILE_NUMBER: rider_mobile, CITY: city_name,
             ON_TIME_RATE: on_time_rate})

    cumulative_stats = {ID: '', NAME: '', NIC: '', MOBILE_NUMBER: '', CITY: '',
                            ON_TIME_RATE: sum(rider_data[ON_TIME_RATE] for rider_data in riders_data)}
    riders_data.append(cumulative_stats)
    header = [ID, NAME, NIC, MOBILE_NUMBER, CITY, ON_TIME_RATE]
    subject = "RIDER ON TIME REPORT"
    zip_file = ZiPFile.create_zip(riders_data, header, "on time Report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(start_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
