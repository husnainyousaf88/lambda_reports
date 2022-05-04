class ReportSerializer:
    """
        Class responsible for validating data from API
    """
    data = None
    error = None

    def __init__(self, data):
        self.data = data

    def is_valid(self):
        """
        Check if data from api is valid or not
        :return: Bool
        """
        is_data_valid = True
        query_string = self.data.get('queryStringParameters', None)
        if query_string:
            start_date = query_string.get('start_date', None)
            end_date = query_string.get('end_date', None)
            email = query_string.get('email', None)
            report_type = query_string.get('report_type', None)
            if not start_date or not end_date or not email or not report_type:
                self.error = {"msg": "Field is None", 'fields': [start_date, end_date, email, report_type]}
                is_data_valid = False
        else:
            self.error = {"msg": "Invalid Query String", 'fields': [query_string]}
            is_data_valid = False
        return is_data_valid

    def get_validated_data(self):
        """
        Return validated fetch from request query params
        :return: Dict
        """
        query_string = self.data.get('queryStringParameters', None)
        start_date = query_string.get('start_date', None)
        end_date = query_string.get('end_date', None)
        email = query_string.get('email', None)
        report_type = query_string.get('report_type', None)

        return {"start_date": start_date, "end_date": end_date, "email": email, "report_type": report_type}
