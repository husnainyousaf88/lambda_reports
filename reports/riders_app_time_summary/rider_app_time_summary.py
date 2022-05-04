from utilities.attachment import ZiPFile
from utilities.email_service import EmailFactory
from reports.riders_app_time_summary.data_factory import DataFactory
from datetime import timedelta
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def rider_app_time_summary(start_date, report_date, email, wallet_type=None):
    """
    Rider App times summary report

    Parameters
    ----------
    start_date : None
    wallet_type : None
    report_date : datetime.date
        the date from which times need to be calculated
    email : str
        email of the user to whom the report will be sent
    """
    records = []
    riders_stats = DataFactory.get_rider_stats(report_date)
    for rider_stats in riders_stats:
        rider_id = rider_stats[0]  # get rider_id
        rider_name = rider_stats[1]  # get rider_name
        rider_number = rider_stats[2]  # get rider_number
        rider_total_time = rider_stats[3]  # get rider total time
        rider_total_pause_time = rider_stats[4]  # get rider pause time
        pause_time = '-'
        resume_time = '-'
        resume_times = DataFactory.get_resume_time(report_date, rider_id)
        pause_times = DataFactory.get_pause_time(report_date, rider_id)
        if pause_times:
            pause_time = ((pause_time[0] + timedelta(hours=5)).strftime(DATETIME_FORMAT)
                          for pause_time in pause_times)
            pause_time = ', '.join(pause_time)

        if resume_time:
            resume_time = ((resume_time[0] + timedelta(hours=5)).strftime(DATETIME_FORMAT)for resume_time in resume_times)
            resume_time = ','.join(resume_time)
        records.append({
            'rider': '{} | {}'.format(rider_name, rider_number),
            'total_time': rider_total_time,
            'total_worked_time': rider_total_time - rider_total_pause_time,
            'total_pause_time': rider_total_pause_time,
            'pause_time': pause_time,
            'resume_time': resume_time
        })
    header = ['rider', 'total_time', 'total_worked_time', 'total_pause_time', 'pause_time', 'resume_time']
    subject = "RIDER APP TIME SUMMARY"
    zip_file = ZiPFile.create_zip(records, header, "app_time_summary.csv")
    attachment = {'name': zip_file[0] + '.zip', 'content': zip_file[1]}
    email_service = EmailFactory(start_date, report_date, subject)
    email_service.send_email_with_attachment(attachment=attachment, receiver=email)
