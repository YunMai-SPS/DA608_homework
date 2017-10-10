suppressWarnings(suppressMessages(library(shiny)))
suppressWarnings(suppressMessages(library(dplyr)))
suppressWarnings(suppressMessages(library(plotly)))

cmr<-read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv")
cmr2 <- mutate_if(cmr,is.factor, as.character) %>% 
  group_by(Year,ICD.Chapter) %>% 
  summarize(nation.rate = 10^5*(sum(as.numeric(Deaths))/sum(as.numeric(Population)))) %>% 
  mutate(State = "NATIONAL") %>% 
  dplyr::rename(Crude.Rate=nation.rate) %>% 
  as.data.frame()

cmr3 <- select(cmr,ICD.Chapter,Year,Crude.Rate,State) %>% 
  mutate_if(is.factor, as.character) %>% 
  as.data.frame()

cmr_nat <- rbind(cmr2,cmr3)
cmr_nat$fill <- with(cmr_nat, ifelse(State == 'Nat', 1,0))

server <- function(input,output){
  filterData <- reactive({
    cmrSlice <- cmr_nat %>% 
      filter(ICD.Chapter %in% input$disease & State %in% c(input$state,input$national)) %>% 
      transform(State = reorder(State, Crude.Rate))
  })
  output$line <- renderPlot({
    plot_ly(filterData(), x = ~Year, y = ~Crude.Rate, type = 'scatter', mode = 'lines+markers',color = ~State) %>% 
      layout(title = input$disease)
  })
}
