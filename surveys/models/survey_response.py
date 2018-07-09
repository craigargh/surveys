import datetime

import mongoengine


class SurveyResponse(mongoengine.EmbeddedDocument):
    survey = mongoengine.ObjectIdField()
    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    user = mongoengine.IntField()

    meta = {
        'db_alias': 'main',
        'collection': 'survey_responses',
    }