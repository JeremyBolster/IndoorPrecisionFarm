from back_end.configuration import Config
from back_end.databases.database_connection import DataBaseConnector
from back_end.databases.time_series_database_connection import TSDataBaseConnector
from back_end.log import GreenHouseLog
from back_end.greenhouse.greenhouse import Greenhouse
from back_end.greenhouse.communication.simulated_arduino import ArduinoSimulated
import click
import time


@click.group()
@click.option('--color', help='Specify if logs should be colored or not')
@click.option('--output', default=True, help='Specify if logs should appear on stderr.', type=click.BOOL)
@click.option('--logfile', default='./greenhouse.log', help='Specify the output location of the logfile.', type=click.format_filename)
def cli(color, output, logfile):
    # TODO add color option
    GreenHouseLog().set_up_loggers(logfile, output)
    Config().configure()
    DataBaseConnector().check_connection()
    TSDataBaseConnector().check_connection()


@cli.command()
@click.option('--device', help='Specify the device to connect to sensors with. E.G. /dev/xyz  or simulated')
@click.option('--pattern', help='Specify the climate pattern to run.', type=click.format_filename)
def run(device, pattern):
    """Run an instance of a greenhouse"""
    # TODO do something with the device
    # TODO we should while true this I guess
    greenhouse = Greenhouse()
    greenhouse.setup(ArduinoSimulated(), pattern)
    greenhouse.run()
    time.sleep(30)


@cli.command('check-db')
def check_db():
    """Check the connection to the databases"""
    pass


if __name__ == '__main__':
    cli()
