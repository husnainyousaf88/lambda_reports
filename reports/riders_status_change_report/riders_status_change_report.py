from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_status_change_report.data_factory import DataFactory
from datetime import datetime, timedelta

AGENT_ID = 'Agent ID'
AGENT_NAME = 'Agent Name'
AGENT_EMAIL = "Agent Email"
AGENT_LAST_LOGIN = "Agent Last Login"
RIDER_ID = 'Rider ID'
RIDER_NAME = 'Rider Name'
ACTION = 'Action'
MESSAGE = 'Message'
DATETIME = "Date & Time"


def rider_states(start_date, end_date, email, wallet_type=None):
    end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    logs = DataFactory.logs_query(start_date, end_date)
    logs_data = [{
        AGENT_ID: log[0],  # get agent_id
        AGENT_NAME: log[1],  # get agent_name
        AGENT_EMAIL: log[2],  # get agent_email
        AGENT_LAST_LOGIN: log[3],  # get agent_last_login
        RIDER_ID: log[4],  # get rider_id
        RIDER_NAME: log[5],  # get rider_name
        ACTION: log[6],  # get action
        MESSAGE: log[7],  # get message
        DATETIME: str(log[8]),  # get date
    } for log in logs]
    header = [AGENT_ID, AGENT_NAME, AGENT_EMAIL, AGENT_LAST_LOGIN, RIDER_ID, RIDER_NAME, ACTION, MESSAGE, DATETIME]
    subject = "RIDER STATE CHANGE REPORT"
    zip_file = ZiPFile.create_zip(logs_data, header, "Rider enable disable report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(start_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
