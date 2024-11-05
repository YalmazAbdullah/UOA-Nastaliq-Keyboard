library(tidyverse)
library(ggpubr)
library(rstatix)

################
# Prepare Data #
################
# Read Data
data <- read.csv("./output/data/dakshina.csv")
data <- read.csv("./output/data/roUrParl.csv")
view(data)

# Add Hand-Finger combined column
# Each key uses only one Hand-Finger combination
data$Hand_Finger <- paste(data$Hand, data$Finger)
view(data)

# Add 1 smoothing
crulp <- subset(data, Keyboard == "CRULP")
roman <- subset(data, Keyboard == "Roman")
windows <- subset(data, Keyboard == "Windows")

crulp$Prob <- (crulp$Frequency)/(sum(crulp$Frequency))
roman$Prob <- (roman$Frequency)/(sum(roman$Frequency))
windows$Prob <- (windows$Frequency)/(sum(windows$Frequency))

data <- rbind(crulp, roman, windows)
view(data)

# Total distance calculation
data$Base <- data$Distance*data$Prob
view(data)

# Summary stats
data %>%
  group_by(Keyboard) %>%
  get_summary_stats(Base, type = "common") 

# Finger distance graph
new_data <- data %>%
  group_by(Finger) %>%
  summarise(Total_Base = sum(Base))
ggplot(data, aes(fill=Keyboard, y=Base, x=Finger)) + 
    geom_bar(position="dodge", stat="Base")

# Finger freq
new_data <- data %>%
  group_by(Finger) %>%
  summarise(Total_Base = sum(Frequency))
ggplot(data, aes(fill=Keyboard, y=Frequency, x=Finger)) + 
    geom_bar(position="dodge", stat="Frequency")

# Hand
new_data <- data %>%
  group_by(Hand) %>%
  summarise(Total_Base = sum(Frequency))
ggplot(data, aes(fill=Keyboard, y=Frequency, x=Hand)) + 
    geom_bar(position="dodge", stat="Frequency")

# Row
# Alternating