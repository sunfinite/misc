"""Transfer volunteer attendance information from Google docs to Podio"""
from pypodio2 import api
from client_info import *
import csv
import time

csv_file = '/home/skatkuri/attendance.csv'
def normalize(string):
    return string.lower().replace(' ', '').replace('.', '')
# The items that we want to add are attendance info for each volunteer
# for a given Sunday.
c = api.OAuthClient(client_id, client_token, email, password)
# The app that we want to add items to has a reference to another app 
# which lists the volunteer names. 
# So first get all the item_ids for all volunteer names
name_item_id_map = {}
app_names = []
items = c.Item.filter(13024238, {'limit': 42})
for item in items['items']:
    normalized_name = normalize(item['title'])
    app_names.append(normalized_name)
    name_item_id_map[normalized_name] = item['item_id']

# Attendance information until now has been collected via a 
# google form which I exported to a csv
r = csv.reader(open(csv_file, 'rU'))
headers = r.next()

# we have to now map the names from the csv to item ids fetched above
# but the csv had a text field for names and not a drop-down
# so i had to manually clean it up (somewhat tedious) 
lines = list(r)
csv_map = {}
for line in lines:
    name = normalize(line[1])
    csv_map.setdefault(name, []).append((line[2], line[3]))
    
csv_names = map(lambda x: normalize(x[1]), lines)
print ("These names in the Google form are not in Podio: "
       "%s" % str(set(csv_names) - set(app_names)))
print ("These names in Podio do not have entries in the Google form: "
       "%s" % str(set(app_names) - set(csv_names)))

for name in csv_map:
    try:
        item_id = name_item_id_map[name] 
    except KeyError:
        continue
    for row in csv_map[name]:
        t = time.strptime(row[0].strip(), "%m/%d/%Y")
        date = time.strftime('%Y-%m-%d %H:%M:%S', t)
        feedback = row[1] if row[1] else ' '
        c.Item.create(13024297, {'fields': {
            'teacher-name': name_item_id_map[name], 
            'date': date,
            'attendance': 'Present', 
            'feedback-things-to-remember-from-this-day': feedback}}
        )
