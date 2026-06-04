library(tidyverse)
library(rstatix)
library(ggplot2)
library(ggpubr)

data_combined <- read.csv(
  "../../Data_Discount/scored/monad_combined_subset.csv"
)

data_dakshina <- read.csv(
  "../../Data_Discount/scored/monad_dakshina_dataset.csv"
)

data_roUrParl <- read.csv(
  "../../Data_Discount/scored/monad_roUrParl_dataset.csv"
)

# combine into single df for comparison
df <- bind_rows(
  data_combined  %>% mutate(Source = "combined"),
  data_dakshina  %>% mutate(Source = "dakshina"),
  data_roUrParl  %>% mutate(Source = "roUrParl")
)
df$Source <- factor(df$Source, levels = c("combined", "dakshina", "roUrParl"))

print(df)