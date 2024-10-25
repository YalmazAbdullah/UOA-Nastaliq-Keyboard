library(FSA)
library(tidyverse)
library(ggpubr)
library(rstatix)
library(lme4)
library(robustlmm)
library(ggplot2)
library(emmeans)

# Read Data
data <- read.csv("./output/dakshina.csv")
data <- read.csv("./output/roUrParl.csv")
view(data)

# Add Hand-Finger combined column
# Each key uses only one Hand-Finger combination
data$HandFinger <- paste(data$Hand, data$Finger)
view(data)

#Add 1 smoothing
crulp <- subset(data, Keyboard == "CRULP")
roman <- subset(data, Keyboard == "Roman")
windows <- subset(data, Keyboard == "Windows")

crulp$Freq_Add1 <- (crulp$Frequency+1)/(sum(crulp$Frequency)+length(crulp$Frequency))
roman$Freq_Add1 <- (roman$Frequency+1)/(sum(roman$Frequency)+length(roman$Frequency))
windows$Freq_Add1 <- (windows$Frequency+1)/(sum(windows$Frequency)+length(windows$Frequency))

data <- rbind(crulp, roman, windows)
