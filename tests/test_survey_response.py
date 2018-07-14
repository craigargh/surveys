import datetime
from unittest import TestCase

import mongoengine

from surveys import survey_response
from surveys.db.models import Survey


class TestSurveyResponse(TestCase):
    def setUp(self):
        mongoengine.register_connection(alias='main', host='mongomock://localhost')

    def tearDown(self):
        Survey.objects().delete()

    def test_create_survey_response_is_inserted_into_the_database(self):
        survey = Survey()
        survey.available_places = 1
        survey.save()

        survey_response.create(survey.id, 1234)

        result = Survey.objects().first()

        self.assertEqual(1, len(result.responses))

    def test_create_survey_response_sets_user_id(self):
        survey = Survey()
        survey.available_places = 1
        survey.save()

        survey_response.create(survey.id, 1234)

        result = Survey.objects().first()

        self.assertEqual(1234, result.responses[0].user)

    def test_create_survey_response_sets_created_at(self):
        survey = Survey()
        survey.available_places = 1
        survey.save()

        survey_response.create(survey.id, 1234)

        result = Survey.objects().first()

        self.assertEqual(datetime.datetime, type(result.responses[0].created_at))

    def test_create_survey_response_throws_exception_when_reached_max_responses(self):
        survey = Survey()
        survey.available_places = 2
        survey.save()

        survey_response.create(survey.id, 1234)
        survey_response.create(survey.id, 5678)

        with self.assertRaises(ValueError) as max_responses_error:
            survey_response.create(survey.id, 91011)

        self.assertEqual('The maximum number (2) of survey responses has been reached', str(max_responses_error.exception))

    def test_create_survey_responses_throws_exception_when_user_answers_same_survey_twice(self):
        survey = Survey()
        survey.available_places = 10
        survey.save()

        survey_response.create(survey.id, 1234)

        with self.assertRaises(ValueError) as user_error:
            survey_response.create(survey.id, 1234)

        self.assertEqual('User 1234 has already completed survey', str(user_error.exception))

    def test_create_survey_responses_checks_for_duplicate_user_when_user_id_is_string(self):
        survey = Survey()
        survey.available_places = 10
        survey.save()

        survey_response.create(survey.id, 1234)

        with self.assertRaises(ValueError) as user_error:
            survey_response.create(survey.id, "1234")

        self.assertEqual('User 1234 has already completed survey', str(user_error.exception))
