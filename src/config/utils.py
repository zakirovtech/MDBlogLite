from typing import Dict

import psycopg2
from psycopg2 import OperationalError


def is_postgres_available(credentials: Dict) -> bool:
    try:
        conn = psycopg2.connect(
            dbname=credentials.get("NAME"),
            user=credentials.get("USER"),
            password=credentials.get("PASSWORD"),
            host=credentials.get("HOST"),
            port=credentials.get("PORT", "5432"),
            connect_timeout=2
        )
        conn.close()
        return True
    except OperationalError as e:
        print(e)
        return False
