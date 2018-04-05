# Labeling videos

After testing on still images, I moved on to videos.

Since the model is quite slow (2-3 seconds per image), the labeling cannot be done real-time, and has to be done frame by frame, so I save temporary files which I clean afterwards when the resulting video is created.

```bash
python label_video video_file 01.avi 02.avi
```
This creates the corresponding *01_annotated.avi* and *02_annotated.avi* files

The process takes about 30 minutes for a 2 minutes clip.
