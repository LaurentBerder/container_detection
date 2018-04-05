import os
import json

directory = os.chdir("train/")
list = os.listdir(directory)

for l in list:
    if 'json' in l:
        data = json.loads(open(l).read()).get('labels')
        labels = [d.get('label_class') for d in data]
        if None in labels:
            print(l)
            
