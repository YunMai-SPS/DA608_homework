suppressWarnings(suppressMessages(library(shiny)))
suppressWarnings(suppressMessages(library(dplyr)))
suppressWarnings(suppressMessages(library(plotly)))

df<-read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv")
df2 <- mutate_if(df,is.factor, as.character) %>% 
  group_by(Year,ICD.Chapter) %>% 
  summarize(nation.rate = 10^5*(sum(as.numeric(Deaths))/sum(as.numeric(Population)))) %>% 
  mutate(State = "NATIONAL") %>% 
  dplyr::rename(Crude.Rate=nation.rate) %>% 
  as.data.frame()

df3 <- select(df,ICD.Chapter,Year,Crude.Rate,State) %>% 
  mutate_if(is.factor, as.character) %>% 
  as.data.frame()

df_nat <- rbind(df2,df3)
df_nat$fill <- with(df_nat, ifelse(State == 'Nat', 1,0))

server <- function(input,output){
  filterData <- reactive({
    dfSlice <- df_nat %>% 
      filter(ICD.Chapter %in% input$disease & State %in% c(input$state,input$national)) %>% 
      transform(State = reorder(State, Crude.Rate))
  })
  output$line <- renderPlot({
    plot_ly(filterData(), x = ~Year, y = ~Crude.Rate, type = 'scatter', mode = 'lines+markers',color = ~State)
  })
}
