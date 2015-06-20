import api
import database
import json
from datetime import datetime
import os
import time

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
        repos_list.extend(search_res['items'])
    return repos_list

def load_stats_files(repo):
    cont_file = STATS_DIR + repo
    lw_file = STATS_DIR + LW_STATS_DIR + repo
    with open(cont_file) as f:
        contributors = json.load(f)
    with open(lw_file) as f:
        lw_contributors = json.load(f)
    return {'contributors':contributors, 'linewise':lw_contributors}


def parse_stats():
    stats_files = os.listdir(STATS_DIR)
    projects = dict()
    for s in stats_files:
        with open(STATS_DIR+s) as f:
            stats = json.load(f)
            contributions = dict((cont['login'], cont['contributions']) for cont in stats)
            projects[s.replace('?','/')] = contributions
    with open('aggregated_stats.json', 'w') as f:
        json.dump(projects, f, indent=2)
