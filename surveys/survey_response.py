from surveys.db.models import Survey, SurveyResponse


def create(survey_id, user_id):
    survey_response = SurveyResponse()
    survey_response.user = user_id

    survey = Survey.objects(id=survey_id).first()
    survey.responses.append(survey_response)

    survey.save()
