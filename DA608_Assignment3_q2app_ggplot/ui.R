ui <- fluidPage(
  headerPanel("Crude Mortality Rate"),
  sidebarPanel(
    selectInput(inputId = "disease",
                label = "Choose disease", 
                choices = unique(df$ICD.Chapter),
                selected = "Neoplasms"),
    selectInput(inputId = "year",
                label = "Choose year", 
                choices = unique(df$Year),
                selected = 1999)
  ),
  mainPanel(
    plotOutput("bar")
    
  )
)