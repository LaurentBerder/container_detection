# Container detection Shiny app

This is a Shiny application for detection of containers in photos. 
This application is inspired by [Road2stat's application](https://github.com/road2stat/imgsvd/) and uses a model based on [ChainerCV's implementation of SSD](https://github.com/chainer/chainercv/tree/master/examples/ssd),
trained on [COCO Dataset](http://cocodataset.org/) and manually labeled data for the containers.

![App]()

## Preparation

To run this Shiny app locally, install the following R packages first:

```r
install.packages(c("shiny", "markdown", "rARPACK", "jpeg", "png"))
```

```python
pip install -r ../requirements.txt
```

## Play with it
Just use:

```r
shiny::runapp("")
```
