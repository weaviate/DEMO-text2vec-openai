import json

f = open('data/movies.json')
data = json.load(f)

for movie in data[:10]:
    print(movie["Title"])