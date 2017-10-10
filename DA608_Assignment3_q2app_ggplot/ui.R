ui <- fluidPage(
  headerPanel("Crude Mortality Rate"),
  sidebarPanel(
    selectInput(inputId = "disease",
                label = "Choose disease", 
                choices = unique(cmr$ICD.Chapter),
                selected = "Neoplasms"),
    selectInput(inputId = "year",
                label = "Choose year", 
                choices = unique(cmr$Year),
                selected = 1999)
  ),
  mainPanel(
    plotOutput("bar")
    
  )
)