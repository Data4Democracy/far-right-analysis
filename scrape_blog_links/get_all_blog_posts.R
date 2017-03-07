# scrape_blog_links_byyear: Function that takes a year & blog_domain as argument
#    and grabs all links to posts from that year.  Returns a character vector
#    of urls

library(rvest); library(dplyr); library(stringr)
library(lubridate); library(readr); library(httr)

scrape_blog_links_byyear <- function(year, blog_domain){
     require(rvest); require(dplyr); require(stringr)
     require(lubridate); require(readr); require(httr)
     
     blog_post_links <- list()
     if(year == year(now())){
          date_range <- seq(as.Date(paste0(year, "-01-01")), 
                            as.Date(substr(now(), 1, 10)), by = 1L)
     }else{
          date_range <- seq(as.Date(paste0(year, "-01-01")), 
                            as.Date(paste0(year, "-12-31")), by = 1L)
     }
     
     base_url <- function(date){
          paste0(blog_domain, 
                 "/", year(date),
                 "/", str_pad(month(date), pad = "0", width = 2),
                 "/", str_pad(mday(date), pad = "0", width = 2))
     }
     blog_urls <- vector(mode = "list", length = length(date_range))
     
     for(i in seq_along(date_range)){
          print(paste0("archive page index: ", i))
          archive_base_url <- base_url(date_range[i])
          print(archive_base_url)
          error_404 <- FALSE
          counter <- 1
          while(error_404 == FALSE & counter <= 30){
               print(paste0("counter: ", counter))
               archive_page_url <- paste0(archive_base_url, "/page/", counter)
               print(paste0("archive page url: ", archive_page_url))
               archive_page_response <- GET(archive_page_url)
               archive_page_status <- status_code(archive_page_response)
               print(paste0("archive page status code: ", archive_page_status))
               if(archive_page_status == 404){
                    error_404 <- TRUE
               }else{
                    blog_urls[[i]]$post_links <- 
                         archive_page_response %>% read_html() %>% 
                         html_nodes(".entry-title a") %>% html_attr("href")
               }
               counter <- counter + 1
          }
     }     
     return(blog_urls %>% unlist() %>% unname())
}

# Get some data for blog "Western Rifle Shooters" and write to CSV
blog_domain <- "https://westernrifleshooters.wordpress.com"
data_frame(post_url = scrape_blog_links_byyear(2017, blog_domain)) %>% 
     write_csv("scrape_blog_links/westernrifleshooters_2017.csv")
data_frame(post_url = scrape_blog_links_byyear(2016, blog_domain)) %>%
     write_csv("scrape_blog_links/westernrifleshooters_2016.csv")