import mongoengine


def startup():
    mongoengine.register_connection(alias='main', name='surveys', host='mongo')
