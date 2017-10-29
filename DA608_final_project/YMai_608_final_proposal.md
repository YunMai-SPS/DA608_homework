DATA608 Final Project Proposal
================
Yun Mai
Oct 21, 2017

Project Proposal
----------------

### 1.Introduction

Yelp is a social-local platform which collected sizable data from it's 135 million monthly reviews. These data will provide valuable insight for the business owners like how they and their competitors are doing with their business, what customers like, what is the reason they come back, what is the factors that help in improving their business, and what factors have negative impacts etc.

### 2. Goal

This the final project for the Knowledge and Visual Analytics course as part of the CUNY DATA Science master degree. In this project, I will use the data to address the following questions:

1.  The reviewer's check-in time reflects the number of the customers visiting the restaurant. I will create graphs of the most popular and least popular restaurant according to the reviews number in the dataset during the week.

2.  Use the map to show the reviews and ratings for different business locations, categories, and geographic regions.

3.  The Neighborhood is one of the important factors affecting the choice of customers. Businesses will also consider neighborhood when they select the locations, thinking whether the restaurant can make benefit in the neighborhood and whether they can find their niche there. I will make bubble chart to show the relations between neighborhood, categories, and reviews.

### Data

Data will be downloaded from Yelp Dataset Challenge round 9 from yelp website <https://www.yelp.com/dataset>. The JSON dataset will be chosen imported into R for the further processing.

The dataset has:

4.1M reviews;

947K tips;

1M users;

144K businesses;

1.1M business attributes( e.g. hours, parking availability, ambiance; and aggregated check-ins over time for each of the 125K businesses)

The data includes diverse sets of cities:

Edinburgh in U.K.;

Karlsruhe in Germany;

Montreal and Waterloo in Canada,

Pittsburgh, Charlotte,

Urbana-Champaign,

Phoenix, Las Vagas,

Madison

Cleveland in U.S.

### Challenges

I will have to clean the Data to extract the relevant attributes of interest and applying. The datasets are in big size so it will take long running time. If I can not find a place online to hold the medium/large size data I will split the datasets into small pieces and combine them after loading.

The reviews could be sparse and there could be some bias as some reviewers tend to rate higher/lower than average. Some normalization may be applied when doing the analysis.

Packages

``` r
suppressWarnings(suppressMessages(library(jsonlite)))
suppressWarnings(suppressMessages(library(tidyjson)))
suppressWarnings(suppressMessages(library(plyr)))
suppressWarnings(suppressMessages(library(dplyr)))

suppressWarnings(suppressMessages(library(knitr)))
suppressWarnings(suppressMessages(library(tidyr)))
suppressWarnings(suppressMessages(library(ggplot2)))
suppressWarnings(suppressMessages(library(ggthemes)))
suppressWarnings(suppressMessages(library(viridis)))
suppressWarnings(suppressMessages(library(stringr)))
suppressWarnings(suppressMessages(library(data.table)))
```

\*\*For task 1:\*

``` r
checkin <- data.frame()
for (i in seq(1,10)){
  url = paste0("https://raw.githubusercontent.com/YunMai-SPS/DA608_homework/master/DA608_final_project/checkin",i,".csv")
  itm<- fread(url)
  checkin <- rbind(checkin,itm)
}
checkin <- checkin[,-c(1,2)]
checkin[,5]<-lapply(checkin[,5],as.numeric)
checkin <-drop_na(checkin)

ct <- checkin %>% group_by(business_id) %>% summarise(n = n()) %>% arrange(desc(n))
b_id <- c(unlist(list(ct[1:10,1])))

checkin_plot <- subset(checkin,business_id %in% b_id)

p <- ggplot(checkin_plot, aes(x=Hour, y=Day, fill=Review_Number))
p <- p + geom_tile(color="white", size=0.1)
p <- p + scale_fill_viridis(name="# Reviews")
p <- p + coord_equal()
p <- p + facet_wrap(~business_id, ncol=5)
p <- p + labs(x=NULL, y=NULL, title="Reviews per weekday & time of day by restaurant")
p <- p + theme_tufte()
p
```

![](YMai_608_final_proposal_files/figure-markdown_github-ascii_identifiers/unnamed-chunk-2-1.png)

I will use the whole dataset to do the visulization so there will be a lot of restaurants. The name and the location(city) will be added for corresponding record. The interaction will be slecting the city etiher by dropdown list or slid bar.

**For task 2**

``` r
bsn <- data.frame()
for (i in seq(1,3)){
  url = paste0("https://raw.githubusercontent.com/YunMai-SPS/DA608_homework/master/DA608_final_project/business",i,".csv")
  itm<- fread(url)
  bsn <- rbind(bsn,itm)
}

kable(head(bsn,5))
```

| V1  | V1  | business\_id            | name                | neighborhood   | address                   | city      | state | postal\_code |  latitude|   longitude|  stars|  review\_count|
|:----|:----|:------------------------|:--------------------|:---------------|:--------------------------|:----------|:------|:-------------|---------:|-----------:|------:|--------------:|
| 1   | 1   | 0DI8Dt2PJp07XkVvIElIcQ  | Innovative Vapors   |                | 227 E Baseline Rd, Ste J2 | Tempe     | AZ    | 85283        |  33.37821|  -111.93610|    4.5|             17|
| 2   | 2   | LTlCaCGZE14GuaUXUGbamg  | Cut and Taste       |                | 495 S Grand Central Pkwy  | Las Vegas | NV    | 89106        |  36.19228|  -115.15927|    5.0|              9|
| 3   | 3   | EDqCEAGXVGCH4FJXgqtjqg  | Pizza Pizza         | Dufferin Grove | 979 Bloor Street W        | Toronto   | ON    | M6H 1L5      |  43.66105|   -79.42909|    2.5|              7|
| 4   | 4   | cnGIivYRLxpF7tBVR\_JwWA | Plush Salon and Spa |                | 7014 Steubenville Pike    | Oakdale   | PA    | 15071        |  40.44454|   -80.17454|    4.0|              4|
| 5   | 5   | cdk-qqJ71q6P7TJTww\_DSA | Comfort Inn         | Downtown Core  | 321 Jarvis Street         | Toronto   | ON    | M5B 2C2      |  43.65983|   -79.37540|    3.0|              8|

The interaction for task 2 will be tooltips showing the name, average ratings and review numbers.

**For task 3**

``` r
length(unique(bsn$neighborhood))/length(unique(bsn$business_id))
```

    ## [1] 0.002623688

Only 0.2% business has the neighborhood attribute. I will only 37746 restaurants to see whether there is any pattern. Bubble chart will be used.

For the final project, I plan to use Dash to make the interactions. Tools will be used are: matplotlib . Plotly, Seaborn, cufflinks, bokeh.
