library(readr)
library(tidyverse)

combine_fingers <- function(df) {
  # Combined finger press
  df$Press_Little <- df$Press_L_Little + df$Press_R_Little
  df$Press_Ring   <- df$Press_L_Ring   + df$Press_R_Ring
  df$Press_Middle <- df$Press_L_Middle + df$Press_R_Middle
  df$Press_Index  <- df$Press_L_Index  + df$Press_R_Index
  
  # Combined finger distance
  df$Dist_Little  <- df$Dist_L_Little + df$Dist_R_Little
  df$Dist_Ring    <- df$Dist_L_Ring   + df$Dist_R_Ring
  df$Dist_Middle  <- df$Dist_L_Middle + df$Dist_R_Middle
  df$Dist_Index   <- df$Dist_L_Index  + df$Dist_R_Index
  
  # Combined hand press
  df$Press_L <- df$Press_L_Little + df$Press_L_Ring + df$Press_L_Middle + df$Press_L_Index
  df$Press_R <- df$Press_R_Little + df$Press_R_Ring + df$Press_R_Middle + df$Press_R_Index
  
  # Combined hand distance
  df$Dist_L <- df$Dist_L_Little + df$Dist_L_Ring + df$Dist_L_Middle + df$Dist_L_Index
  df$Dist_R <- df$Dist_R_Little + df$Dist_R_Ring + df$Dist_R_Middle + df$Dist_R_Index
  
  # Total press
  df$Press <- df$Press_L + df$Press_R
  
  # Total distance
  df$Dist <- df$Dist_L + df$Dist_R
  return(df)
}

data_unigram <- read.csv("../../Data_Discount/scored/monad_combined_subset.csv")
data_bigram <- read.csv("../../Data_Discount/scored/dyad_combined_subset.csv")
data_sentence <- read.csv("../../Data_Discount/scored/sentence_combined_subset.csv")
data_bigram<-combine_fingers(data_bigram)
data_sentence<-combine_fingers(data_sentence)

head(data_unigram)