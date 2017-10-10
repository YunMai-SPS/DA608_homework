ui <- fluidPage(
  headerPanel("Crude Mortality Rate"),
  sidebarPanel(
    selectInput(inputId = "disease",
                label = "Choose disease", 
                choices = unique(cmr$ICD.Chapter),
                selected = 1999)
  ),
  mainPanel(
    plotOutput("bar")
  )
)
