from flask import Flask
from flask import request
import json
from back_end.greenhouse.greenhouse import Greenhouse


class RestEndpoint(object):

    app = Flask(__name__)

    def __init__(self):
        pass

    @staticmethod
    @app.route('/')
    def root():
        return json.dumps({
            'message': 'This is a UNBC precision farm.',
            'success': True
        }), 200

    @staticmethod
    @app.route('/sensors', methods=['GET'])
    def sensors():
        """
        This endpoint returns the list of the current working sensors for the farm.
        """
        # TODO implement a mechanism for returning a list of the current working sensors
        return json.dumps({
            'message': '',
            'success': True
        }), 200

    @staticmethod
    @app.route('/sensors/<string:type>', methods=['GET'])
    def device(type):
        """
        This endpoint returns the current value of the specified sensor reading. eg. water_temp
        :param type: Specified environment variable to get the value for.
        """
        # TODO this
        return json.dumps({
            'message': '',
            'success': True
        }), 200

    @staticmethod
    @app.route('/climate', methods=['GET', 'POST'])
    def climate():
        """
        This endpoint returns the current climate status of the farm.
        """
        # TODO this
        if request.method == 'POST':
            return json.dumps({
                'message': 'Not Implemented',
                'success': True
            }), 200
        else:
            greenhouse = Greenhouse()
            return json.dumps({
                'message': greenhouse.current_state.to_json(),
                'success': True
            }), 200

    @staticmethod
    @app.route('/status', methods=['GET'])
    def status():
        """
        This endpoint returns the current status of the greenhouse. This includes the progress and time remaining
        of the climate pattern. It also displays any recoverable errors that have recently been caught.
        """
        greenhouse = Greenhouse()
        return json.dumps({
            'message': {
                'desired state': greenhouse.desired_state.to_json(),
                'elapsed time': greenhouse.elapsed_time
            },
            'success': True
        }), 200

    @staticmethod
    @app.route('/<path:path>')
    def catch_all(path):
        return json.dumps({
            'message': 'The requested endpoint could not be found on this server.',
            'success': False
        }), 404
