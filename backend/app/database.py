import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable

from .config import DB_PATH


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                lat REAL NOT NULL,
                lon REAL NOT NULL,
                valid_time TEXT,
                nwp_rainfall REAL NOT NULL,
                regime TEXT NOT NULL,
                correction REAL NOT NULL,
                corrected_rainfall REAL NOT NULL
            )'''
        )
        conn.commit()
        yield conn
    finally:
        conn.close()


def save_predictions(results: Iterable[dict], created_at: str) -> None:
    with get_db() as conn:
        conn.executemany(
            '''INSERT INTO predictions
               (created_at, lat, lon, valid_time, nwp_rainfall, regime, correction, corrected_rainfall)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            [
                (
                    created_at,
                    r['latitude'], r['longitude'], r['valid_time'],
                    r['nwp_rainfall_mm'], r['predicted_regime'],
                    r['predicted_correction_mm'], r['corrected_rainfall_mm']
                )
                for r in results
            ]
        )
        conn.commit()


def recent_predictions(limit: int = 50):
    limit = max(1, min(int(limit), 500))
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            '''SELECT id, created_at, lat, lon, valid_time,
                      nwp_rainfall, regime, correction, corrected_rainfall
               FROM predictions ORDER BY id DESC LIMIT ?''',
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
