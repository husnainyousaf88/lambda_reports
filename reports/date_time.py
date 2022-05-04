from datetime import datetime, timedelta


class DateTime:
    """
    Validate and convert start_date and end_date into start_time and end_time
    return : dictionary
    """
    @staticmethod
    def get_dates(start_date, end_date):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        start_time = datetime.strptime('{date} 23:59:00'.format(date=start_date - timedelta(days=1)),
                                       '%Y-%m-%d %H:%M:%S')
        end_time = min(datetime.strptime('{date} 23:59:00'.format(date=end_date),
                                         '%Y-%m-%d %H:%M:%S'), datetime.now())
        result = {'start_time': start_time, 'end_time': end_time, 'start_date': start_date, 'end_date': end_date}
        return result
