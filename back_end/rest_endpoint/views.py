from flask import Flask
from flask import request
from flask import send_file
import json
from back_end.greenhouse.greenhouse import Greenhouse
from typing import Tuple
import os
from functools import reduce


class RestEndpoint(object):
    app = Flask(__name__)

    def __init__(self):
        pass

    @staticmethod
    @app.route('/')
    def root():
        return json.dumps({
            'message': 'This is a UNBC precision farm.',
            'endpoints': ['/api'],
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
        greenhouse = Greenhouse()
        if request.method == 'POST':
            if greenhouse.change_pattern(request.json):
                greenhouse.pattern = request.json
                return json.dumps({
                    'message': 'New Pattern Accepted',
                    'success': True
                }), 200
            return json.dumps({
                'message': 'Pattern format is incorrect',
                'success': False
            }), 400
        else:
            return json.dumps({
                'message': greenhouse.pattern,
                'success': True
            }), 200

    @staticmethod
    @app.route('/api/v1/status/', methods=['GET', 'POST'])
    def api_v1_status():
        """
        This endpoint returns various reporting information. Examples of this are:
            - Progress of the current pattern -> elapsed time, remaining time
        :return:
        """
        greenhouse = Greenhouse()  # Greenhouse is a singleton
        if request.method == 'POST':
            if 'time_offset' in request.json and greenhouse.offset_time(request.json['time_offset']):
                return json.dumps({
                    'message': 'Offset updated by' + str(request.json['time_offset']),
                    'success': True
                }), 200
            return json.dumps({
                'message': 'The POSTed data is incorrect.',
                'success': False
            }), 400
        return json.dumps({
            'message': {
                'desired_state': greenhouse.desired_state.to_json(),
                'elapsed_time': int(greenhouse.elapsed_time),
                'recipe_length': greenhouse.get_pattern_time_length(),
                'start_time': int(greenhouse.start_time)
            },
            'success': True
        }), 200
        pass

    @staticmethod
    def _get_newest_image_name_and_filepath_and_timestamp(media_dir: str = './media/webcam') -> Tuple[str, str, int]:
        """
        This function searches the webcam media directory for the newest webcam snapshot. It naively assumes that the
        file name will be the timestamp of when it was taken in unix time. If the directory is empty it will raise a
        FileNotFoundError.
        :param media_dir: The media directory to search for the webcam snapshots.
        :return: This function returns a three tuple of: The filename, the absolute filepath, the timestamp from the
        file
        """
        abs_folder_path = os.path.abspath(media_dir)
        files_list = [f for f in os.listdir(abs_folder_path) if os.path.isfile(os.path.join(abs_folder_path, f))]

        newest_file = \
            reduce(
                lambda x, y: x if
                int(x.split('.')[0]) - max(int(x.split('.')[0]), int(y.split('.')[0])) == 0 else y,
                files_list, '-1.jpg')

        if newest_file is -1:
            raise FileNotFoundError

        return newest_file, os.path.join(abs_folder_path, newest_file), int(newest_file.split('.')[0])

    @staticmethod
    @app.route('/api/v1/image/', methods=['GET'])
    def api_v1_image():
        """
        This endpoint returns metadata about the most recent image that the farm has taken.
        """
        _, _, timestamp = RestEndpoint._get_newest_image_name_and_filepath_and_timestamp()
        return json.dumps({
            'image_url': '/api/v1/image/view',
            'last_updated': timestamp,
            'success': True
        }), 200

    @staticmethod
    @app.route('/api/v1/image/view', methods=['GET'])
    def api_v1_img_view():
        """
        This endpoint returns the most recent image literal that the farm has taken.
        """
        _, newest_filepath, _ = RestEndpoint._get_newest_image_name_and_filepath_and_timestamp()
        return send_file(newest_filepath, mimetype='image/jpeg'), 200

    @staticmethod
    @app.route('/<path:path>')
    def catch_all(path):
        return json.dumps({
            'message': 'The requested endpoint could not be found on this server.',
            'success': False
        }), 404
