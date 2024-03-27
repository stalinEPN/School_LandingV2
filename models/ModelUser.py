from .entities.User import User
from database.db import get_connection
from flask import flash
from psycopg2 import IntegrityError

class ModelUser():

    @classmethod
    def login(self, user):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = """Select id, username, password, correo from users
                     where username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
        except IntegrityError as ex:
            raise IntegrityError(ex)
        except Exception as ex:
            raise Exception(ex)
 
    @classmethod
    def get_by_id(self, id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = """Select id, username, correo from users
                     where id = '{}'""".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    