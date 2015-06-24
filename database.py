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

contribution_table = """
CREATE TABLE contribution (
project_id INTEGER NOT NULL,
user_id INTEGER NOT NULL,
adds FLOAT,
deletes FLOAT,
commits FLOAT,
FOREIGN KEY (project_id) REFERENCES project(id),
FOREIGN KEY (user_id) REFERENCES user(id),
CONSTRAINT adds_ratios CHECK ((adds BETWEEN 0 AND 1) OR adds = NULL),
CONSTRAINT dels_ratios CHECK ((deletes BETWEEN 0 AND 1) OR deletes = NULL),
CONSTRAINT commits_ratios CHECK ((commits BETWEEN 0 AND 1) OR commits = NULL)
);
"""

user_table = """
CREATE TABLE user (
id SERIAL PRIMARY KEY,
login TEXT
);
"""


CONN = psycopg2.connect(config.database_config)

def init_db():
    cur = CONN.cursor()
    cur.execute(projects_table)
    cur.execute(contributors_table)
    CONN.commit()

def new_user(user_name):
    cur = CONN.cursor()
    cur.execute("SELECT id FROM user WHERE login =  %s", (user_name,))
    res = cur.fetchone() 
    if res is not None:
        return res
    cur.execute("INSERT INTO user (login) VALUES (%s)", (user_name,))
    cur.execute("SELECT id FROM project WHERE full_name =  %s", (user_name,))
    return cur.fetchone()

def new_project(project_name):
    cur = CONN.cursor()
    cur.execute("SELECT id FROM project WHERE full_name =  %s", (project_name,))
    res = cur.fetchone() 
    if res is not None:
        return res
    cur.execute("INSERT INTO project (full_name) VALUES (%s)", (project_name,))
    cur.execute("SELECT id FROM project WHERE full_name =  %s", (project_name,))
    return cur.fetchone()

def dataframe_to_db(contributors, project_name):
    """insert a df of contributors into the database"""

    """needs more modularity"""
    cur = CONN.cursor()

    cur.execute("SELECT id FROM user WHERE login =  %s", (c['author'],))
    author = cur.fetchone()
    if author is None:
        author = new_user(c['author'])

    cur.execute("SELECT id FROM project WHERE full_name =  %s", (project_name,))
    project = cur.fetchone()
    if project is None:
        project = new_project(project_name)

    for c in contributors.to_records():
        cur.execute("""INSERT INTO contribution (project_id, user_id, adds, deletes,
        commits) VALUES (%s, %s, %s, %s, %s)""",
            (project[0], author[0], c['a'], c['d'], c['c']))

    cur.execute("""
    UPDATE project SET
    (last_updated, bus_factor) = (%s, %s)
    WHERE id = %s;
    """, (datetime.now(), len(contributors), project[0])) #time of data not time now!
    CONN.commit()
