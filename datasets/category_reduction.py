import json
import yaml
import os
import argparse
from shutil import copyfile


def find_class(args):
    inv = []
    for file in (os.listdir(args.dataset_folder)):
        # only look for COCO annotation files
        if '__labels.json' not in file or 'COCO' not in file:
            continue
        with open(args.dataset_folder+file, 'r') as f:
            coco = json.load(f)
        this_file = {'label_file': file, 'photo_file': file.split('__labels')[0]+'.jpg', 'count': 0}
        for annotation in coco['labels']:
            if annotation['label_class'] == args.category:
                this_file['count'] += 1
        if this_file['count'] >= 1:
            inv.append(this_file)
    return inv


def delete_files(args, inventory):
    current = sum(item['count'] for item in inventory)
    count = 0
    for file in inventory:
        if current < args.number:
            break
        os.remove(args.dataset_folder+file['label_file'])
        os.remove(args.dataset_folder+file['photo_file'])
        current -= file['count']
        count += 1
    print("{} files were deleted containing the category {}".format(count, args.category))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--category', help='The name of the category to reduce')
    parser.add_argument('--dataset_folder', help='The COCO folder where photos and json files are located')
    parser.add_argument('--number', type=int, help='The final required number of representations for the given class')
    args = parser.parse_args()

    inventory = find_class(args)
    print("number of boxes: ", sum(item['count'] for item in inventory))
    print("number of files: ", len(inventory))
    delete_files(args, inventory)


if __name__ == '__main__':
    main()
