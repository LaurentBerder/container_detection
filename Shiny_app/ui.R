library("shiny")
library("markdown")

shinyUI(fluidPage(

  title = "Detecting containers: counting containers in images",
  theme = "bootstrap.min.css",

  # css hacks for responsive images
  tags$head(tags$style(
    type="text/css",
    "#original_image img {max-width: 100%; width: 100%; height: auto}"
  )),

  tags$head(tags$style(
    type="text/css",
    "#output_image img {max-width: 100%; width: 100%; height: auto}"
  )),

  titlePanel(title=div(img(src="https://ih0.redbubble.net/image.512525295.6965/flat,800x800,075,f.jpg"), "Container Recognition Artificial Neuralnetwork GUI (CRANG)")),

  tags$hr(),

  fluidRow(
    column(
      width = 6,
      h4("Upload a picture"),
      tags$hr(),
      fileInput("file1", "Upload a PNG or JPEG image:")
    )
  ),

  tags$hr(),

  fluidRow(
    column(
      width = 6,
      h4("Original picture"),
      tags$hr(),
      imageOutput("original_image", height = "auto")),
    column(
      width = 6,
      h4("Detection"),
      tags$hr(),
      imageOutput("output_image", height = "auto")
    )
  ),

  tags$hr(),

  fluidRow(
    column(
      width = 12,
      includeMarkdown("footer.md")
    )
  )

))
