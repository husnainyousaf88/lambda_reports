import threading
from utilities.response import json_response
from reports.report_factory import ReportFactory
from utilities.serializers import ReportSerializer
from settings.base import (TEST_RECEIVER, TEST_START_DATE, TEST_END_DATE, TEST_REPORT_TYPE, DEBUG)


def lambda_handler(event, context):
    """
    Main function called AWS lambda
    Parameters
    ----------
    event: key
    context: value
    Returns
    -------
        None
    """
    if DEBUG:  # added to directly run on AWS Lambda
        report_factory = ReportFactory(start_date=TEST_START_DATE, end_date=TEST_END_DATE, email=TEST_RECEIVER,
                                       report_type=TEST_REPORT_TYPE)
        report_factory.generate_report()
    else:
        try:
            serializer = ReportSerializer(data=event)
            if serializer.is_valid():
                validated_data = serializer.get_validated_data()
                start_date = validated_data['start_date']
                end_date = validated_data['end_date']
                email = validated_data['email']
                report_type = validated_data['report_type']
                report_factory = ReportFactory(start_date=start_date, end_date=end_date, email=email,
                                               report_type=int(report_type))
                report_factory.generate_report()
                return json_response(code=200, msg="Report will be sent soon")
            else:
                return json_response(code=400, msg="errors", error=serializer.error)
        except Exception as e:
            return json_response(code=400, msg=str(e.args), error=serializer.error)
