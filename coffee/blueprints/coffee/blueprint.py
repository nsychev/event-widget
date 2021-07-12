import flask


coffee = flask.Blueprint(
    'coffee',
    __name__,
    url_prefix='/teaching/os/coffee/'
)
