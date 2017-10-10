ui <- fluidPage(
  headerPanel("Crude Mortality Rate"),
  sidebarPanel(
    checkboxGroupInput(inputId = "national",
                       label = "Choose national",
                       choices = 'NATIONAL'),
    checkboxGroupInput(inputId = "state",
                       label = "Choose state",
                       choices =as.character(unique(cmr$State))),
    checkboxGroupInput(inputId = "disease",
                       label = "Choose disease", 
                       choices = as.character(unique(cmr$ICD.Chapter)))
  ),
  mainPanel(
    plotOutput("line")
  )
)
