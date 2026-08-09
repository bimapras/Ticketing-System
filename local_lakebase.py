import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def lakebase_url():
    return os.environ["LAKEBASE_URL"]


@contextmanager
def get_connection():
    conn = psycopg2.connect(
        lakebase_url(),
        cursor_factory=RealDictCursor
    )

    try:
        yield conn
    finally:
        conn.close()


def run_query(sql: str, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
        
def run_write(sql: str, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            if cur.description:
                result = cur.fetchone()
            else:
                result = cur.rowcount
            conn.commit()
            return result
        
def run_transaction(queries):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                results = []

                for sql, params in queries:
                    cur.execute(sql, params)

                    if cur.description:
                        results.append(cur.fetchone())
                    else:
                        results.append(cur.rowcount)

            conn.commit()
            return results

        except Exception:
            conn.rollback()
            raise