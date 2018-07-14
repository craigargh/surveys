from surveys.db.models import Survey, SurveyResponse


def create(survey_id, user_id):
    survey = Survey.objects(id=survey_id).first()
    validate(survey, user_id)

    survey_response = SurveyResponse()
    survey_response.user = user_id

    survey.responses.append(survey_response)

    survey.save()


def validate(survey, user_id):
    if not len(survey.responses) < survey.available_places:
        raise ValueError(f'The maximum number ({survey.available_places}) of survey responses has been reached')

    if int(user_id) in respondents(survey):
        raise ValueError(f'User {user_id} has already completed survey')


def respondents(survey):
    return {
        response.user
        for response in survey.responses
    }
