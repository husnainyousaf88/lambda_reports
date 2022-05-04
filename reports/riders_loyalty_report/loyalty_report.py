from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_loyalty_report.data_factory import DataFactory
from datetime import timedelta, datetime

NAME = 'Name'
NIC = 'CNIC'
CITY = 'City'
POINTS_AT_BEGGING = "Points at Beginning"
POINTS_BETWEEN_PEROID = "Points between Period"
POINTS_AT_END = "Points at End"
PENALTY_POINTS = "Penalty Points in Period"
REDEEM_POINTS = "Redeem Points in Period"


def rider_loyalty(start_date, end_date, email, wallet_type=None):
    """
    Rider Loyalty report

    Parameters
    ----------
    start_date : datetime.date
    end_date : datetime.date
    recipients : typing.List[str]
        email(s) of the user(s) to whom the report will be sent
        :param wallet_type:
        :param start_date:
        :param end_date:
        :param email:
    """
    end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    riders_data = []
    riders = DataFactory.get_eligible_rider_report(start_date, end_date)
    for rider in riders:
        rider_id = rider[0]  # get rider_id
        rider_name = rider[1]  # get rider_name
        rider_nic = rider[2]  # get rider_nic
        rider_city = rider[3]  # get rider_city_name
        point_stats = DataFactory.get_points_stats(rider_id, start_date, end_date)
        point_at_beginning = point_stats['point_at_beginning']
        point_bw_peroid = point_stats['point_bw_period']
        point_at_end = point_stats['point_at_end']
        redeem_points = point_stats['redeem_points']
        penalty_points = point_stats['penalty_points']
        riders_data.append(
            {
                NAME: rider_name,
                NIC: rider_nic,
                CITY: rider_city,
                POINTS_AT_BEGGING: point_at_beginning,
                POINTS_BETWEEN_PEROID: point_bw_peroid,
                POINTS_AT_END: point_at_end,
                PENALTY_POINTS: penalty_points,
                REDEEM_POINTS: redeem_points,
            }
        )
    cumulative_stats = {
        NAME: '',
        NIC: len(riders_data), CITY: '',
        POINTS_AT_BEGGING: sum(rider_data[POINTS_BETWEEN_PEROID] for rider_data in riders_data),
        POINTS_BETWEEN_PEROID: sum(rider_data[POINTS_BETWEEN_PEROID] for rider_data in riders_data),
        POINTS_AT_END: sum(rider_data[POINTS_AT_END] for rider_data in riders_data),
        PENALTY_POINTS: sum(rider_data[PENALTY_POINTS] for rider_data in riders_data),
        REDEEM_POINTS: sum(rider_data[REDEEM_POINTS] for rider_data in riders_data),
    }
    riders_data.append(cumulative_stats)

    header = [NAME, NIC, CITY, POINTS_AT_BEGGING, POINTS_BETWEEN_PEROID, POINTS_AT_END, PENALTY_POINTS, REDEEM_POINTS]
    subject = "RIDER LOYALTY REPORT"
    zip_file = ZiPFile.create_zip(riders_data, header, "Loyalty Report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(end_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
