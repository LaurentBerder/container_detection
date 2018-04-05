# Dataset

You'll only find here a few samples of the custom-labeled photos to see their format.

I combined the labeled images with COCO images to decrease False Positives.

## Scripts

+ check_labels_in_json.py

    To make sure that i didn't forget to label any of the bounding boxes during the labeling process, I ran this script each time I finished. It returns the name of json files that contain null-labeled boxes.
+ from_COCO_to_custom_json.py

    Once you've downloaded and uncompressed the [COCO datasets](http://cocodataset.org/#download), run this script to translate the labels to the same format that the one used by the manual labeling tool, and copy the concerned image files to the same folder. This uses the label YAML file to only select the files containing the type of objects that you want to use for training.
+ category_reduction.py

    Manually labeling images is very tedious, so I unhappily wasn't able to do it over thousands of images. This resulted in a class imbalance between the object I was really aiming to detect (containers) and the objects existing in COCO. So I used this script to remove some of the COCO data in order to get a better balance.
+ downsize_all.py
    
    Some of the images I wanted to use for testing were too large (resulting in a memory error during test), I set a maximum size and made sure none exceeded that size.
