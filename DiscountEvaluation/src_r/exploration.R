library(tidyverse)
library(rstatix)
library(ggplot2)

data <- read.csv("./output/dyad/roUrParl_dataset.csv")
data <- read.csv("./output/dyad/dakshina_dataset.csv")

analysis <- function(data,variable){
  summary<-data %>%
    group_by(Keyboard) %>%
    get_summary_stats(variable, type = "common")
  print(summary)
  
  plot<-ggplot(data, aes(x=Keyboard, y=.data[[variable]])) + 
    geom_bar(stat = "identity")
  print(plot)
  
  # Friedman
  formula <- as.formula(paste(variable," ~ Keyboard | X"))
  friedman_results <- friedman_test(data,formula)
  print(friedman_results)
  
  # Effect size
  effect_size <- friedman_effsize(data,formula) 
  print(effect_size)
  
  # Post-hoc
  formula <- as.formula(paste(variable," ~ Keyboard"))
  pwc <- wilcox_test(data,formula, paired = TRUE, p.adjust.method = "hommel")
  print(pwc)
}

##################
# SMOOTHING #
##################
# smoothing normalizes the values too!
# Add-1 Smoothing
crulp <- subset(data, Keyboard == "CRULP")
windows <- subset(data, Keyboard == "WINDOWS")
ime <- subset(data, Keyboard == "IME")

#9024 is subject count or vocab count in language model terms
crulp$Probability <- (crulp$Frequency+1)/(sum(crulp$Frequency)+9024)
ime$Probability <- (ime$Frequency+1)/(sum(ime$Frequency)+9024)
windows$Probability <- (windows$Frequency+1)/(sum(windows$Frequency)+9024)
data <- rbind(crulp, windows, ime)

#############################
# KEYYING DISTANCE ANALYSIS #
#############################

# Calculate TotalDistance (Without Smoothing)
data$BigramDistance <- data$KeyyingDistance*data$Probability
analysis(data,"BigramDistance")

boards <- c("WINDOWS","CRULP","IME")
for (board in boards){
  print(board)
  plot<-ggplot(subset(data, Keyboard == board), aes(x = BigramDistance)) + 
    geom_histogram(position = "identity", bins=100)
  print(plot)
}
# IME has more values close to 0

      
print("=================================================================")

################################
# PER FINGER DISTANCE ANALYSIS #
################################
fingers <- c("little","ring","middle","index")
results_list <- list()
for (finger in fingers) {
  print(paste("l_",finger))
  data[[finger]] <- (data[[paste("l_",finger, sep = "")]]*data$Probability) +
                    (data[[paste("r_",finger, sep = "")]]*data$Probability)
  analysis(data,finger)
  
  boards <- c("WINDOWS","CRULP","IME")
  for (board in boards){
    print(board)
    plot<-ggplot(subset(data, Keyboard == board), aes(x = .data[[finger]])) + 
      geom_histogram(position = "identity", bins=100)
    print(plot)
  }

  print("=================================================================")
}
# could significane be inflated by high number of 0 frequency where other keyboard on same key has high value freq

##############################
# PER HAND DISTANCE ANALYSIS #
##############################
data$RightHand <- (data$right_total*data$Probability)
analysis(data,"RightHand")
print("=================================================================")
data$LeftHand <- (data$left_total*data$Probability)
analysis(data,"LeftHand")
print("=================================================================")
data$HandDiff <- (data$RightHand-data$LeftHand)
analysis(data,"HandDiff")
print("=================================================================")

###################
# STROKE ANALYSIS #
###################

stroke_types <- c("SameHand","SameKey","SameFinger","Reach", "Hurdle")
results_list <- list()

for (stroke_type in stroke_types) {
  data[[stroke_type]] <- ifelse(data[[stroke_type]] == "True", 1, 0)
  data[[stroke_type]] <- (data[[stroke_type]]*data$Probability) +
    (data[[stroke_type]]*data$Probability)
  analysis(data,stroke_type)
  print("=================================================================")
}
