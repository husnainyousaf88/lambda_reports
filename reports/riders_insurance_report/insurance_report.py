from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_insurance_report.data_factory import DataFactory
from reports.date_time import DateTime

NAME = 'Name'
NIC = 'CNIC'
CITY = 'City'
INSURANCE_DATE = 'Insurance Date'
CHURN_DATE = 'Churn Date'


def rider_insurance(start_date, end_date, email, wallet_type=None):
    """
    Rider Insurance report

    Parameters
    ----------
    wallet_type : None
    start_date : datetime.date
    end_date : datetime.date
    email : typing.List[str]
        email(s) of the user(s) to whom the report will be sent
    """

    riders_data = []
    data = DateTime.get_dates(start_date, end_date)
    start_time, end_time = data['start_time'], data['end_time']

    insurance_id = DataFactory.get_insurance_data(start_time, end_time)
    res = tuple(sub[1] for sub in insurance_id)
    orders = "','".join((str(order) for order in res))
    riders = DataFactory.get_rider_insurance(orders)
    for rider in riders:
        name = rider[1]
        nic = rider[0]
        city = rider[2]

        riders_data.append(
            {
                NAME: name,
                NIC: nic,
                CITY: city,
                INSURANCE_DATE: rider[3],
                CHURN_DATE: rider[4]
            }
        )
    cumulative_stats = {
        NAME: '',
        NIC: len(riders_data),
        CITY: '',
        INSURANCE_DATE: '',
        CHURN_DATE: ''

    }
    riders_data.append(cumulative_stats)

    header = [NAME, NIC, CITY, INSURANCE_DATE, CHURN_DATE]
    subject = "RIDER INSURANCE REPORT"
    zip_file = ZiPFile.create_zip(riders_data, header, "insurance Report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(end_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
