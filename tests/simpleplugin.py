# A demonstration plugin for ogretest that sets up a database and provides
# methods for creating objects.
# No, we don't escape the SQL, this is only a demo.
import sqlite3
from io import BytesIO

sqlite_connection = None


def get_connection(force_new=False):
    global sqlite_connection
    if force_new and sqlite_connection is not None:
        sqlite_connection.close()
        sqlite_connection = None

    if sqlite_connection is None:
        sqlite_connection = sqlite3.connect(":memory:")
    return sqlite_connection


def create_tables():
    conn = get_connection()
    conn.execute("create table user (name text, password text)")
    conn.execute("create table client (name text)")
    conn.execute("create table policy (id name, client name)")
    conn.commit()


def create_user(name, password):
    conn = get_connection()
    conn.execute("insert into user values ('%s', '%s')" % (name, password))
    conn.commit()


def create_client(name):
    conn = get_connection()
    conn.execute("insert into client values ('%s')" % name)
    conn.commit()


def create_policy(id, client):
    conn = get_connection()
    conn.execute("insert into policy values ('%s', '%s')" % (id, client))
    conn.commit()


# We include this from the generic plugin so we can test conflicts
def _print(text):
    print(text)


class OgrePlugin(object):
    name = 'simple'

    actions = {
        "Create Tables": create_tables,
        "Create User": create_user,
        "Create Client": create_client,
        "Create Insurance Policy": create_policy,
        "Print": _print,
    }

    def dump(self):
        conn = get_connection()
        out = BytesIO()
        for line in conn.iterdump():
            out.write(b'%s\n' % line.encode('UTF-8'))

        yield 'database.sql', out

    def load(self, streams):
        sqlstream = streams.pop('database.sql')
        if streams:
            # We got passed files we don't know what it is, error out
            raise ValueError("Unknown data files '%s'" % ', '.join(streams))

        # Reset connection
        conn = get_connection(force_new=True)
        conn.executescript(sqlstream.read().decode('UTF-8'))


ogre_plugin = OgrePlugin()
