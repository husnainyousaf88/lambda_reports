from .database import Database

SENDER_EMAIL = 'husnain.yousaf@cheetay.pk'
EMAIL_SUBJECT = 'Rider Fill Report {} - {}'


TEST_START_DATE = '2021-10-01'
TEST_END_DATE = '2021-10-30'

TEST_RECEIVER = 'husnain.yousaf@cheetay.pk'
TEST_REPORT_TYPE = 2


DEBUG = False  # In case you want to run lambda function directly from AWS, from api need to keep it false.

db_env = "prod"
connection = Database.connection(db_env)
