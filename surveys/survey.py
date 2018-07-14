from surveys.db.models import Survey


def create(name, available_places, user):
    survey = Survey()

    survey.name = name
    survey.available_places = available_places
    survey.user = user

    survey.save()


def list_surveys():
    return Survey.objects

