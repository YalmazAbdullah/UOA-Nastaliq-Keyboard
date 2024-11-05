library(tidyverse)
library(rstatix)
library(nlme)
library(lme4)

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

crulp$Prob_Add1 <- (crulp$Frequency+1)/(sum(crulp$Frequency)+length(crulp$Frequency))
roman$Prob_Add1 <- (roman$Frequency+1)/(sum(roman$Frequency)+length(roman$Frequency))
windows$Prob_Add1 <- (windows$Frequency+1)/(sum(windows$Frequency)+length(windows$Frequency))

data <- rbind(crulp, roman, windows)
view(data)

# Total distance calculation and log transformation
data$Base <- data$Distance*data$Prob_Add1
data$Base <- log(df$Base)
view(data)

##################################
# Non linear mixed effects Model #
##################################
mod <- lme(Base ~  Keyboard *Hand_Finger , random = ~ Keyboard | Key, data =data)
mod
plot(mod)

summary <- summary(mod)
table = summary$tTable 
table 

anova(mod)

modnlme1 <- nlme(Base ~  Keyboard *Hand_Finger, data = data,
                 random = ~ Keyboard | Key,
                 fixed = Hand_Finger+Keyboard,
                 start = )

