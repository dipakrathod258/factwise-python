from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.mysql_util.singleton import Singleton
from src.log_conf import Logger

LOGGER = Logger.get_logger(__name__)


class SQLAlchemyConnectionManager(metaclass=Singleton):

    def __init__(self):

        host = '127.0.0.1'
        database = 'factwise_project_board'
        user = 'root'
        password = 'Alternation1.'

        self.engine = create_engine(
            f'mysql+pymysql://{user}:{password}@{host}/{database}')

        self.Session = sessionmaker(bind=self.engine)


