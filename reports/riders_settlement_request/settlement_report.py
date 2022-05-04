from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_settlement_request.data_factory import DataFactory
from reports.date_time import DateTime

DATETIME = 'Date/Time'
RIDER_NAME = 'Rider Name'
RIDER_CNIC = 'Rider CNIC'
ACCOUNT_NUMBER = 'Account No.'
AGENT_NAME = 'Agent Name'
AMOUNT = 'Amount'
STATUS = 'Status'

DATE_FORMAT = '%Y-%m-%d %H:%M'


def settlement_requests(start_date, end_date, email, wallet_type=None):
    """
    Rider settlement requests report

    Parameters
    ----------
    wallet_type: None
    start_date : datetime.date
    end_date : datetime.date
    email : str
        email of the user to whom the report will be sent
    """
    data = DateTime.get_dates(start_date, end_date)
    start_time, end_time = data['start_time'], data['end_time']
    s_requests = DataFactory.get_settlement_request(start_time, end_time)
    s_requests_data = [{
        DATETIME: DataFactory.convert_to_localtime(s_request[0], DATE_FORMAT),
        RIDER_NAME: s_request[1],
        RIDER_CNIC: s_request[2],
        ACCOUNT_NUMBER: s_request[3],
        AGENT_NAME: s_request[4] if s_request[7] else '',
        AMOUNT: s_request[5],
        STATUS: s_request[6]
    } for s_request in s_requests]

    header = [DATETIME, RIDER_NAME, RIDER_CNIC, ACCOUNT_NUMBER, AGENT_NAME, AMOUNT, STATUS]
    subject = "RIDER SETTLEMENT REPORT"
    zip_file = ZiPFile.create_zip(s_requests_data, header, "Settlement Report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(start_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
