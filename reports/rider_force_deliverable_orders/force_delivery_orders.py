from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.rider_force_deliverable_orders.data_factory import DataFactory

ORDER_NUMBER = 'Order Number'
RIDER = 'Rider'
DELIVERER_NAME = 'Deliverer Name'
FORCE_DELIVERY_CATEGORY = 'Force Delivery Category'
FORCE_DELIVERY_DESCRIPTION = 'Force Delivery description'
DELIVERY_TIME = 'Delivery Time'


def force_deliverable_orders(start_date, end_date, email,  wallet_type=None):
    """
    Force delivered orders report

    Parameters
    ----------
    start_date : datetime.date
    end_date : datetime.date
    wallet_type : None
    email : str
        email of the user to whom the report will be sent
    """

    rider_data = DataFactory.get_riders_data(start_date, end_date)
    riders_data = [{
        ORDER_NUMBER: data[0],
        RIDER: data[1],
        DELIVERER_NAME: data[2],
        FORCE_DELIVERY_CATEGORY: data[3],
        FORCE_DELIVERY_DESCRIPTION: data[4],
        DELIVERY_TIME: data[5],
    } for data in rider_data]

    header = [ORDER_NUMBER, RIDER, DELIVERER_NAME, FORCE_DELIVERY_CATEGORY, FORCE_DELIVERY_DESCRIPTION,
              DELIVERY_TIME]
    subject = "RIDER FORCE DELIVERABLE ORDERS"
    zip_file = ZiPFile.create_zip(riders_data, header, "Rider Force deliverable Report.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(start_date, end_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
