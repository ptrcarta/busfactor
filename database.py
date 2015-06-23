import config
import psycopg2
from datetime import datetime


projects_table = """
CREATE TABLE project (
id SERIAL PRIMARY KEY,
full_name TEXT NOT NULL,
last_updated TIMESTAMP,
bus_factor INTEGER,
UNIQUE (full_name)
);
"""
contributors_table = """
CREATE TABLE contributor (
project_id INTEGER NOT NULL,
login TEXT NOT NULL,
adds FLOAT,
deletes FLOAT,
commits FLOAT,
FOREIGN KEY (project_id) REFERENCES project(id),
CONSTRAINT adds_ratios CHECK ((adds BETWEEN 0 AND 1) OR adds = NULL),
CONSTRAINT dels_ratios CHECK ((deletes BETWEEN 0 AND 1) OR deletes = NULL),
CONSTRAINT commits_ratios CHECK ((commits BETWEEN 0 AND 1) OR commits = NULL)
);
"""

CONN = psycopg2.connect(config.database_config)

def init_db():
    cur = CONN.cursor()
    cur.execute(projects_table)
    cur.execute(contributors_table)
    CONN.commit()

def new_project(project_name):
    cur = CONN.cursor()
    cur.execute("SELECT id FROM project WHERE full_name =  %s", (project_name,))
    if cur.fetchone() is not None:
        raise Exception('project already in db')
    cur.execute("INSERT INTO project (full_name) VALUES (%s)", (project_name,))
    cur.execute("SELECT id FROM project WHERE full_name =  %s", (project_name,))
    return cur.fetchone()

def dataframe_to_db(contributors, project_name):
    """insert a df of contributors into the database"""

    """needs more modularity"""
    cur = CONN.cursor()
    cur.execute("SELECT id FROM project WHERE full_name =  %s", (project_name,))
    project = cur.fetchone()
    if project is None:
        project = new_project(project_name)
    for c in contributors.to_records():
        cur.execute("""INSERT INTO contributor (project_id, login, adds, deletes,
        commits) VALUES (%s, %s, %s, %s, %s)""",
            (project[0], c['author'], c['a'], c['d'], c['c']))
    cur.execute("""
    UPDATE project SET
    (last_updated, bus_factor) = (%s, %s)
    WHERE id = %s;
    """, (datetime.now(), len(contributors), project[0])) #time of data not time now!
    CONN.commit()
