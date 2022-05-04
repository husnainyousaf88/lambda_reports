import sys
import logging
import pymysql
from .prod import ProdDatabase
from .staging import StagingDatabase
from .preprod import PreProdDatabase
from .local import LocalDatabase

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Database:
    def __init__(self):
        pass

    @staticmethod
    def connection(db_env):
        databases = {
            'prod': ProdDatabase,
            'staging': StagingDatabase,
            'preprod': PreProdDatabase,
            'local': LocalDatabase
        }
        selected_db = databases[db_env]
        try:
            connection = pymysql.connect(host=selected_db['endpoint'],
                                         port=3306,
                                         user=selected_db['username'],
                                         passwd=selected_db['password'],
                                         db=selected_db['database_name'])
        except pymysql.MySQLError as e:
            logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            logger.error(e)
            sys.exit()
        cursor = connection.cursor()
        return cursor
