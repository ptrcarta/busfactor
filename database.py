import sqlite3
import config

CONN = sqlite3.connect(config.db_file)

def create_schema():
    projects_table = """
    CREATE TABLE project (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    total_commits INTEGER,
    last_updated TEXT
    );
    """
    contributors_table = """
    CREATE TABLE contribution (
    project_id INTEGER NOT NULL,
    login TEXT NOT NULL,
    adds INTEGER,
    deletes INTEGER,
    commits INTEGER,
    contributions INTEGER
    FOREIGN KEY (project_id) REFERENCES project(id)
    );
    """

    cursor = CONN.cursor()
    cursor.execute(projects_table)
    cursor.execute(contributors_table)
    cursor.commit()
