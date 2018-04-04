# Computer vision: 
# Object Detection to detect and count specific objects (shipping containers) from images and/or videos

This project is based on ChainerCV API and [Single Shot MultiBox Detector](https://github.com/chainer/chainercv/tree/master/examples/ssd) algorithm.
The dataset used for training is a mix of COCO dataset and manually labeled images (using [yuyu21's tool](https://github.com/yuyu2172/image-labelling-tool)).

## Labeling
Labeling is done throug the graphical interface (using QT) with the command:
*python flask_app.py --image_dir "path_to_images" --label_names "label_names_coco_container.yml" --file_ext jpg*

## Training
I have been using a RedHat 7.4 server with a GPU (Tesla) for the training, and have gone through 500K+ iterations, with validation every 1K and decreased learning rate every 100K.

Training is done with the command:

*nohup python examples/ssd/train.py --train "path_to_training_set"   --lr 0.0001 --step_size 100000  --val "path_to_validation_set"   --label label_names_coco_container.yml    --out models/ --gpu 0 --loaderjob 10   --iteration 1000000 --val_iteration 1000 &*

## Test
I created a Shiny app for the application of the model, which calls a python program to display side by side the original image and the result:
![shiny_demo](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
