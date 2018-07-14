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
        survey.save()

        survey_response.create(survey.id, 1234)

        result = Survey.objects().first()

        self.assertEqual(1, len(result.responses))

    def test_create_survey_response_sets_user_id(self):
        survey = Survey()
        survey.save()

        survey_response.create(survey.id, 1234)

        result = Survey.objects().first()

        self.assertEqual(1234, result.responses[0].user)

    def test_create_survey_response_sets_created_at(self):
        survey = Survey()
        survey.save()

        survey_response.create(survey.id, 1234)

        result = Survey.objects().first()

        self.assertEqual(datetime.datetime, type(result.responses[0].created_at))
