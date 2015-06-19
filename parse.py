import json

with open('sqlmap.json') as f:
    stats = json.load(f)

contributors = dict()

for s in stats:
    c = s['author']['login']
    lines = sum(f['a'] + f['d'] for f in s['weeks'])
    contributors[c] = lines

print(contributors)
