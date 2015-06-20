STARS_SEARCH_URL = "https://api.github.com/search/repositories?q=stars:>={min_stars}&sort=stars"
STATS_URL = "https://api.github.com/repos/{fullname}/contributors"

STARS_DIR = 'popular_repos/'
STARS_FILENAME = "most_starred_{page}.json"

STATS_DIR = "repos_stats/"

import json
import config
from datetime import datetime
import os
import time
import requests


def get_request(url):
    return requests.get(url, auth=(config.github_username, config.github_password))

def get_repos_list(min_stars=1000):
    request_url = STARS_SEARCH_URL.format(min_stars=min_stars)
    page = 1
    while True:
        r = get_request(request_url)
        if r.status_code == 200:
            with open(STARS_DIR+STARS_FILENAME.format(page=page), 'w') as f:
                print(page)
                f.write(r.text)
            if 'next' in r.links:
                request_url = r.links['next']['url']
                page = r.links['next']['url'].split('=')[-1]
                time.sleep(1)
            else:
                break
        else:
            print(r.headers)
            print(r.content)
            break

def get_repos_stats():
    search_files = os.listdir(STARS_DIR)
    search_files = list(zip(*sorted(map(lambda x: (int(x.split('_')[-1].split('.')[0]), x), search_files))))[1]

    repos = set()
    for sf in search_files:
        with open(STARS_DIR+sf) as f:
            search_res = json.load(f)
            for r in search_res['items']:
                repos.add(r['full_name'])

    done_repos = set(map(lambda x: x.replace('?', '/'), os.listdir(STAT_DIRS)))

    print("total", len(repos))
    print("done", len(done_repos))

    for repo in repos - done_repos:
        print(repos)
        break
        r = get_request(STATS_URL.format(fullname=repo))
        while r.status_code == 202:
            time.sleep(1)
            r = get_request(STATS_URL.format(fullname=repo))

        if r.status_code == 200:
            print(repo[0])
            with open(STATS_DIR+repo.replace('/','?'), 'w') as f:
                f.write(r.text)
        elif r.status_code == 403:
            reset_time = datetime.fromtimestamp(int(r.headers['X-RateLimit-Reset']))
            now = datetime.now()
            wait_delay = (reset_time - now).total_seconds()
            print("sleep", wait_delay)
            time.sleep(wait_delay)
        else:
            print(STATS_URL.format(fullname=repo))
            print(r.status_code)
            print(r.content)
        time.sleep(1)

if __name__ == '__main__': get_repos_stats()
