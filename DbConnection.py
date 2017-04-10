import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

USER = 'anystring'
DBNAME = 'test1'
PASSWORD = ''
TABLE = 'invitees'


class DbManager:
    def __init__(self):
        try:
            conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)

        except psycopg2.OperationalError:
            raise RuntimeError('Wrong DB credentials, check configuration.')

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()

    def fetch_user(self, name, email):
        self.cursor.execute(
            "SELECT * FROM {table} WHERE email = '{email}' AND invitee = '{name}' LIMIT 1;".format(table=TABLE,
                                                                                                   email=email,
                                                                                                   name=name))
        return self.cursor.fetchall()

    def get_users(self, name='', email=''):
        self.cursor.execute(
            "SELECT * FROM {table} WHERE email ~ '{email}' OR invitee ~ '{name}';".format(table=TABLE,
                                                                                          email=email,
                                                                                          name=name))

        return self.cursor.fetchall()

    def delete_user(self, name, email):
        self.cursor.execute(
            "DELETE FROM {table} WHERE email = '{email}' AND invitee = '{name}';".format(table=TABLE,
                                                                                         email=email,
                                                                                         name=name))

    def create_user(self, name, email):
        self.cursor.execute("INSERT INTO {table} VALUES ('{name}', '{email}')".format(table=TABLE, name=name,
                                                                                      email=email))
        return self.fetch_user(name, email)

    def update_user(self, name, email):
        self.cursor.execute("SELECT count(*) FROM {table} WHERE invitee = '{name}';".format(table=TABLE, name=name))
        names = int(self.cursor.fetchall()[0][0])

        self.cursor.execute("SELECT count(*) FROM {table} WHERE email = '{email}';".format(table=TABLE, email=email))
        emails = int(self.cursor.fetchall()[0][0])

        if emails + names > 1:
            self.cursor.execute(
                "SELECT * FROM {table} WHERE email = '{email}' OR invitee = '{name}';".format(table=TABLE,
                                                                                              email=email,
                                                                                              name=name))
            conflicts = self.cursor.fetchall()

            raise NameError(
                "Conflicting invitee data, DELETE conflicting users: {conflicts}".format(conflicts=conflicts))

        elif names > emails:
            self.cursor.execute("UPDATE {table} SET email = '{email}' WHERE invitee = '{name}';".format(table=TABLE,
                                                                                                        email=email,
                                                                                                        name=name))

        elif emails > names:
            self.cursor.execute("UPDATE {table} SET invitee = '{name}' WHERE email = '{email}';".format(table=TABLE,
                                                                                                        email=email,
                                                                                                        name=name))
        else:
            return self.create_user(name, email)

        return self.fetch_user(name, email)

