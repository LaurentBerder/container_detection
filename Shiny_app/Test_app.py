import matplotlib.pyplot as plot
import argparse
import yaml
import json
import numpy as np
import pandas as pd
import os
from chainercv.utils import read_image
import chainer
from chainercv.datasets import voc_bbox_label_names #voc_detection_label_names
from chainercv.links import SSD300
from chainercv import utils
from chainercv.visualizations import vis_bbox


class OriginalDetectionDataset(chainer.dataset.DatasetMixin):

    def __init__(self, data_dir, label_names):
        self.data_dir = data_dir
        self.label_names = label_names

        self.img_filenames = []
        self.anno_filenames = []
        # for name in sorted(os.listdir(data_dir)):
        for root, dirs, files in os.walk(data_dir):
            for name in sorted(files):
                # If the file is not an image, ignore the file.
                if os.path.splitext(name)[1] != '.jpg':
                    continue
                img_filename = os.path.join(root, name)
                anno_filename = os.path.splitext(img_filename)[0] + '__labels.json'
                if not os.path.exists(anno_filename):
                    continue
                self.img_filenames.append(img_filename)
                self.anno_filenames.append(anno_filename)

    def __len__(self):
        return len(self.img_filenames)

    def get_example(self, i):
        img_filename = self.img_filenames[i]
        anno_filename = self.anno_filenames[i]
        img = read_image(img_filename)

        with open(anno_filename, 'r') as f:
            anno = json.load(f)
        anno = anno['labels']

        bbox = []
        label = []
        for anno_i in anno:
            h = anno_i['size']['y']
            w = anno_i['size']['x']
            center_y = anno_i['centre']['y']
            center_x = anno_i['centre']['x']

            if anno_i['label_class'] not in self.label_names:
                raise ValueError(
                    'The class does not exist {}'.format(anno_i['label_class']))
            l = self.label_names.index(anno_i['label_class'])
            bbox.append(
                [center_y - h / 2, center_x - w / 2,
                 center_y + h / 2, center_x + w / 2])
            label.append(l)

        bbox = np.array(bbox, dtype=np.float32)
        label = np.array(label, dtype=np.int32)
        return img, bbox, label


def demo(args):
    chainer.config.train = False

    with open(args.label_names, 'r') as f:
        label_names = tuple(yaml.load(f))
    model = SSD300(
        n_fg_class=len(label_names),
        pretrained_model=args.pretrained_model)
    # Change the threshold for showing labels
    #model.score_thresh=0.4
    model.nms_thres=args.threshold

    bbox  = np.full(4, np.nan)
    label = np.full(1, np.nan).astype(int)
    score = np.full(1, np.nan)
    img = utils.read_image(args.image, color=True)
    bboxes, labels, scores = model.predict([img])
    for i, l in enumerate(labels[0]):
        if label_names[l] in ['container', 'truck', 'ship']:
            bbox  = np.vstack([bbox, bboxes[0][i]])
            label = np.append(label, int(labels[0][i]))
            score = np.append(score, scores[0][i])
    #bbox, label, score = bboxes[0], labels[0], scores[0]
    bbox  = np.array(pd.DataFrame(bbox).dropna())
    label = np.asarray([h for h in label if not h == -2147483648])
    score = np.asarray([h for h in score if not np.isnan(h)])
    nb_containers = sum([1 for l in label if label_names[int(l)] == 'container'])

    a = vis_bbox(
        img, bbox, label, score, label_names=label_names)
    a.annotate("Number of containers = {}".format(nb_containers), xytext=(0, 0), xy=(0, 0), color='green', fontsize=14)
    plot.axis('off')
    plot.savefig("./temp_result/result.png", bbox_inches='tight', interpolation="nearest")
    print("finished")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image',
        help='An image file to use for container detection')
    parser.add_argument('--pretrained_model',
                        help='The model to use for the forecast',
                        default="./Models/model_iter_245000_en_haut")
    parser.add_argument('--label_names',
        help='The path to the yaml file with label names',
        default="./Models/label_names_coco_container.yml")
    parser.add_argument('--threshold', help='The value for score_tresh, varying the confidence-based bounding boxes shown',
        default=.55)
    args = parser.parse_args()

    demo(args)



if __name__ == '__main__':
    main()
