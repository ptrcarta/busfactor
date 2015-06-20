import api
import database
import json
from datetime import datetime
import os
import time
import pandas as pd

STARS_DIR = 'popular_repos/'

LW_STATS_DIR = 'linewise/'
STATS_DIR = "repos_stats/"


def load_search_result(results_dir):
    search_files = os.listdir(results_dir)
    search_files = list(zip(*sorted(map(lambda x: (int(x.split('_')[-1].split('.')[0]), x), search_files))))[1]
    repos_list = []
    for sf in search_files:
        with open(results_dir+sf) as f:
            search_res = json.load(f)
        for i in search_res['items']:
            yield i

def load_stats_files(repo):
    repo = repo.replace("/", "?")
    cont_file = STATS_DIR + repo
    lw_file = STATS_DIR + LW_STATS_DIR + repo
    with open(cont_file) as f:
        contributors = json.load(f)
    with open(lw_file) as f:
        lw_contributors = json.load(f)
    return {'contributors':contributors, 'linewise':lw_contributors}


def parse_stats():
    """parse the linewise results and create a single json out of them"""

    """very slow because of json decoding / file reading"""
    stats_files = os.listdir(STATS_DIR+LW_STATS_DIR)
    projects = []
    for s in stats_files:
        proj = []
        with open(STATS_DIR+LW_STATS_DIR+s) as f:
            stats = json.load(f)
        for contributor in stats:
            author = contributor['author'] 
            author = author['login'] if author is not None else None
            total = contributor['total']
            bigl = ((i["a"], i["c"], i["d"]) for i in contributor['weeks'])
            a, c, d = zip(*bigl)
            a = sum(a)
            c = sum(c)
            d = sum(d)
            proj.append(dict(author=author, total=total, a=a, c=c, d=d))
        projects.append({'project':s.replace('?','/'), 'contributors':proj})

    with open('aggregated_stats2.json', 'w') as f:
        json.dump(projects, f, indent=4)

def get_stats_dataframes()
    with open('aggregated_stats2.json', 'w') as f:
        stats = json.load(f)
    projects = dict()
    for s in stats:
        projects[s['project']] = pd.Dataframe(s['contributors'])
    return projects

if __name__ == '__main__': parse_stats()
