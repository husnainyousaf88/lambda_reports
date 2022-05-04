from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_detail_report.data_factory import DataFactory

ID = 'ID'
NIC = 'CNIC'
CITY = 'City'
NAME = 'Name'
MOBILE_NUMBER = 'Mobile Number'
REFERRED_BY_ID = 'Referred BY ID'
REFERRED_BY_NIC = 'Referred BY NIC'
ENABLED = "Enabled"
JOINING_DATE = 'Joining Date'
ADDRESS = 'Address'
WALLET_TYPE = "E Wallet Type"
WALLET_Number = "E Wallet Number"
FIRST_ORDER_ASSIGNED = "First Order Assigned At"
FIRST_ORDER_PICKED_UP = "First Order Picked Up At"
FIRST_ORDER_DELIVERED = "First Order Delivered At"
FIRST_DELIVERED_ORDER_NUMBER = "First Delivered Order Number"
LAST_ORDER_DELIVERED = "Last Order Delivered At"


def rider_details(start_date=None, end_date=None, email=None, wallet_type=None):
    """
    Emails Details of all riders in related cities to requested dashboard user email address.
    """

    riders = DataFactory.get_riders_all_data(wallet_type)

    riders_data = [{ID: rider[0], NAME: rider[1], NIC: rider[2], MOBILE_NUMBER: rider[3],
                    REFERRED_BY_ID: '' if rider[4] is None else rider[5],
                    REFERRED_BY_NIC: '' if rider[4] is None else rider[6],
                    ENABLED: rider[7], WALLET_TYPE: rider[8],
                    WALLET_Number: rider[9],
                    JOINING_DATE: rider[10], ADDRESS: rider[11], CITY: rider[12],
                    FIRST_ORDER_ASSIGNED: rider[13],
                    FIRST_ORDER_PICKED_UP: rider[14],
                    FIRST_ORDER_DELIVERED: rider[15],
                    FIRST_DELIVERED_ORDER_NUMBER:rider[17],
                    LAST_ORDER_DELIVERED: rider[16]}
                   for rider in riders]

    header = [ID, NAME, NIC, MOBILE_NUMBER, REFERRED_BY_ID, REFERRED_BY_NIC, ENABLED, WALLET_TYPE, WALLET_Number,
              JOINING_DATE, ADDRESS, CITY, FIRST_ORDER_ASSIGNED, FIRST_ORDER_PICKED_UP, FIRST_ORDER_DELIVERED,
              FIRST_DELIVERED_ORDER_NUMBER, LAST_ORDER_DELIVERED]
    subject = "RIDER DETAIL REPORT"
    zip_file = ZiPFile.create_zip(riders_data, header, "detail Report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(start_date=None, end_date=None, subject=subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
