import os
import json
import argparse

 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', help='The folder to scan')
    args = parser.parse_args()
    
    directory = os.chdir(args.directory)
    list = os.listdir(directory)

    for l in list:
        if 'json' in l:
            data = json.loads(open(l).read()).get('labels')
            labels = [d.get('label_class') for d in data]
            if None in labels:
                print(l)
