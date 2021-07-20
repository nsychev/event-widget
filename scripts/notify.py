#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback

import flask
import telegram

from sqlalchemy.orm import contains_eager

from coffee.app import create_app
from coffee.storage.models import Event, Reservation, Section, User

MESSAGE = "You have an active reservation."


def main():
    app = create_app()

    with app.test_request_context() as _:
        app.preprocess_request()
        bot = telegram.Bot(app.config['TELEGRAM']['token'])

        for user in (flask.g.db.query(User)
                     .join(Reservation, User.reservations)
                     .join(Section, Reservation.section)
                     .join(Event, Section.event)
                     .filter(Event.available == True)
                     .options(
                         contains_eager(User.reservations),
                         contains_eager(User.reservations, Reservation.section),
                         contains_eager(User.reservations, Reservation.section, Section.event)
                     )
                     .order_by(User.id.asc(), Reservation.name.asc())
                     .all()):
            message = MESSAGE + "\n"

            for reservation in user.reservations:
                message += f"- {reservation.section.name}, {reservation.name}\n"

            try:
                bot.send_message(
                    chat_id=user.telegram_id,
                    text=message
                )
            except:
                print("Can't send message to", user.telegram_id, file=sys.stderr)
                traceback.print_exc()


if __name__ == "__main__":
    main()
