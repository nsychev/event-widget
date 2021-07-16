import functools

import flask


def require_authorization(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if (flask.request.headers.get('authorization', None) !=
                f'Basic {flask.current_app.config.get("ADMIN_CREDENTIALS", "!")}'):
            return flask.Response(
                "<h1>Access forbidden</h1>",
                401,
                {'WWW-Authenticate': 'Basic realm="Please proceed to the customs"'}
            )

        return func(*args, **kwargs)

    return inner
