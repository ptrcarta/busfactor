import json
import os
import time
import requests

STATS_URL = "https://api.github.com/repos/{fullname}/stats/contributors"

search_files = os.listdir('popular_repos')
search_files = list(zip(*sorted(map(lambda x: (int(x.split('_')[-1].split('.')[0]), x), search_files))))[1]


repos = list()
for sf in search_files:
    with open('popular_repos/'+sf) as f:
        search_res = json.load(f)
        for r in search_res['items']:
            repos.append((r['full_name'], r['stargazers_count']))

for repo in repos:
    r = requests.get(STATS_URL.format(fullname=repo[0]))
    if r.status_code == 202:
        time.sleep(0.5)
        r = requests.get(STATS_URL.format(fullname=repo[0]))
    if r.status_code == 200:
        print(repo[0])
        with open("repos_stats/"+repo[0].replace('/','?'), 'w') as f:
            f.write(r.text)
        time.sleep(6)
    else:
        print(r.status_code)
        print(r.headers)
        print(r.content)
