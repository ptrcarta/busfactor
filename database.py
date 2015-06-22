import config
import psycopg2


projects_table = """
CREATE TABLE project (
id INTEGER PRIMARY KEY,
full_name TEXT NOT NULL,
total_commits INTEGER,
last_updated TEXT,
bus_factor INTEGER
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
CONSTRAINT ratios CHECK ((adds BETWEEN 0 AND 1) AND (deletes BETWEEN 0 AND 1) AND (commits BETWEEN 0 AND 1))
);
"""

CONN = psycopg2.connect(config.database_config)

def init_db():
    cur = CONN.cursor()
    cur.execute(projects_table)
    cur.execute(contributors_table)
    cur.commit()

def dataframe_to_db(contributors, project):
    """insert a df of contributors into the database"""
    cur = CONN.cursor()
    pass
