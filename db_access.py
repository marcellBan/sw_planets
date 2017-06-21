import os
import sys
import datetime
import psycopg2
from psycopg2.extras import DictCursor


class CredentialsMissingError(Exception):
    pass


class DatabaseError(Exception):
    pass


def db_connection(function):
    def wrapper(*args, **kwargs):
        _db_connection = None
        _cursor = None
        connection_data = {
            'dbname': os.environ.get('MY_PSQL_DBNAME'),
            'user': os.environ.get('MY_PSQL_USER'),
            'host': os.environ.get('MY_PSQL_HOST'),
            'password': os.environ.get('MY_PSQL_PASSWORD')
        }
        # if environment values are missing raise exception
        if any(map(lambda x: x is None, connection_data.values())):
            print('Database credentials are missing!', file=sys.stderr)
            raise CredentialsMissingError()
        connect_string = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
        connect_string = connect_string.format(**connection_data)
        try:
            _db_connection = psycopg2.connect(connect_string, cursor_factory=DictCursor)
            _db_connection.autocommit = True
            _cursor = _db_connection.cursor()
            result = function(*args, **kwargs, cursor=_cursor)
        except psycopg2.DatabaseError as e:
            print('Database error occured:', file=sys.stderr)
            print(e, file=sys.stderr)
            raise DatabaseError()
        finally:
            if _cursor is not None:
                _cursor.close()
            if _db_connection is not None:
                _db_connection.close()
        return result
    return wrapper


@db_connection
def get_user(username, cursor=None):
    query = '''
            SELECT * FROM users
              WHERE username = %s;
            '''
    if cursor is None:
        print('No database cursor.', file=sys.stderr)
        raise psycopg2.DatabaseError()
    cursor.execute(query, [username])
    return cursor.fetchone()


@db_connection
def add_user(username, password, cursor=None):
    query = '''
            INSERT INTO users (username, password)
              VALUES (%s, %s);
            '''
    if cursor is None:
        print('No database cursor.', file=sys.stderr)
        raise psycopg2.DatabaseError()
    cursor.execute(query, [username, password])


@db_connection
def add_vote(user_id, planet_id, cursor=None):
    query = '''
            INSERT INTO "planet-votes" (planet_id, user_id, submission_time)
              VALUES (%s, %s, %s);
            '''
    if cursor is None:
        print('No database cursor.', file=sys.stderr)
        raise psycopg2.DatabaseError()
    cursor.execute(query, [planet_id, user_id, datetime.datetime.now()])
