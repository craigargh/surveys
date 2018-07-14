from flask import Flask, request

from surveys import survey, survey_response
from surveys.db import mongo_connection

app = Flask(__name__)

mongo_connection.startup()


@app.route('/surveys', methods=['GET'], strict_slashes=False)
def surveys():
    all_surveys = survey.list_surveys()

    return all_surveys.to_json()


@app.route('/surveys', methods=['POST'], strict_slashes=False)
def create_survey():
    request_data = request.form

    name = request_data.get('name')
    available_places = request_data.get('available_places')
    user = request_data.get('user')

    survey.create(name, available_places, user)

    return 'Success', 200


@app.route('/survey_responses', methods=['POST'], strict_slashes=False)
def create_survey_response():
    request_data = request.form

    survey_id = request_data.get('survey')
    user_id = request_data.get('user')

    try:
        survey_response.create(survey_id, user_id)
    except ValueError as survey_response_error:
        return str(survey_response_error), 400

    return 'Success', 200


app.run()
