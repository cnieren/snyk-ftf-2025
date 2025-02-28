import json

filename = 'mountains.json'
mountains = dict()

with open(filename, 'r') as filep:
    raw_mountains = json.load(filep)
    for m in raw_mountains:
        mountains[m['name']] = { 'height': int(m['height'].replace(',', '')), 'first': m['first'] }
        

one = mountains['Tongshanjiabu']
result = str(one['height']) + ',' + one['first']
print(result)