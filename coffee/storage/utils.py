from contextlib import contextmanager

import flask
import sqlalchemy

from .models import Base


def create_database_tables(db_engine):
    def inner():
        Base.metadata.create_all(db_engine)
    return inner


def establish_database_connection(database):
    def inner():
        flask.g.db = database()
    return inner


def teardown_database(exc: Exception = None):
    database = flask.g.pop('db')
    if exc is None:
        database.commit()
    else:
        database.rollback()


def get_engine(config):
    return sqlalchemy.create_engine(config['DATABASE_URL'])


def install_database(app):
    db_engine = get_engine(app.config)
    db_factory = sqlalchemy.orm.sessionmaker(bind=db_engine)
    database = sqlalchemy.orm.scoped_session(db_factory)

    app.before_first_request(create_database_tables(db_engine))
    app.before_request(establish_database_connection(database))
    app.teardown_appcontext(teardown_database)


@contextmanager
def get_standalone_session(config):
    db_engine = get_engine(config)
    db_factory = sqlalchemy.orm.sessionmaker(bind=db_engine, expire_on_commit=False)
    create_database_tables(db_engine)()

    session = db_factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
