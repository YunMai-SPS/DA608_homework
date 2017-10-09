suppressWarnings(suppressMessages(library(shiny)))
suppressWarnings(suppressMessages(library(dplyr)))
suppressWarnings(suppressMessages(library(ggplot2)))

df<-read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv")

server <- function(input,output){
  filterData <- reactive({
    dfSlice <- df %>% 
      filter(Year== 2010,ICD.Chapter ==as.character(input$disease)) %>% 
      transform(State = reorder(State, Crude.Rate))
  })
  output$bar <- renderPlot({
    ggplot(filterData(),aes(x = State, y = Crude.Rate))+ 
      geom_bar(stat = "identity")+
      coord_flip()
  })
}