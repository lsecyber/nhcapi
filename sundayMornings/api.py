import traceback

import flask
from flask import Flask
from flask_restful import Resource, Api, request
import pandas as pd
import ast

from werkzeug.datastructures import Headers

import sundaymornings

app = Flask(__name__)
api = Api(app)


class SundayMornings(Resource):
    def get(self):
        try:
            step = request.args.get('step')
            result = sundaymornings.runStep(step)

            if not result:
                data = {'success': 'False'}
                response = flask.make_response(data)
                response.status_code = 500
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            else:
                data = {'success': 'True',
                        'output': str(result)}
                response = flask.make_response(data)
                response.status_code = 200
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
        except Exception as e:
            print('Error: ' + str(e))
            traceback.print_exc()
            data = {'success': 'False',
                    'output': str(e)}
            response = flask.make_response(data)
            response.status_code = 500
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response


api.add_resource(SundayMornings, '/api')

if __name__ == '__main__':
    app.run(port=5555, debug=False)
