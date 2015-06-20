import json
import config
from datetime import datetime
import os
import time
import requests

STATS_URL = "https://api.github.com/repos/{fullname}/contributors"

search_files = os.listdir('popular_repos')
search_files = list(zip(*sorted(map(lambda x: (int(x.split('_')[-1].split('.')[0]), x), search_files))))[1]


repos = set()
for sf in search_files:
    with open('popular_repos/'+sf) as f:
        search_res = json.load(f)
        for r in search_res['items']:
            repos.add(r['full_name'])

done_repos = set(map(lambda x: x.replace('?', '/'), os.listdir('repos_stats')))

print("total", len(repos))
print("done", len(done_repos))

for repo in repos - done_repos:
    print(repos)
    break
    r = requests.get(STATS_URL.format(fullname=repo))
    if r.status_code == 403:
        reset_time = datetime.fromtimestamp(int(r.headers['X-RateLimit-Reset']))
        now = datetime.now()
        wait_delay = (reset_time - now).total_seconds()
        print("sleep", wait_delay)
        time.sleep(wait_delay)
    if r.status_code == 202:
        time.sleep(1)
        r = requests.get(STATS_URL.format(fullname=repo))
    if r.status_code == 200:
        print(repo[0])
        with open("repos_stats/"+repo.replace('/','?'), 'w') as f:
            f.write(r.text)
    else:
        print(STATS_URL.format(fullname=repo))
        print(r.status_code)
        print(r.headers)
        print(r.content)
    time.sleep(1)
