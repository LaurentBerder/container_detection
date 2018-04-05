import cv2
import yaml
import numpy as np
import pandas as pd
import os
import argparse
import matplotlib.pyplot as plot
import chainer
from chainercv.links import SSD300
from chainercv import utils
from chainercv.visualizations import vis_bbox


def save_frames(video_file, path_in):
    cap = cv2.VideoCapture(video_file)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 1

    print("This video has {} frames".format(length), flush=True)

    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imwrite(path_in + "frame{}.jpg".format(str(count).zfill(5)), frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if count % 10 == 0:
            print("Progress: %0.2f%%" % (count / length * 100,), flush=True)
        if count == length:
            break
        count += 1

    cap.release()
    cv2.destroyAllWindows()

    return fps


def annotate(args, path_in, path_out):
    chainer.config.train = False

    with open("model/label_names_coco_container.yml", 'r') as f:
        label_names = tuple(yaml.load(f))
    model = SSD300(
        n_fg_class=len(label_names),
        pretrained_model=args.model)
    # Change the threshold for showing labels
    # model.score_thresh=0.4
    # model.nms_thres = args.threshold

    count = 1
    numfiles = len([f for f in os.listdir(path_in) if ".jpg" in f])

    for file in [f for f in os.listdir(path_in) if ".jpg" in f]:
        img = utils.read_image(path_in+file, color=True)
        bboxes, labels, scores = model.predict([img])
        bbox, label, score = bboxes[0], labels[0], scores[0]
        nb_containers = sum([1 for l in label if label_names[int(l)] == 'container'])

        a = vis_bbox(
            img, bbox, label, score, label_names=label_names)
        a.annotate("Number of containers = {}".format(nb_containers), xytext=(0, 0), xy=(0, 0))
        plot.axis('off')
        plot.savefig(path_out + "frame{}.png".format(str(count).zfill(5)), bbox_inches='tight')
        plot.close()
        if count % 10 == 0:
            print("Progress: %0.2f%%" % (count / numfiles * 100,), flush=True)
        count += 1


def make_video(path_out, outvid, fps=25, size=None, is_color=True, format="XVID"):
    """
    Create a video from a list of images.

    @param      outvid      output video
    @param      images      list of images to use in the video
    @param      fps         frame per second
    @param      size        size of each frame
    @param      is_color    color
    @param      format      see http://www.fourcc.org/codecs.php
    @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

    The function relies on http://opencv-python-tutroals.readthedocs.org/en/latest/.
    By default, the video will have the size of the first image.
    It will resize every image to this size before adding them to the video.
    """
    images = [f for f in os.listdir(path_out) if ".png" in f]
    from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
    fourcc = VideoWriter_fourcc(*format)
    vid = None
    count = 0
    for image in images:
        if not os.path.exists(path_out + image):
            raise FileNotFoundError(image)
        img = imread(path_out + image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)
        if count % 100 == 0:
            print("Progress: %0.2f%%" % (count / len(images) * 100,), flush=True)
    vid.release()
    return vid


def remove_temp_files(path):
    filelist = os.listdir(path)
    for f in filelist:
        os.remove(os.path.join(path, f))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_file', default='loading-of-a-container-ship_lowres.mp4', nargs='+')
    parser.add_argument('--model', default="./model/model_iter_568500")
    args = parser.parse_args()

    path_in = "./temp/"
    path_out = "./temp_out/"

    for file in args.video_file:
        remove_temp_files(path_in)
        remove_temp_files(path_out)
        print("\n\n######### {} ###########".format(file), flush=True)
        print("\n\n######### Saving frames ###########", flush=True)
        fps = save_frames(file, path_in)
        print("\n\n######### Annotating frames ###########", flush=True)
        annotate(args, path_in, path_out)
        print("\n\n######### Remaking video ###########", flush=True)
        result_video = make_video(path_out, '{}_annotated.avi'.format(file.split('.')[0]), fps)
        print("\n\n######### Finished creating {}_annotated.avi ###########".format(file.split('.')[0]), flush=True)
        remove_temp_files(path_in)
        remove_temp_files(path_out)        


if __name__ == '__main__':
    main()
