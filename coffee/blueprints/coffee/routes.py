import flask

from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.exc import NoResultFound

from ...storage.models import Event, Section, Reservation, User
from . import utils
from .blueprint import coffee
from .forms import RegistrationForm


@coffee.route('/')
def main():
    if flask.g.user is None:
        return flask.render_template('telegram.html')

    event = (flask.g.db.query(Event)
             .filter(Event.available == True)
             .join(Section, Event.sections, isouter=True)
             .join(Reservation, Section.reservations, isouter=True)
             .filter(Reservation.user_id == None)
             .options(
                 contains_eager(Event.sections),
                 contains_eager(Event.sections, Section.reservations)
             )
             .order_by(Section.id.asc(), Reservation.name.asc())
             .one())

    return flask.render_template(
        'main.html',
        event=event
    )


@coffee.route('/callback')
def callback():
    print(flask.request.headers, flush=True, file=__import__('sys').stderr)
    if not utils.verify(flask.request, flask.current_app.config['TELEGRAM']['token']):
        return flask.abort(400)

    telegram_id = int(flask.request.args['id'])
    try:
        user = (flask.g.db.query(User)
                .filter(User.telegram_id == telegram_id)
                .one())

        flask.session['user_id'] = user.id
        return flask.redirect(
            flask.url_for('coffee.main'),
            code=303
        )
    except NoResultFound:
        flask.session['telegram_id'] = telegram_id

        return flask.redirect(
            flask.url_for('coffee.register'),
            code=303
        )


@coffee.route('/register', methods=['GET', 'POST'])
def register():
    if 'telegram_id' not in flask.session:
        return flask.abort(400)

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            telegram_id=flask.session['telegram_id'],
            name=form.name.data,
        )
        flask.g.db.add(user)
        flask.g.db.commit()
        flask.session['user_id'] = user.id
        return flask.redirect(
            flask.url_for('coffee.main'),
            code=303
        )

    return flask.render_template('register.html', form=form)


@coffee.route('/logout')
def logout():
    flask.session.pop('user_id', None)
    return flask.redirect(flask.url_for('coffee.main'), code=303)


@coffee.route('/book/<int:reservation_id>', methods=['GET', 'POST'])
def book(reservation_id):
    if flask.g.user is None:
        return flask.render_template('telegram.html')

    reservation = (flask.g.db.query(Reservation)
                   .filter(Reservation.id == reservation_id)
                   .join(Section, Reservation.section, isouter=True)
                   .join(Event, Section.event, isouter=True)
                   .options(
                        contains_eager(Reservation.section),
                        contains_eager(Reservation.section, Section.event)
                   )
                   .one())

    if reservation.user_id is not None:
        return flask.render_template('denied.html'), 409

    if flask.request.method == 'POST':
        reservation.user_id = flask.g.user.id
        flask.g.db.add(reservation)
        flask.g.db.commit()

        return flask.redirect(
            flask.url_for('coffee.main'),
            code=303
        )

    return flask.render_template(
        'confirmation.html',
        reservation=reservation
    )


@coffee.route('/cancel/<int:reservation_id>')
def cancel(reservation_id):
    if flask.g.user is None:
        return flask.render_template('telegram.html')

    reservation = (flask.g.db.query(Reservation)
                   .filter(Reservation.id == reservation_id)
                   .join(Section, Reservation.section, isouter=True)
                   .options(
                        contains_eager(Reservation.section)
                   )
                   .one())

    if reservation.user_id != flask.g.user.id:
        return flask.render_template('denied_cancel.html'), 403


    reservation.user_id = None
    flask.g.db.add(reservation)
    flask.g.db.commit()

    return flask.redirect(
        flask.url_for('coffee.main'),
        code=303
    )
