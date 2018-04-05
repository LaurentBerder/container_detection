# SSD Example


This example provides following functionalities.

+ (Annotating dataset for detection task. This is the functionality supported by image-labelling-tool.)
+ A data loader object that wraps annotated data, and conveniently access data using Python.
+ A SSD training script that works with the data loader.


### Dependency

+ `chainer`
+ `chainercv>=0.6`


### Process
1. Annotate dataset (please read the [README](https://github.com/yuyu2172/image-labelling-tool) in the top of this repo)

Please store all image data below `DATA_DIR`. The label names should be writtein in a YAML file locating at `LABEL_NAME`.
The file extension of the images can be selected by `EXT` (e.g. jpg).

After finish annotating data,
the annotation files are stored umder `DATA_DIR` together with the images.

```bash
$ python flask_app.py --image_dir DATA_DIR --label_names LABEL_FILE --file_ext EXT
```

2. Train SSD

This script assumes data stored in the annotation style of this annotation tool.
Thanks to that, you do not need to write any data loader code by yourself.

```bash
$ python train.py --train DATA_DIR --label_names LABEL_NAMES --gpu GPU
```

More on `train.py`.
```bash
$ python train.py -h
```


### Dividing a dataset into train/val
When calling `train.py` without supplying `--val`, the dataset is split into two with ratio 8:2.
The larger one is used as the training dataset and the smaller one is used as the validation dataset.

There can be a situation when the train/val split should be fixed.
You can use fixed split during training by supplying both `--train` and `--val` when calling `train.py`.

In order to split data in fixed manner, there is a convenient script `randomly_split_directory.py`.
This script divides all data in `DATA_DIR` into `TRAIN_DIR` and `VAL_DIR`.

```bash
$ python randomly_split_directory.py TRAIN_DIR VAL_DIR DATA_DIR
```


### Example

In order to try these scripts without annotating images, sample annotations are provided.
Each annotation contains a bounding box around an orange or an apple.
It can be downloaded from here.
https://drive.google.com/open?id=0BzBTxmVQJTrGek9ISlNmU2RkTk0

For annotating your own dataset, please read https://github.com/yuyu2172/image-labelling-tool

##### Unzip the compressed file.
```bash
$ git clone https://github.com/yuyu2172/image-labelling-tool
$ cd image-labelling-tool/examples/ssd
# Download the file in the current directory.
$ unzip apple_orange_annotations.zip
```

##### Run train code
```bash
$ python train.py --train apple_orange_annotations --label_names apple_orange_annotations/apple_orange_label_names.yml --val_iteration 100 --gpu GPU
```

For environments with a less powerful GPU, please reduce computational demand by setting `--batchsize` to a lower value than the default one.
For those who are worried that nothing appears, please pass `--batchsize 1` and `--log_iteration 1` to the command.
This will make the script to report log for every image.

Python's `multiprocessing` works badly with OpenCV in some environments ([dicussion](https://github.com/chainer/chainercv/issues/386#issuecomment-321485827)).
In that case, please set `--loaderjob 0`.
This will make the script to use `SerialIterator` instead of `MultiprocessingIterator`.

##### Alternatively, fix data used for validation
[description](https://github.com/yuyu2172/image-labelling-tool/tree/master/examples/ssd#dividing-dataset-into-trainval)
```bash
$ python randomly_split_directory.py train val apple_orange_annotations
$ python train.py --train train --val val --label_names apple_orange_annotations/apple_orange_label_names.yml --val_iteration 100  --gpu GPU
```

##### Demo code to visualize output

```bash
$ python demo.py --pretrained_model result/model_iter_400 --label_names apple_orange_annotations/apple_orange_label_names.yml apple_orange_annotations/Orange/frame0017.jpg
```

Here is a link to a weight trained for 400 iterations.
[model_iter_400](https://drive.google.com/file/d/0B8QTag5ixHD3NWVGN3FVZHVHdFU/view?usp=sharing)
