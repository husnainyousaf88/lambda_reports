from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_fill_report.data_factory import DataFactory


########################################
#  CSV HEADERS
########################################

ID = 'ID'
SHIFT_START_DATE = 'Shift Start Date'
SHIFT_START_TIME = 'Shift Start Time'
SHIFT_END_DATE = 'Shift End Date'
SHIFT_END_TIME = 'Shift End Time'
HOT_SPOT = 'HotSpot'
CITY = 'City'
RIDER_REQUIRED = 'Rider Required'


def get_rider_fill_rate(start_date, end_date, email, wallet_type=None):
    """
    Create and Send Email Rider Fill Rate Report
    Parameters
    ----------
    wallet_type: None
    start_date: Date Object
    end_date: Date Object
    email: str( user_email)
    Returns
    -------
        None
    """
    shifts = DataFactory.get_rider_shifts(start_date, end_date)
    riders_data = [{ID: shift[0], SHIFT_START_DATE:shift[1].date(), SHIFT_START_TIME: shift[1].time(), SHIFT_END_DATE:shift[2].date(),
                    SHIFT_END_TIME:shift[2].time(), HOT_SPOT:shift[3], CITY: shift[4], RIDER_REQUIRED:shift[5]}
                   for shift in shifts]
    subject = "RIDER_FILL_RATE_REPORT"
    header = [ID, SHIFT_START_DATE, SHIFT_START_TIME, SHIFT_END_DATE, SHIFT_END_TIME, HOT_SPOT, CITY, RIDER_REQUIRED]
    zip_file = ZiPFile.create_zip(riders_data, header, "Fill Rate Report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(start_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
