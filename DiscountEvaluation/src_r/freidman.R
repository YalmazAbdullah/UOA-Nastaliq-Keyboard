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

crulp$Prob_Add1 <- (crulp$Frequency+1)/(sum(crulp$Frequency)+length(crulp$Frequency))
roman$Prob_Add1 <- (roman$Frequency+1)/(sum(roman$Frequency)+length(roman$Frequency))
windows$Prob_Add1 <- (windows$Frequency+1)/(sum(windows$Frequency)+length(windows$Frequency))

data <- rbind(crulp, roman, windows)
view(data)

# Total distance calculation
data$Base <- data$Distance*data$Prob_Add1
view(data)

####################
# Key and Keyboard #
####################
res.fried <- data %>% friedman_test(Base ~ Keyboard | Key)
res.fried

# Effect size
data %>% friedman_effsize(Base ~ Keyboard |Key) 

# Post-hoc
pwc <- data %>%
  wilcox_test(Base ~ Keyboard, paired = TRUE, p.adjust.method = "hommel")
pwc 
ggboxplot(data, x = "Keyboard", y = "Base", add = "jitter")

###########################
# Hand_Finger and Keyboard #
###########################

data <- data %>%
  group_by(Hand_Finger,Keyboard) %>%
  summarise(Sum_Value = sum(Base), .groups = 'drop')
view(data)

res.fried <- data %>% friedman_test(Sum_Value ~ Keyboard | Hand_Finger)
res.fried
knitr::kable(res.fried, format = "markdown")

# Effect size
data %>% friedman_effsize(Sum_Value ~ Keyboard |Hand_Finger) 

# Post-hoc
pwc <- data %>%
  wilcox_test(Sum_Value ~ Keyboard, paired = TRUE, p.adjust.method = "hommel")
pwc 
knitr::kable(pwc, format = "markdown")

ggboxplot(data, x = "Keyboard", y = "Sum_Value", add = "jitter")
