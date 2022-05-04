from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_shift_report.data_factory import DataFactory
from datetime import datetime, timedelta


RIDER_ID = 'Rider ID'
RIDER_SHIFT_ID = 'Rider Shift ID'
NAME = 'Name'
MOBILE_NUMBER = 'Mobile Number'
NIC = 'CNIC'
CITY = 'City'
HOTSPOT = 'Hotspot'
STATUS = 'Status'
SHIFT_START_DATE = 'Shift Start Date'
SHIFT_START_TIME = 'Shift Start Time'
SHIFT_END_DATE = 'Shift End Date'
SHIFT_END_TIME = 'Shift End Time'
RIDER_STARTED_SHIFT_AT = 'Rider Started Shift at'


def rider_shifts(start_date, end_date, email, rider, wallet_type=None):
    """
    Rider Shifts Report, Return Riders, Taken/started shifts of selected date range for specificn rider

    Parameters
    ----------
    wallet_type: None
    start_date : datetime.date
        Shift start_at
    end_date : datetime.date
        Shift start_at
    email : typing.List[str]
        email(s) of the user(s) to whom the report will be sent
    rider : dict

    """

    rider_shift = DataFactory.get_rider_shift_data(start_date, end_date, rider)
    rider_data = [{
        RIDER_ID: rider,  # user id
        RIDER_SHIFT_ID: rs[0],  # rider shift_id
        NAME: rs[5],  # rider_name
        MOBILE_NUMBER: rs[6],  # rider mobile
        NIC: rs[7],  # rider nic
        CITY: rs[8],  # rider city
        HOTSPOT: rs[1],  # rider area_name
        STATUS: 'Started' if rs[2] is not None else 'Taken',
        SHIFT_START_DATE: rs[3].date(),  # get rider start date
        SHIFT_START_TIME: rs[3].time(),  # get rider start time
        SHIFT_END_DATE: rs[4].date(),  # get rider end_date
        SHIFT_END_TIME: rs[4].time(),  # rider end_time
        RIDER_STARTED_SHIFT_AT: rs[2].time() if rs[2] is not None else ''
    } for rs in rider_shift]
    header = [RIDER_ID, RIDER_SHIFT_ID, NAME, MOBILE_NUMBER, NIC, CITY, HOTSPOT, STATUS,
              SHIFT_START_DATE, SHIFT_START_TIME, SHIFT_END_DATE, SHIFT_END_TIME, RIDER_STARTED_SHIFT_AT]
    subject = "RIDER SHIFT REPORT"
    zip_file = ZiPFile.create_zip(rider_data, header, "rider shift.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(start_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
