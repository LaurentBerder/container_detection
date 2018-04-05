#################################################
###### Make sure R packages are installed: ######
#################################################
# list.of.packages <- c("shiny", "markdown", "rARPACK", "jpeg", "png")
# new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
# if(length(new.packages)) install.packages(new.packages)

#######################################################
####### Make sure Python packages are installed: ######
#######################################################
# system("pip install -r requirements.txt")

library("shiny")
library("rARPACK")
library("jpeg")
library("png")


shinyServer(function(input, output) {

  lst = list()

  run_svd = reactive({

    imgtype = input$file1$type

    if (is.null(imgtype)) {
      inFile1 = "demo.jpg"
      imgtype = "image/jpeg"
    } else {
      if (!(imgtype %in% c("image/jpeg", "image/png"))) {
        stop("Only JPEG and PNG images are supported")
      }
      inFile1 = input$file1$datapath

      command_line = paste('python ./Models/Test_app.py --image', input$file1$datapath)
      retour_fonction = system(command_line, wait=T)
      retour_fonction
    }

    is_jpeg  = imgtype == "image/jpeg"

    rawimg = (if (is_jpeg) jpeg::readJPEG else png::readPNG)(inFile1)

    #lst = factorize(rawimg, 100)

    return(lst)

  })

  do_recovery = reactive({

    imgtype = input$file1$type

    if (is.null(imgtype)) {
      imgtype = "image/jpeg"
    } else {
      if (!(imgtype %in% c("image/jpeg", "image/png"))) {
        stop("Only JPEG and PNG images are supported")
      }
    }

    is_jpeg = imgtype == "image/jpeg"

    #outfile2 = tempfile(fileext = ifelse(is_jpeg, ".jpg", ".png"))
    #(if (is_jpeg) jpeg::writeJPEG else png::writePNG)(image = m, target = outfile2, 1)

    outfile2 = "./temp_result/result.png"

    return(list("out" = outfile2))

  })

  output$original_image = renderImage({

    lst <<- run_svd()
    list(
      src = if (is.null(input$file1)) "demo.jpg" else input$file1$datapath,
      title = "Original Image")

  }, deleteFile = TRUE)

  output$output_image = renderImage({

    # lst = writeSVD()
    result = do_recovery()

    list(
      src = if (is.null(input$file1)) "wait.gif" else result$out,
      title = paste("Detected containers")
    )

  }, deleteFile = FALSE)

})

