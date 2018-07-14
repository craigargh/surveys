from unittest import TestCase

import mongoengine

from surveys import survey
from surveys.db.models import Survey


class TestSurvey(TestCase):
    def setUp(self):
        mongoengine.register_connection(alias='main', host='mongomock://localhost')

    def tearDown(self):
        Survey.objects.delete()

    def test_create_survey_saves_document_to_database(self):
        survey.create('test_survey', 12, '63')

        result = Survey.objects()

        self.assertEqual(1, len(result))

    def test_create_survey_sets_survey_name(self):
        survey.create('test_survey', 12, 63)

        saved_survey = Survey.objects().first()

        self.assertEqual('test_survey', saved_survey.name)

    def test_create_survey_sets_available_places(self):
        survey.create('test_survey', 12, 63)

        saved_survey = Survey.objects().first()

        self.assertEqual(12, saved_survey.available_places)

    def test_create_survey_sets_user_id(self):
        survey.create('test_survey', 12, 63)

        saved_survey = Survey.objects.first()

        self.assertEqual(63, saved_survey.user)

    def test_list_surveys_returns_all_surveys(self):
        first_survey = Survey()
        first_survey.name = 'First Survey'

        second_survey = Survey()
        second_survey.name = 'Second Survey'

        Survey.objects.insert(
            [first_survey, second_survey]
        )

        result = survey.list_surveys()

        self.assertEqual(2, len(result))

        self.assertEqual('First Survey', result[0].name)
        self.assertEqual('Second Survey', result[1].name)
