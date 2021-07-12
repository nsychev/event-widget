import flask

from sqlalchemy.orm import contains_eager

from ...storage.models import User, Reservation, Section
from .blueprint import coffee


@coffee.before_app_request
def process_session():
    if 'user_id' in flask.session:
        flask.g.user = (flask.g.db.query(User)
                        .filter(User.id == flask.session['user_id'])
                        .join(Reservation, User.reservations, isouter=True)
                        .join(Section, Reservation.section, isouter=True)
                        .options(
                            contains_eager(User.reservations),
                            contains_eager(User.reservations, Reservation.section)
                        )
                        .one_or_none())
    else:
        flask.g.user = None


@coffee.app_context_processor
def inject_template():
    return {
        'user': flask.g.user,
        'telegram_bot_username': flask.current_app.config['TELEGRAM']['username']
    }
