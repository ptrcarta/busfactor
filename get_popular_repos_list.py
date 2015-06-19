import requests
import time

STATS_URL = "https://api.github.com/repos/{username}/{project}/stats/contributors"
STARS_SEARCH_URL = "https://api.github.com/search/repositories?q=stars:>={min_stars}&sort=stars"

STARS_FILENAME = "most_starred_{page}.json"

request_url = STARS_SEARCH_URL.format(min_stars=1000)
page = 1

while True:
    r = requests.get(request_url)
    if r.status_code == 200:
        with open('popular_repos/'+STARS_FILENAME.format(page=page), 'w') as f:
            print(page)
            f.write(r.text)
        if 'next' in r.links:
            request_url = r.links['next']['url']
            page = r.links['next']['url'].split('=')[-1]
            time.sleep(6) # 6 requests per minute :(
        else:
            break
    else:
        print(r.headers)
        print(r.content)
        break
