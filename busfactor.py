STARS_DIR = 'popular_repos/'
LW_STARS_DIR = 'linewise/'
STARS_FILENAME = "most_starred_{page}.json"

STATS_DIR = "repos_stats/"

import api
import json
from datetime import datetime
import os
import time


def get_repos_stats():
    search_files = os.listdir(STARS_DIR)
    search_files = list(zip(*sorted(map(lambda x: (int(x.split('_')[-1].split('.')[0]), x), search_files))))[1]

    repos = set()
    for sf in search_files:
        with open(STARS_DIR+sf) as f:
            search_res = json.load(f)
            for r in search_res['items']:
                repos.add(r['full_name'])

    done_repos = set(map(lambda x: x.replace('?', '/'), os.listdir(STATS_DIR)))
    lw_done_repos = set(map(lambda x: x.replace('?', '/'), os.listdir(STATS_DIR+LW_STATS_DIR)))

    print("total", len(repos))
    print("done", len(done_repos))

    for repo in repos - done_repos:
        download_contributors_stats(repo)

    for repo in repos - lw_done_repos:
        download_linewise_stats(repo)

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

if __name__ == '__main__': get_repos_stats()
