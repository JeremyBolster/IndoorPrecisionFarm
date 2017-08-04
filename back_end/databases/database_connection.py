import logging
import psycopg2
import traceback
from back_end.configuration import Config
from contextlib import contextmanager


class DataBaseConnector(object):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.config = Config.config
        self.host = self.config['postgres']['host']
        self.db_name = self.config['postgres']['db']
        self.user = self.config['postgres']['username']
        self.password = self.config['postgres']['password']
        self.port = self.config['postgres']['port']

    def check_connection(self) -> None:
        with self.__connect() as cursor:
            if cursor:
                self.log.info("Connected to primary data store successfully.")
            else:
                self.log.info("Unable to Connect to primary data store.")

    @contextmanager
    def __connect(self) -> None:

        conn_string = "host='{host}' dbname='{db_name}' user='{user}' password='{password}' port='{port}'".format(
            host=self.host, db_name=self.db_name, user=self.user, password=self.password, port=self.port
        )

        # print the connection string we will use to connect
        self.log.info("Connecting to database -> {db}".format(db=conn_string))

        try:
            # get a connection, if a connect cannot be made an exception will be raised here
            conn = psycopg2.connect(conn_string)
            # conn.cursor will return a cursor object, you can use this cursor to perform queries
            cursor = conn.cursor()
            yield cursor
            cursor.close()
        except psycopg2.OperationalError as exc:
            self.log.error("Uh oh, can't connect to primary data store. Invalid dbname, user or password? %s",
                           conn_string)
            self.log.debug("DB Error %s ", traceback.format_exc())
            yield None  # This keeps us from throwing a context manager exception right after which bloats the logs

    def __execute(self):
        # TODO implement this
        with self.__connect() as cursor:
            cursor.execute("SELECT * from tutorials")
            rows = cursor.fetchall()
            print(rows)

