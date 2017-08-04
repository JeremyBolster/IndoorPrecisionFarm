from back_end.configuration import Config
from back_end.databases.database_connection import DataBaseConnector
from back_end.databases.time_series_database_connection import TSDataBaseConnector
from back_end.log import GreenHouseLog
import click


@click.command()
@click.option('--output', default=True, help='Specify if logs should appear on stderr.', type=click.BOOL)
@click.option('--logfile', default='./greenhouse.log', help='Specify the output location of the logfile.', type=click.format_filename)
def cli(output, logfile):
    GreenHouseLog().set_up_loggers(logfile, output)
    Config().configure()
    DataBaseConnector().check_connection()
    TSDataBaseConnector().check_connection()


if __name__ == '__main__':
    cli()
