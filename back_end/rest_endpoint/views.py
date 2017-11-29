from flask import Flask
from flask import request
from flask import send_file
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
    @app.route('/api/')
    def api():
        return json.dumps({
            'supported_api_versions': ['v1'],
            'success': True
        }), 200

    @staticmethod
    @app.route('/api/v1/')
    def api_v1():
        return json.dumps({
            'endpoints': [
                '/api/v1/climate/',
                '/api/v1/pattern/',
                '/api/v1/status/',
                '/api/v1/image/'
                ],
            'success': True
        }), 200

    @staticmethod
    @app.route('/api/v1/climate/', methods=['GET'])
    def api_v1_climate():
        """
        This endpoint returns the current climate values of the farm.
        """
        greenhouse = Greenhouse()
        return json.dumps({
            'message': greenhouse.current_state.to_json(),
            'success': True
        }), 200

    @staticmethod
    @app.route('/api/v1/pattern/', methods=['GET', 'POST'])
    def api_v1_pattern():
        """
        GET: This endpoint returns the current pattern executing on the farm
        POST: This endpoint allows for the current pattern to be replaced
        """
        # TODO this
        if request.method == 'POST':
            return json.dumps({
                'message': 'Not Implemented',
                'success': True
            }), 200
        else:
            return json.dumps({
                'message': 'Not Implemented',
                'success': True
            }), 200

    @staticmethod
    @app.route('/api/v1/status/', methods=['GET'])
    def api_v1_status():
        """
        This endpoint returns various reporting information. Examples of this are:
            - Progress of the current pattern -> elapsed time, remaining time
        :return:
        """
        greenhouse = Greenhouse()  # Greenhouse is a singleton
        return json.dumps({
            'message': {
                'desired_state': greenhouse.desired_state.to_json(),
                'elapsed_time': int(greenhouse.elapsed_time)
            },
            'success': True
        }), 200
        pass

    @staticmethod
    @app.route('/api/v1/image/', methods=['GET'])
    def api_v1_image():
        # TODO last updated should be implemented
        return json.dumps({
            'image_url': '/api/vi/image/view',
            'last_updated': '',
            'success': True
        }), 200

    @staticmethod
    @app.route('/api/v1/image/view', methods=['GET'])
    def api_v1_img_view():
        # TODO this should return the most recent image taken
        return send_file('../media/apple.jpg', mimetype='image/gif'), 200

    @staticmethod
    @app.route('/<path:path>')
    def catch_all(path):
        return json.dumps({
            'message': 'The requested endpoint could not be found on this server.',
            'success': False
        }), 404
