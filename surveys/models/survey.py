import mongoengine

from surveys.models.survey_response import SurveyResponse


class Survey(mongoengine.Document):
    name = mongoengine.StringField()
    available_places = mongoengine.IntField()
    user = mongoengine.IntField()

    responses = mongoengine.EmbeddedDocumentListField(SurveyResponse)

    meta = {
        'db_alias': 'main',
        'collection': 'surveys',
    }
