# Computer vision: 
# Object Detection to detect and count specific objects (shipping containers) from images and/or videos

This project is based on ChainerCV API and [Single Shot MultiBox Detector](https://github.com/chainer/chainercv/tree/master/examples/ssd) algorithm.
The dataset used for training is a mix of COCO dataset and manually labeled images (using [yuyu21's tool](https://github.com/yuyu2172/image-labelling-tool)). The reason for this is that my first attempt, using only my labeled images, was very effective in terms of *True Positives*, but was also generating lots of *False Positives*, so I had to enrich the datasets for some negative mining.

## Labeling
Labeling is done throug the graphical interface (using QT) with the command:
```bash
python flask_app.py --image_dir "path_to_images" --label_names "label_names_coco_container.yml" --file_ext jpg
```

## Training
I have been using a RedHat 7.4 server with a GPU (Tesla) for the training, and have gone through 500K+ iterations, with validation every 1K and decreased learning rate every 100K.

Training is done with the command:

```bash
python examples/ssd/train.py --train "path_to_training_set"   --lr 0.0001 --step_size 100000  --val "path_to_validation_set"   --label label_names_coco_container.yml    --out models/ --gpu 0 --loaderjob 10   --iteration 1000000 --val_iteration 1000
```

## Test on images
I created a Shiny app for the application of the model, which calls a python program to display side by side the original image and the result:

![shiny_demo](https://github.com/LaurentBerder/container_detection/blob/master/shiny_demo.png "Shiny app")

## Test on videos
I've also downloaded a few clips of videos and labeled them. Since the model used is not very fast, it can't be used real time (detection takes a couple seconds per images).

So the script captures all the frames, then labels each of them, and reconstructs the video from the label frames:

```bash
python Video/label_video.py --video_file "path_to_video(s)_to_labelize"
```

# Results
![Result_video](https://github.com/LaurentBerder/container_detection/blob/master/video_result.gif "Result video")
