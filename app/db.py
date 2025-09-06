import os
os.environ["CASSANDRA_DRIVER_EVENT_LOOP"] = "asyncio"

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
from cassandra.cqlengine import connection
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent

CONNECT_BUNDLE = BASE_DIR / "unencrypted" / "astradb_connect.zip"

def get_session():
    cloud_config= {
    'secure_connect_bundle': CONNECT_BUNDLE
    }

    with open("app/astradb_token/astradb_token.json") as f:
        secrets = json.load(f)

    CLIENT_ID = secrets["clientId"]
    CLIENT_SECRET = secrets["secret"]

    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))

    return session
