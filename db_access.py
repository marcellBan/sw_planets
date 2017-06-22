import os
import sys
import datetime
import psycopg2
import urllib
from psycopg2.extras import DictCursor


class CredentialsMissingError(Exception):
    pass


class DatabaseError(Exception):
    pass


def db_connection(function):
    def wrapper(*args, **kwargs):
        _db_connection = None
        _cursor = None
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
        try:
            _db_connection = conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
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


@db_connection
def get_statistics(cursor=None):
    query = '''
            SELECT planet_id, COUNT(*) AS votes
              FROM "planet-votes"
              GROUP BY planet_id
              ORDER BY planet_id;
            '''
    if cursor is None:
        print('No database cursor.', file=sys.stderr)
        raise psycopg2.DatabaseError()
    cursor.execute(query)
    return cursor.fetchall()
