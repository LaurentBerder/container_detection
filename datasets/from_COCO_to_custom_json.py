import json
import yaml
import os
import argparse
from shutil import copyfile


def transform_json(args, selected_categories):
    with open(args.COCO_annotation_file, 'r') as f:
        coco = json.load(f)

    results = dict((l, 0) for l in selected_categories)
    copied_files = 1

    for annotation in coco['annotations']:
        # only keep the annotations we're interested in
        this_annot = [cat['name'] for cat in coco['categories'] if cat['id'] == annotation['category_id']][0]
        if this_annot not in selected_categories:
            continue
        results[this_annot] += 1

        filename = [image['file_name'] for image in coco['images'] if image['id'] == annotation['image_id']][0]
        print(filename + ",           " + str(copied_files) + " files")
        print(results)
        json_filename = filename.split('.')[0] + '__labels.json'
        bbox = annotation['bbox']

        # If the file doesn't exist, it's the first time we encounter it so we create the json and copy the image
        if filename not in os.listdir(args.custom_annotation_folder):
            copyfile(args.COCO_image_folder + filename, args.custom_annotation_folder + filename)
            copied_files += 1
            img = {'image_filename': filename, 'complete': False,
                   'labels': [
                       {'label_type': 'box', 'object_id': 1, 'label_class': this_annot,
                        'centre': {'x': bbox[0] + (bbox[2]/2), 'y': bbox[1] + (bbox[3]/2)},
                        'size': {'x': bbox[2], 'y': bbox[3]}}
                   ]}
            with open(args.custom_annotation_folder + json_filename, 'w') as output:
                json.dump(img, output)


        # If the file already exists, it has been copied, so we add info to the json
        else:
            with open(args.custom_annotation_folder + json_filename, 'r') as f:
                img = json.load(f)
            img['labels'].append({
                'label_type': 'box', 'object_id': 1, 'label_class': this_annot,
                'centre': {'x': bbox[0] + (bbox[2] / 2), 'y': bbox[1] + (bbox[3] / 2)},
                'size': {'x': bbox[2], 'y': bbox[3]}
            })
            with open(args.custom_annotation_folder + json_filename, 'w') as output:
                json.dump(img, output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--COCO_annotation_file', help='The COCO annotation file downloaded from COCO website')
    parser.add_argument('--COCO_image_folder', help='The COCO photos folder downloaded from COCO website')
    parser.add_argument('--labels', help='The yaml file where the list of classes is saved')
    parser.add_argument('--custom_annotation_folder', help='The folder in which json files are saved')
    args = parser.parse_args()

    with open(args.labels, 'r') as f:
        selected_categories = list(yaml.load(f))
    transform_json(args, selected_categories)


if __name__ == '__main__':
    main()
