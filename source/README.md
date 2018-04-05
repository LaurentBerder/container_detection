This is where the main scripts are.


##### Label
```bash
cd container_detection/source/
python flask_app.py --image_dir ../Datasets/train/ --label_names label_names_coco_container.yml --file_ext jpg
```
This launches the GUI that scans the image directory and lets you draw bounding boxes around objects. The result is a json file is created for each image with the corresponding coordinates and labels.

##### Train
```bash
cd container_detection/source/
nohup python examples/ssd/train.py --train ../datasets/train/ --lr 0.0001 --step_size 100000  --val ../datasets/validation/ \
      --label label_names_coco_container.yml  --out models/ --gpu 0 --loaderjob 10 --iteration 1000000 --val_iteration 1000 &
```
This launches the training process, with a rather large learning rate, which decreases every 100K iterations, and with validations every 1000 iterations. Iterations load is distributed over 10 processes, and it uses the GPU to increase speed.

##### Test
```bash 
cd container_detection/source/
python examples/ssd/demo.py --label_names label_names_coco_container.yml --gpu 0 --pretrained_model models/model_iter_3000 \
      Test_images/01.jpg
```
This allows you to see the result of the models on a single image.

##### Videos
```bash
cd container_detection/source/Video/
python label_video.py --video_file 01.avi
```
This labels a full video frame by frame and saves the result.
