from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_covid_19_sops.data_factory import DataFactory

ORDER_NUMBER = 'Order #'
RIDER_ID = 'Rider Id'
CNIC = 'Cnic'
RIDER_NAME = 'Rider Name'
RIDER_PHONE = 'Rider Phone'
WEARING_MASK = 'Wearing Mask'
WEARING_GLOVES = 'Wearing Gloves'
MAINTAIN_SOCIAL_DISTANCE = 'Maintain Social Distance'
DELIVERY_BAG = 'Delivery Bag'


def covid_19_sops(start_date, end_date, email, wallet_type=None):
    sops_logs = DataFactory.get_riders_detail(start_date, end_date)
    sops_data = [{
        ORDER_NUMBER: log[0],
        RIDER_ID: log[1],
        CNIC: log[2],
        RIDER_NAME: log[3],
        RIDER_PHONE: log[4],
        WEARING_MASK: log[5],
        WEARING_GLOVES: log[6],
        MAINTAIN_SOCIAL_DISTANCE: log[7],
        DELIVERY_BAG: log[8],
    } for log in sops_logs]
    header = [ORDER_NUMBER, RIDER_ID, CNIC, RIDER_NAME, RIDER_PHONE, WEARING_MASK, WEARING_GLOVES,
              MAINTAIN_SOCIAL_DISTANCE, DELIVERY_BAG]

    subject = "RIDER CASH COLLECTION REPORT"
    zip_file = ZiPFile.create_zip(sops_data, header, "Rider sops Report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(start_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
