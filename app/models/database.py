import os
import sqlite3
from pathlib import Path

DATABASE_PATH_ENV = os.getenv("DATABASE_PATH")
DATABASE_URL_ENV = os.getenv("DATABASE_URL")

def _resolve_db_path():
    if DATABASE_PATH_ENV:
        path = DATABASE_PATH_ENV
    elif DATABASE_URL_ENV:
        
        if DATABASE_URL_ENV.startswith("sqlite:///"):
            path = DATABASE_URL_ENV.replace("sqlite:///", "", 1)
        elif DATABASE_URL_ENV.startswith("sqlite:////"):
            path = DATABASE_URL_ENV.replace("sqlite:////", "/", 1)
        else:
            path = DATABASE_URL_ENV
    else:
        path = os.path.join(os.getcwd(), "registro-civil-prueba.db")

    p = Path(path).expanduser().resolve()
    return str(p)

DATABASE_NAME = _resolve_db_path()


def _ensure_parent_dir_exists(db_path_str):
    
    p = Path(db_path_str)
    parent = p.parent
    if not parent.exists():
        try:
            parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"No se pudo crear la carpeta padre {parent}: {e}") from e


def get_db_connection():
    _ensure_parent_dir_exists(DATABASE_NAME)

    try:
        conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.OperationalError as e:
        raise sqlite3.OperationalError(f"Error con la DB en '{DATABASE_NAME}': {e}") from e


def execute_query(query, params=None):
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        conn.commit()
    finally:
        cur.close()
        conn.close()


def fetch_all(query, params=None):
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        rows = cur.fetchall()
        result = [dict(row) for row in rows]
        return result
    finally:
        cur.close()
        conn.close()


def fetch_one(query, params=None):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        cur.close()
        conn.close()
