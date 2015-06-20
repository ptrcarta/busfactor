import requests
import config
import logging

logger = logging.getLogger(__name__)

STARS_SEARCH_URL = "https://api.github.com/search/repositories?q=stars:>={min_stars}&sort=stars"
STATS_URL = "https://api.github.com/repos/{fullname}/contributors"
LW_STATS_URL = "https://api.github.com/repos/{fullname}/stats/contributors"

def _request(url):
    return requests.get(url, auth=(config.github_username, config.github_password))


def _get(url, items_q, list_node=None):
    logger.info("querying API on url: %s" %url)
    r = _request(url)
    while r.status_code == 202:
        time.sleep(1)
        r = _request(url)
    if r.status_code == 200:
        if list_node:
            items_q.extend(r.json[list_node])
        else:
            items_q.extend(r.json)
        else:
        time.sleep(1)
        if 'links' in r.headers:
            if 'next' in r.links:
                _get(r.links['next']['url'], items_q)

    elif r.status_code == 403:
        reset_time = datetime.fromtimestamp(int(r.headers['X-RateLimit-Reset']))
        now = datetime.now()
        wait_delay = (reset_time - now).total_seconds()
        logger.info("sleeping %s seconds" % wait_delay)
        time.sleep(wait_delay)
        _get(url, items_q)
    else:
        logger.error("%d while requesting: %s, returned message %s" %(
            r.status_code,
            STATS_URL.format(fullname=repo),
            r.content))
        time.sleep(1)

def contributors_stats(repo):
    contributors_list = []
    url = STATS_URL.format(fullname=repo)
    _get(url, contributors_list)
    return contributors_list

def linewise_stats(repo):
    lw_list = []
    url = STATS_URL.format(fullname=repo)
    _get(url, lw_list)
    return lw_list

def repos_list(min_stars=1000):
    repos_list = []
    url = STARS_SEARCH_URL.format(min_stars=min_stars)
    _get(url, repos_list, list_node='items')
    return repos_list
